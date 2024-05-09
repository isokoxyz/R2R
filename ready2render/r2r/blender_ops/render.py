import bpy

def set_render_output_settings(render_output_path, output_format, render_res_x, render_res_y, write_still=True):
    # bpy.context.scene.render.filepath = "K:/" # Set save path for images
    bpy.context.scene.render.filepath = render_output_path # Set save path for images
    bpy.context.scene.render.image_settings.file_format = output_format # Set image file format
    
    bpy.context.scene.render.resolution_x = render_res_x
    bpy.context.scene.render.resolution_y = render_res_y
    
    bpy.ops.render.render(write_still=write_still)

def configure_render_settings(engine, device_type, device, resolution_percentage, samples):
    bpy.data.scenes[0].render.engine = engine
    bpy.data.scenes[0].render.resolution_percentage = resolution_percentage
    bpy.data.scenes[0].cycles.samples = samples

    # Set the device_type
    bpy.context.preferences.addons["cycles"].preferences.compute_device_type = device_type
    
    # Set the device and feature set
    bpy.context.scene.cycles.device = device
    
    # get_devices() to let Blender detects GPU device
    bpy.context.preferences.addons["cycles"].preferences.get_devices()
    print(bpy.context.preferences.addons["cycles"].preferences.compute_device_type)

    for d in bpy.context.preferences.addons["cycles"].preferences.devices:
        d["use"] = 0
        if d["name"][:6] == 'NVIDIA':
            d["use"] = 1
        print(d["name"], d["use"])

#     bpy.context.scene.render.engine = engine
#     bpy.context.scene.cycles.device = device

#     for scene in bpy.data.scenes:
#         print(scene.name)
#         scene.cycles.device = device
#         scene.render.resolution_percentage = resolution_percentage
#         scene.cycles.samples = samples

def configure_bake_settings(engine, device_type, device, use_pass_direct, use_pass_indirect, use_selected_to_active, bake_type):
    configure_render_settings(engine, device_type, device, 200, 1000)

    bpy.context.scene.render.bake.use_pass_direct = use_pass_direct
    bpy.context.scene.render.bake.use_pass_indirect = use_pass_indirect
    bpy.context.scene.render.bake.use_selected_to_active = use_selected_to_active
    bpy.context.scene.cycles.bake_type = bake_type

def configure_render_operation_and_render():
    bpy.ops.render.render(write_still=True)