from r2r.bpy_handlers.MaterialHandler import MaterialHandler


class ObjectHandler:
    """
    This class provides helper functions to modify an Object in a Blender scene
    """
    def __init__(self, bpy):
        self.bpy = bpy
        self.material_handler = MaterialHandler(bpy=bpy)

    def rename_object_in_scene(self, old_name, new_name):
        """
        This function renames an object
        """
        old_object = self.bpy.data.objects.get(old_name)
        old_object.name = new_name

    def set_object_location(self, object_name, location):
        """
        This function sets the x,y,z location values of an object
        """
        obj = self.bpy.data.objects[object_name]

        obj.location.x = location['x']
        obj.location.y = location['y']
        obj.location.z = location['z']

    def set_object_rotation(self, object_name, rotation, mode):
        """
        This function sets the rotation values of an object for the specified mode
        """
        obj = self.bpy.data.objects[object_name]

        if mode == "quaternion":
            obj.rotation.w = rotation['w']
            obj.rotation.x = rotation['x']
            obj.rotation.y = rotation['y']
            obj.rotation.z = rotation['z']

    def apply_transform_to_selected_object(self, target_object, location=True, rotation=True):
        """
        This function applies a transformation to an object's location and rotation
        """
        self.select_object_and_make_active(target_object)
        self.bpy.ops.object.transform_apply(location=location, rotation=rotation)

    def select_object_and_make_active(self, selected_object):
        """
        This function makes the specified object active
        """
        selected_object.select_set(True)
        self.bpy.context.view_layer.objects.active = selected_object

    def select_object_by_name_and_make_active(self, object_name):
        """
        This function selects the object with the specified name and makes it active
        """
        selected_object = self.bpy.data.objects.get(object_name)
        # selected_object.select_set(True)
        # bpy.context.view_layer.objects.active = selected_object
        self.select_object_and_make_active(selected_object)

        return selected_object

    def set_object_origin(self, type, center):
        """
        This function sets an objects origin values
        """
        self.bpy.ops.object.origin_set(type=type, center=center)

    def link_selected_objects_in_scene(self, type):
        """
        This function links selected objects
        """
        self.bpy.ops.object.make_links_data(type=type)

    def make_object_active(self, object):
        """
        This function makes an object active
        """
        self.bpy.context.view_layer.objects.active = object

    def parenting_object(self, parent_object, child_object):
        """
        This function sets a parent to a child object
        """
        bpy = self.bpy

        bpy.ops.object.select_all(action="DESELECT")
        child_object.select_set(True)
        parent_object.select_set(True)

        bpy.context.view_layer.objects.active = parent_object
        bpy.ops.object.parent_set(
            type='OBJECT', keep_transform=False)

    def place_object(self, should_transfer_w_materials, should_clear_old_materials, dest_group_object_name, target_name):
        """
        This function transfers an object with its materials to a new object with a specified name
        """
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
            self.material_handler.transfer_materials(should_clear_old_materials,
                                                     dest_group_object, target_object)
