
class CameraHandler:
    def __init__(self, bpy):
        self.bpy = bpy
    
    def set_scene_camera(self, cam_name):
        obj_camera = self.bpy.data.objects[cam_name]
        self.bpy.context.scene.camera = obj_camera

    def shift_camera_lens(self, cam_name, shift_x, shift_y):
        camera = self.bpy.data.cameras[cam_name]
        camera.shift_x = shift_x
        camera.shift_y = shift_y