from blender_ops.scene import *
from blender_ops.render import *
from blender_ops.shaders import *
from blender_ops.camera import *
from kadcars.kadcars_shaders import add_hdri_to_scene
from kad_py.main.kad_py_public import pact_build_and_fetch_local
from ipfs_utils.ipfs_utils import download_glb_asset
from config import SENDER, MAINNET_NETWORK_ID

class KadcarsUpgrades():
    def attach_nft(dest_object):
        permanent_node_names = ["Principled BSDF", "Material Output", "BAKED_TEXTURE"]

        #Retrieve bsdf values and node tree
        bsdf = get_principled_bsdf_for_active_material(dest_object)
        kadcar_color = get_input_value_from_bsdf(bsdf, 'Base Color')
        metallic_value = get_input_value_from_bsdf(bsdf, 'Metallic')
        node_tree = get_node_tree_for_selected_object(dest_object)
        nodes = node_tree.nodes

        #Create texture shader node for sticker
        texture_node = nodes.new("ShaderNodeTexImage")
        texture_node.image = bpy.data.images.load("") #TODO: load image
        texture_node.name = "STICKER_NODE"

        #Create UV map node to specify destination
        uv_node = nodes.new("ShaderNodeUVMap")
        uv_node.uv_map = "UVMap.002" #TODO: change hard-coded uv map location
        uv_node.name = "UV_MAP_NODE"

        #Create Mix RGB node to set kadcar color
        mix_node = nodes.new("ShaderNodeMixRGB")
        mix_node.inputs['Color1'].default_value = kadcar_color
        mix_node.name = "MIX_NODE"

        #Link all created nodes to the principled bsdf
        node_tree.links.new(uv_node.outputs['UV'], texture_node.inputs['Vector'])
        node_tree.links.new(texture_node.outputs['Color'], mix_node.inputs['Color2'])
        node_tree.links.new(texture_node.outputs['Alpha'], mix_node.inputs['Fac'])
        node_tree.links.new(mix_node.outputs['Color'], bsdf.inputs['Base Color'])

        #Baking begins here
        deselect_all_scene_objects()
        
        #Set up baking parameters
        bsdf.inputs['Metallic'].default_value = 0.0
        configure_bake_settings('CYCLES', 'CUDA', 'GPU', False, False, False, 'DIFFUSE')
        
        #Select the main uv map for the kadcar
        uv_layers = dest_object.data.uv_layers
        uv_layer_names = [uv.name for uv in uv_layers]
        for name in uv_layer_names:
            if name == "UVMap":
                uv_layers[name].active = True
                print(name)
                print(uv_layers[name])

        #Create a new texture image shader node for the baked texture destination
        image_name = "baked_texture_image"
        image = bpy.data.images.new(image_name, 4096, 4096)
        bake_texture_node = nodes.new("ShaderNodeTexImage")
        bake_texture_node.select = True
        bake_texture_node.name = "BAKED_TEXTURE"
        nodes.active = bake_texture_node
        bake_texture_node.image = image
        
        #Select the kadcar body and bake
        select_object_by_name_and_make_active('Car_Body')
        bpy.ops.object.bake('INVOKE_DEFAULT', type='DIFFUSE', pass_filter={'COLOR'}, save_mode='EXTERNAL', target='IMAGE_TEXTURES')

        #Remove old unneeded nodes
        for node in nodes:
            print(node.name)
            if node.name not in permanent_node_names:
                nodes.remove(node)
        
        #Link new baked texture shader node to the principled bsdf
        node_tree.links.new(bake_texture_node.outputs['Color'], bsdf.inputs['Base Color'])
        
        #Restore the metallic value of the car 
        set_input_value_in_bsdf(bsdf, 'Metallic', metallic_value)

        #Complete scene details and export
        glb_path = '' #TODO
        add_hdri_to_scene('storage')
        export_scene(glb_path, export_all=True, format="GLB")

        return glb_path
