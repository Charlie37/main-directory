bl_info = {
    "name": "Vertex Groups",
    "category": "Object",
    "author": "Arnaud Trouve"
}

import bpy

"""This menu counts the number of vertex groups of the selected object"""
class ObjectVertexGroups(bpy.types.Operator):
    """Object Vertex Groups"""
    bl_idname = "object.vertex_groups"
    bl_label = "Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}

    total = bpy.props.IntProperty(name="Steps", default=2, min=1, max=100)

    def execute(self, context):
        scene = context.scene
        cursor = scene.cursor_location
        obj = scene.objects.active

        vgdict = {}
        vgcpt = 0
        mesh = obj.to_mesh(scene, True, "PREVIEW")
        for g in obj.vertex_groups:
           if g.name == "tete" or g.name == "corps":
               vgcpt += 1
               vgdict[g.index]=g.weight

        meshcpt = 0
        for vert in mesh.vertices:
            for group in vert.groups:
               gr = group.group
               for gi in vgdict.keys():
                   if gi == gr:
                       meshcpt += 1
               #print(vertex, g, g.weight)
               
        group_names = [g.name for g in obj.vertex_groups]
        group_names_tot = len(group_names)
        self.report({'INFO'}, "Vertex Groups: " + str(meshcpt) + "/" + str(vgcpt) + "/" + str(group_names_tot))

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(ObjectVertexGroups.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(ObjectVertexGroups)
    bpy.types.VIEW3D_MT_object.append(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(ObjectVertexGroups.bl_idname, 'SPACE', 'PRESS', ctrl=True, shift=True)
    kmi.properties.total = 4
    addon_keymaps.append(km)

def unregister():
    bpy.utils.unregister_class(ObjectVertexGroups)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    del addon_keymaps[:]


if __name__ == "__main__":
    print('-----executing------')
    register()
