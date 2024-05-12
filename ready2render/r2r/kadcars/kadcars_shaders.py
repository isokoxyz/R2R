from r2r.blender_ops.shaders import customize_world_shader_nodes

def add_hdri_to_scene(hdr_file_path, background_name):
    if background_name == 'storage':
        hdr_file_path = hdr_file_path + ".exr"
    else:
        hdr_file_path = hdr_file_path + ".hdr"

    customize_world_shader_nodes(hdr_file_path, background_name)