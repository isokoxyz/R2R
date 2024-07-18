
class CameraHandler:
    """
    This class contains helper functions that control a Blender scene camera
    """
    def __init__(self, bpy):
        self.bpy = bpy
    
    def set_scene_camera(self, cam_name):
        """
        This function sets the name of the scene camera
        """
        obj_camera = self.bpy.data.objects[cam_name]
        self.bpy.context.scene.camera = obj_camera

    def shift_camera_lens(self, cam_name, shift_x, shift_y):
        """
        This function moves the camera lens by the specified amount in the x and y directions
        """
        camera = self.bpy.data.cameras[cam_name]
        camera.shift_x = shift_x
        camera.shift_y = shift_y