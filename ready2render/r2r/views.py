from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import views
from multiprocessing import Pool
# from r2r.blender_ops.scene import *
# from r2r.blender_ops.render import *
# from r2r.blender_ops.shaders import *
# from r2r.blender_ops.camera import *
# from r2r.kadcars.kadcars_shaders import add_hdri_to_scene
# from r2r.ipfs_utils.ipfs_utils import download_glb_asset
# from r2r.nft import NFT
from r2r.utils.io_utils import *
# from kad_py.main.kad_py_public import pact_build_and_fetch_local
from config import SENDER, MAINNET_NETWORK_ID
import time

def test_function(file):
    import bpy
    time_start = time.time()
    collection_name = "lol"
    bpy.ops.object.select_all(action='DESELECT')
    if collection_name in bpy.data.collections:
        if bpy.data.collections[collection_name] is not bpy.context.scene.collection:
            bpy.data.collections.remove(bpy.data.collections[collection_name])
    # bpy.ops.import_scene.gltf(filepath='C:/Users/Mohannad Ahmad\Desktop\AppDev\Crypto\Kadena\Kadcars\R2R/ready2render/r2r\kadcars\kadcar.glb')
    bpy.ops.import_scene.gltf(filepath='/Users/mohannadahmad/Desktop/AppDev/Kadena/R2R/ready2render/r2r/kadcars/nft_5337.glb')
    bpy.ops.collection.create(name=collection_name)
    bpy.ops.object.select_all(action='SELECT')
    # bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.export_scene.gltf(
        filepath="/Users/mohannadahmad/Desktop/AppDev/Kadena/R2R/ready2render/r2r/kadcars/{}.glb".format(file),
        use_selection=True,
        export_format="GLB",
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
    print((time.time() - time_start))

class CombineView(views.APIView):
    def post(self, request):
        with Pool(2) as p:
            p.map(test_function, ["lol1", "lol2"])
        return HttpResponse("okokoko")
        delete_all_objects_in_scene()
        data = request.data
        destination_nft = NFT(
            token_id=data["dest_token_id"], 
            nft_id=data["dest_nft_id"], 
            collection_id=data["dest_collection_id"],
            collection_name=data["dest_collection_name"],
            chain_id=data["chain_id"]
        )
        # get nft manifests from blockchain
        # print("FETCHING NFT DATA")
        # dest_nft_metadata = pact_build_and_fetch_local(
        #     sender=SENDER, 
        #     pact_code='(marmalade-v2.ledger.get-token-info "{}")'.format(data["dest_nft_id"]), 
        #     network_id=MAINNET_NETWORK_ID, 
        #     chain_id=destination_nft.chain_id
        # )

        # attachment_nft_metadata = pact_build_and_fetch_local(
        #     sender=SENDER, 
        #     pact_code='(marmalade-v2.ledger.get-token-info "{}")'.format(attachment_nft_id), 
        #     network_id=MAINNET_NETWORK_ID, 
        #     chain_id=chain_id
        # )

        # download glbs
        # dest_nft_glb = download_glb_asset("") #TODO: nft asset
        # attachment_nft_image = download_glb_asset("") #TODO: nft asset
        dest_nft_glb = 'C:/Users/Mohannad Ahmad\Desktop\AppDev\Crypto\Kadena\Kadcars\R2R/ready2render/r2r\kadcars\kadcar.glb'
        attachment_nft_image = 'C:/Users/Mohannad Ahmad\Desktop\AppDev\Crypto\Kadena\Kadcars\R2R/ready2render/r2r\kadcars\sticker.jpg'

        # clear scene selection
        deselect_all_scene_objects()

        # import nft glbs into scene
        import_scene_into_collection(dest_nft_glb, "destination")
        # import_scene_into_collection(attachment_nft_image, "attachment")

        # select nft objects
        deselect_all_scene_objects()
        dest_object = select_object_by_name_and_make_active("Car_Body") #TODO: add object name
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

        # link object data
        # link_selected_objects_in_scene("OBDATA")

        #fix kadcar rotation
        make_object_active(dest_object)
        dest_object.rotation_quaternion.x = 1.0
        apply_transform_to_selected_object(dest_object, location=True, rotation=True)
        deselect_all_scene_objects()

        #Retrieve bsdf values and node tree
        print("SETTING UP SHADER NODES")
        bsdf = get_principled_bsdf_for_active_material(dest_object)
        base_color = get_input_value_from_bsdf(bsdf, 'Base Color')
        metallic_value = get_input_value_from_bsdf(bsdf, 'Metallic')
        node_tree = get_node_tree_for_selected_object(dest_object)
        nodes = node_tree.nodes

        #Create texture shader node for sticker
        texture_node = nodes.new("ShaderNodeTexImage")
        texture_node.image = bpy.data.images.load(attachment_nft_image) #TODO: load image
        texture_node.name = "STICKER_NODE"

        #Create UV map node to specify destination
        uv_node = nodes.new("ShaderNodeUVMap")
        uv_node.uv_map = "UVMap.002" #TODO: change hard-coded uv map location
        uv_node.name = "UV_MAP_NODE"

        #Create Mix RGB node to set kadcar color
        mix_node = nodes.new("ShaderNodeMixRGB")
        mix_node.inputs['Color1'].default_value = base_color
        mix_node.name = "MIX_NODE"

        #Link all created nodes to the principled bsdf
        print("CONNECTING ALL SHADER NODES")
        node_tree.links.new(uv_node.outputs['UV'], texture_node.inputs['Vector'])
        node_tree.links.new(texture_node.outputs['Color'], mix_node.inputs['Color2'])
        node_tree.links.new(texture_node.outputs['Alpha'], mix_node.inputs['Fac'])
        node_tree.links.new(mix_node.outputs['Color'], bsdf.inputs['Base Color'])

        #Baking begins here
        # permanent_node_names = ["Principled BSDF", "Material Output", "BAKED_TEXTURE"]
        # deselect_all_scene_objects()
        
        #Set up baking parameters
        # bsdf.inputs['Metallic'].default_value = 0.0
        # configure_bake_settings('CYCLES', 'CUDA', 'GPU', False, False, False, 'DIFFUSE')
        
        #Select the main uv map for the kadcar
        # uv_layers = dest_object.data.uv_layers
        # uv_layer_names = [uv.name for uv in uv_layers]
        # for name in uv_layer_names:
        #     if name == "UVMap":
        #         uv_layers[name].active = True
        #         print(name)
        #         print(uv_layers[name])

        #Create a new texture image shader node for the baked texture destination
        # image_name = "baked_texture_image"
        # image = bpy.data.images.new(image_name, 4096, 4096)
        # bake_texture_node = nodes.new("ShaderNodeTexImage")
        # bake_texture_node.select = True
        # bake_texture_node.name = "BAKED_TEXTURE"
        # nodes.active = bake_texture_node
        # bake_texture_node.image = image
        
        # #Select the kadcar body and bake
        # select_object_by_name_and_make_active('Car_Body')
        # bpy.ops.object.bake('INVOKE_DEFAULT', type='DIFFUSE', pass_filter={'COLOR'}, save_mode='EXTERNAL', target='IMAGE_TEXTURES')

        # #Remove old unneeded nodes
        # for node in nodes:
        #     print(node.name)
        #     if node.name not in permanent_node_names:
        #         nodes.remove(node)
        
        # #Link new baked texture shader node to the principled bsdf
        # node_tree.links.new(bake_texture_node.outputs['Color'], bsdf.inputs['Base Color'])
        
        #Restore the metallic value of the car 
        # set_input_value_in_bsdf(bsdf, 'Metallic', metallic_value)

        #Complete scene details and export
        print("EXPORTING NOW")
        glb_path = 'K:/stickered.glb' #TODO
        
        export_scene(glb_path, export_all=True, format="GLB")

        return glb_path
