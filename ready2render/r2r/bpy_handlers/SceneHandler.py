from pygltflib import GLTF2
from r2r.bpy_handlers.ObjectHandler import ObjectHandler


class SceneHandler:
    """
    This class contains helper functions to control and modify a Blender scene
    """
    def __init__(self, bpy):
        self.bpy = bpy
        self.object_handler = ObjectHandler(bpy=bpy)

    def delete_all_objects_in_scene(self):
        """
        Deletes all objects in the current scene
        """
        deleteListObjects = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'HAIR', 'POINTCLOUD', 'VOLUME', 'GPENCIL',
                             'ARMATURE', 'LATTICE', 'EMPTY', 'LIGHT', 'LIGHT_PROBE', 'CAMERA', 'SPEAKER']

        for o in self.bpy.context.scene.objects:
            for i in deleteListObjects:
                if o.type == i:
                    o.select_set(False)
                else:
                    o.select_set(True)
        self.bpy.ops.object.delete()

    def delete_objects_from_collection_name(self, collection_name):
        """
        This function deletes all objects from the collection with the specified name
        """
        self.bpy.ops.outliner.orphans_purge()
        self.select_only_objects_in_collection_name(collection_name)
        self.delete_and_unlink()

    def delete_and_unlink(self):
        """
        This function deletes all objects and their links
        """
        for o in self.bpy.context.selected_objects:
            self.bpy.data.objects.remove(o, do_unlink=True)

    def deselect_all_scene_objects(self):
        """
        This function deletes all scene objects
        """
        # for ob in bpy.context.selected_objects:
        #     ob.select_set(False)
        self.bpy.ops.object.select_all(action='DESELECT')

    def select_only_objects_in_collection_name(self, collection_name):
        """
        This function selects objects in the collection with the specified name
        """
        collection = self.bpy.data.collections[collection_name]
        self.deselect_all_scene_objects()
        self.select_all_objects_in_collection(collection)

    def select_only_objects_in_collection(self, collection):
        """
        This function selects objects in the specified collection
        """
        self.deselect_all_scene_objects()
        self.select_all_objects_in_collection(collection)

    def select_all_objects_in_collection(self, collection):
        """
        This function selects objects in the specified collection
        """
        # for obj in collection.all_objects:
        #     obj.select_set(True)
        for scene in self.bpy.data.scenes:
            for view_layer in scene.view_layers:
                for o in view_layer.objects:
                    if o.users_collection[0].name == collection.name:
                        print(o)
                        o.select_set(True)

    def import_scene_into_collection(self, file_path, collection_name):
        """
        This function imports data from file into the scene with the specified collection naeme
        """
        bpy = self.bpy
        bpy.ops.object.select_all(action='DESELECT')

        if collection_name in bpy.data.collections:
            if bpy.data.collections[collection_name] is not bpy.context.scene.collection:
                bpy.data.collections.remove(
                    bpy.data.collections[collection_name])

        bpy.ops.import_scene.gltf(filepath=file_path)
        bpy.ops.collection.create(name=collection_name)

        return bpy.data.collections[collection_name]

    def export_scene(self, output_file, export_all=True, format='GLB'):
        """
        This function exports the scene with the specified format to the destination path
        """
        if export_all:
            self.bpy.ops.object.select_all(action='SELECT')

        if format == "GLB":
            self.bpy.ops.export_scene.gltf(
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

    def rename_object_in_scene(self, old_name, new_name):
        old_object = self.bpy.data.objects.get(old_name)
        old_object.name = new_name

    def set_object_location(self, object_name, location):
        obj = self.bpy.data.objects[object_name]

        obj.location.x = location['x']
        obj.location.y = location['y']
        obj.location.z = location['z']

    def set_object_rotation(self, object_name, rotation, mode):
        obj = self.bpy.data.objects[object_name]

        if mode == "quaternion":
            obj.rotation.w = rotation['w']
            obj.rotation.x = rotation['x']
            obj.rotation.y = rotation['y']
            obj.rotation.z = rotation['z']

    def apply_transform_to_selected_object(self, target_object, location=True, rotation=True):
        self.select_object_and_make_active(target_object)
        self.bpy.ops.object.transform_apply(
            location=location, rotation=rotation)

    def select_object_and_make_active(self, selected_object):
        selected_object.select_set(True)
        self.bpy.context.view_layer.objects.active = selected_object

    def select_object_by_name_and_make_active(self, object_name):
        selected_object = self.bpy.data.objects.get(object_name)

        self.select_object_and_make_active(selected_object)

        return selected_object

    def link_selected_objects_in_scene(self, name):
        self.bpy.ops.object.make_links_data(type=name)

    def make_object_active(self, object):
        self.bpy.context.view_layer.objects.active = object

    def parenting_object(self, parent_object, child_object):
        bpy = self.bpy

        bpy.ops.object.select_all(action="DESELECT")

        child_object.select_set(True)
        parent_object.select_set(True)

        bpy.context.view_layer.objects.active = parent_object
        bpy.ops.object.parent_set(
            type='OBJECT', keep_transform=False)

    def place_object(self, should_transfer_w_materials, should_clear_old_materials, dest_group_object_name, target_name):
        bpy = self.bpy

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
        bpy.context.view_layer.objects.active = target_object
        bpy.ops.object.transform_apply(location=True, rotation=True)

        self.parenting_object(dest_group_object, target_object)

        if should_transfer_w_materials:
            self.object_handler.material_handler.transfer_materials(should_clear_old_materials,
                                                                    dest_group_object, target_object)

    def relink_collection(self, src_collection_name, dest_collection_name):
        """
        This function links objects from source collection to destination collection
        """
        src_collection = self.bpy.data.collections[src_collection_name]
        dest_collection = self.bpy.data.collections[dest_collection_name]

        for o in src_collection.all_objects:
            dest_collection.objects.link(o)
            src_collection.objects.unlink(o)

    def add_metadata_to_gltf(gltf_file_path, metadata, save_format):
        """
        This function adds extra metadata to the GLTF file's 'extras' parameter
        """
        gltf = GLTF2()
        gltf = gltf.load(gltf_file_path)
        gltf.extras = metadata
        gltf.save(gltf_file_path)
