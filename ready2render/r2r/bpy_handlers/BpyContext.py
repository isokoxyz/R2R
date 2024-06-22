from r2r.bpy_handlers.ShaderHandler import ShaderHandler
from r2r.bpy_handlers.SceneHandler import SceneHandler
from r2r.bpy_handlers.MaterialHandler import MaterialHandler
from r2r.bpy_handlers.ObjectHandler import ObjectHandler
from r2r.bpy_handlers.RenderHandler import RenderHandler
from r2r.bpy_handlers.CameraHandler import CameraHandler

class BpyContext:
    def __init__(self):
        import bpy
        self.bpy = bpy
        self.scene_handler = SceneHandler(bpy=self.bpy)
        self.shader_handler = ShaderHandler(bpy=self.bpy)
        self.object_handler = ObjectHandler(bpy=self.bpy)
        self.render_handler = RenderHandler(bpy=self.bpy)
        self.camera_handler = CameraHandler(bpy=self.bpy)
        self.material_handler = MaterialHandler(bpy=self.bpy)

    def initialize_scene(self):
        self.scene_handler.delete_all_objects_in_scene()
