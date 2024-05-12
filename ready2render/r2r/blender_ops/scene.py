import bpy
from pygltflib import GLTF2
from r2r.blender_ops.materials import transfer_materials

# Deletion
def delete_all_objects_in_scene():
    """
    Deletes all objects in the current scene
    """
    deleteListObjects = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'HAIR', 'POINTCLOUD', 'VOLUME', 'GPENCIL',
                         'ARMATURE', 'LATTICE', 'EMPTY', 'LIGHT', 'LIGHT_PROBE', 'CAMERA', 'SPEAKER']

    for o in bpy.context.scene.objects:
        for i in deleteListObjects:
            if o.type == i:
                o.select_set(False)
            else:
                o.select_set(True)
    bpy.ops.object.delete()

def delete_objects_from_collection_name(collection_name):
    bpy.ops.outliner.orphans_purge()
    select_only_objects_in_collection_name(collection_name)
    delete_and_unlink()

def delete_and_unlink():
    for o in bpy.context.selected_objects:
        bpy.data.objects.remove(o, do_unlink=True)

def deselect_all_scene_objects():
    # for ob in bpy.context.selected_objects:
    #     ob.select_set(False)
    bpy.ops.object.select_all(action='DESELECT')

# Selection
def select_only_objects_in_collection_name(collection_name):
    collection = bpy.data.collections[collection_name]
    deselect_all_scene_objects()
    select_all_objects_in_collection(collection)

def select_only_objects_in_collection(collection):
    deselect_all_scene_objects()
    select_all_objects_in_collection(collection)

def select_all_objects_in_collection(collection):
    # for obj in collection.all_objects:
    #     obj.select_set(True)
    for scene in bpy.data.scenes:
        for view_layer in scene.view_layers:
            for o in view_layer.objects:
                if o.users_collection[0].name == collection.name:
                    o.select_set(True)

# Import / Export
def import_scene_into_collection(file_path, collection_name): 
    bpy.ops.object.select_all(action='DESELECT')
    
    if collection_name in bpy.data.collections:
        if bpy.data.collections[collection_name] is not bpy.context.scene.collection:
            bpy.data.collections.remove(bpy.data.collections[collection_name])

    bpy.ops.import_scene.gltf(filepath=file_path)
    bpy.ops.collection.create(name=collection_name)

    return bpy.data.collections[collection_name]

def export_scene(output_file, export_all=True, format='GLB'):
    if export_all:
        bpy.ops.object.select_all(action='SELECT')
    # print("OVERRIDING CONTEXT")
    # context_override = bpy.context.copy()
    # context_override["active_object"] = None

    with bpy.context.temp_override(active_object=bpy.data.objects["Car_Body"], window=bpy.context.window):
        if format == "GLB":
            bpy.ops.export_scene.gltf(
                filepath=output_file,
                use_selection=True,
                export_format=format,
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

# Object operations
def rename_object_in_scene(old_name, new_name):
    old_object = bpy.data.objects.get(old_name)
    old_object.name = new_name

def set_object_location(object_name, location):
    obj = bpy.data.objects[object_name]

    obj.location.x = location['x']
    obj.location.y = location['y']
    obj.location.z = location['z']

def set_object_rotation(object_name, rotation, mode):
    obj = bpy.data.objects[object_name]

    if mode == "quaternion":
        obj.rotation.w = rotation['w']
        obj.rotation.x = rotation['x']
        obj.rotation.y = rotation['y']
        obj.rotation.z = rotation['z']

def apply_transform_to_selected_object(target_object, location=True, rotation=True):
    select_object_and_make_active(target_object)
    bpy.ops.object.transform_apply(location=location, rotation=rotation)

def select_object_and_make_active(selected_object):
    selected_object.select_set(True)
    bpy.context.view_layer.objects.active = selected_object

def select_object_by_name_and_make_active(object_name):
    selected_object = bpy.data.objects.get(object_name)
    # selected_object.select_set(True)
    # bpy.context.view_layer.objects.active = selected_object
    select_object_and_make_active(selected_object)

    return selected_object

def link_selected_objects_in_scene(name):
    bpy.ops.object.make_links_data(type=name)

def make_object_active(object):
    bpy.context.view_layer.objects.active = object

def parenting_object(parent_object, child_object):
    bpy.ops.object.select_all(action="DESELECT")
    child_object.select_set(True)
    parent_object.select_set(True)
    bpy.context.view_layer.objects.active = parent_object
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

def place_object(should_transfer_w_materials, should_clear_old_materials, dest_group_object_name, target_name):
    dest_group_object = bpy.data.objects.get(dest_group_object_name)
    target_object = bpy.data.objects.get(target_name)

    target_object.location.x = dest_group_object.location.x
    target_object.location.y = dest_group_object.location.y
    target_object.location.z = dest_group_object.location.z

    target_object.rotation_quaternion.w = dest_group_object.rotation_quaternion.w
    target_object.rotation_quaternion.x = dest_group_object.rotation_quaternion.x
    target_object.rotation_quaternion.y = dest_group_object.rotation_quaternion.y
    target_object.rotation_quaternion.z = dest_group_object.rotation_quaternion.z

    bpy.ops.object.select_all(action="DESELECT")

    target_object.select_set(True)
    bpy.context.view_layer.objects.active=target_object
    bpy.ops.object.transform_apply(location=True, rotation=True)

    parenting_object(dest_group_object, target_object)

    if should_transfer_w_materials:
        transfer_materials(should_clear_old_materials, dest_group_object, target_object)

# Collection operations
def relink_collection(src_collection_name, dest_collection_name):
    src_collection = bpy.data.collections[src_collection_name]
    dest_collection = bpy.data.collections[dest_collection_name]

    for o in src_collection.all_objects:
        dest_collection.objects.link(o)
        src_collection.objects.unlink(o)

def add_metadata_to_gltf(gltf_file_path, metadata, save_format):
    gltf = GLTF2()
    gltf = gltf.load(gltf_file_path)
    gltf.extras = metadata
    gltf.save(gltf_file_path)

    # if save_format == '.glb':
    #     output_file_path = gltf_file_path.split('.')[0] + save_format
    #     gltf2glb(gltf_file_path, output_file_path, override=True)
