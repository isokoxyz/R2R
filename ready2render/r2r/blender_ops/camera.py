import bpy

def set_scene_camera(cam_name):
    obj_camera = bpy.data.objects[cam_name]
    bpy.context.scene.camera = obj_camera