
class RenderHandler:
    """
    This class contains helper functions to set up and execute the render functionality 
    in the Blender scene
    """
    def __init__(
        self,
        bpy,
        engine: str = 'CYCLES',
        # device_type: str = 'CUDA',
        device_type: str = 'METAL',
        device: str = 'GPU',
        resolution_percentage: int = 200,
        samples: int = 50
    ):
        self.bpy = bpy
        self.engine = engine
        self.device_type = device_type
        self.device = device
        self.resolution_percentage = resolution_percentage
        self.samples = samples

    def render_scene(self, render_output_path, output_format, render_res_x, render_res_y, write_still=True):
        """
        This function renders the current blender scene with the specified format and resolution
        """
        self.configure_render_settings(self.engine, self.device_type, self.device, self.resolution_percentage, self.samples)
        # self.bpy.scene.render.filepath = "K:/" # Set save path for images
        self.bpy.context.scene.render.filepath = render_output_path  # Set save path for images
        # Set image file format
        self.bpy.context.scene.render.image_settings.file_format = output_format

        self.bpy.context.scene.render.resolution_x = render_res_x
        self.bpy.context.scene.render.resolution_y = render_res_y

        self.bpy.ops.render.render(write_still=write_still)

    def configure_render_settings(self, engine, device_type, device, resolution_percentage, samples):
        """
        This function is used to configure the blender render settings
        """
        self.bpy.data.scenes[0].render.engine = engine
        self.bpy.data.scenes[0].render.resolution_percentage = resolution_percentage
        self.bpy.data.scenes[0].cycles.samples = samples

        # Set the device_type
        self.bpy.context.preferences.addons["cycles"].preferences.compute_device_type = device_type

        # Set the device and feature set
        self.bpy.context.scene.cycles.device = device

        # get_devices(self, ) to let Blender detects GPU device
        self.bpy.context.preferences.addons["cycles"].preferences.get_devices(self, )
        print(self,
              self.bpy.context.preferences.addons["cycles"].preferences.compute_device_type)

        for d in self.bpy.context.preferences.addons["cycles"].preferences.devices:
            d["use"] = 0
            if d["name"][:6] == 'NVIDIA':
                d["use"] = 1
            print(self, d["name"], d["use"])

    #     self.bpy.scene.render.engine = engine
    #     self.bpy.scene.cycles.device = device

    #     for scene in self.bpydata.scenes:
    #         print(self, scene.name)
    #         scene.cycles.device = device
    #         scene.render.resolution_percentage = resolution_percentage
    #         scene.cycles.samples = samples

    def configure_bake_settings(self, engine, device_type, device, use_pass_direct, use_pass_indirect, use_selected_to_active, bake_type):
        """
        This function configures the settings for the blender baking procedure
        """
        self.configure_render_settings(
            self, engine, device_type, device, 200, 1000)

        self.bpy.context.scene.render.bake.use_pass_direct = use_pass_direct
        self.bpy.context.scene.render.bake.use_pass_indirect = use_pass_indirect
        self.bpy.context.scene.render.bake.use_selected_to_active = use_selected_to_active
        self.bpy.context.scene.cycles.bake_type = bake_type

    def configure_render_operation_and_render(self, ):
        self.bpy.ops.render.render(self, write_still=True)
