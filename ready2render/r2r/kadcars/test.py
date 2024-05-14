import bpy


dest_nft_glb = 'C:/Users/Mohannad Ahmad\Desktop\AppDev\Crypto\Kadena\Kadcars\R2R/ready2render/r2r\kadcars\kadcar.glb'
collection_name = "lol"

bpy.ops.object.select_all(action='DESELECT')
if collection_name in bpy.data.collections:
    if bpy.data.collections[collection_name] is not bpy.context.scene.collection:
        bpy.data.collections.remove(bpy.data.collections[collection_name])
bpy.ops.import_scene.gltf(filepath=dest_nft_glb)
bpy.ops.collection.create(name=collection_name)

bpy.ops.object.select_all(action='SELECT')

print(bpy.context.active_object)
exit()
bpy.ops.export_scene.gltf(
    filepath="K:/lol.glb",
    use_selection=True,
    export_format="GLB",
    export_apply=True,
    export_texcoords=True,
    export_normals=True,
    export_tangents=True,
    export_materials='EXPORT',
    export_colors=True,
    export_cameras=True,
    export_animations=False
    # use_mesh_edges=True,
    # use_mesh_vertices=True,
    # export_extras=True
)