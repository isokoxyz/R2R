from django.http import HttpResponse
from rest_framework import views
from multiprocessing import Pool
import time

from r2r.models.nft_factory import create_nft
from r2r.models.nft import NFT
from r2r.utils.io_utils import *
from r2r.bpy_handlers.BpyContext import BpyContext
from r2r.models.digital_ocean import DigitalOcean


def test_function(file):
    bpy = BpyContext().bpy

    time_start = time.time()
    collection_name = "lol"
    bpy.ops.object.select_all(action='DESELECT')
    if collection_name in bpy.data.collections:
        if bpy.data.collections[collection_name] is not bpy.context.scene.collection:
            bpy.data.collections.remove(bpy.data.collections[collection_name])
    bpy.ops.import_scene.gltf(
        filepath='C:/Users/Mohannad Ahmad\Desktop\AppDev\Crypto\Kadena\Kadcars\R2R/ready2render/r2r\kadcars\kadcar.glb')
    # bpy.ops.import_scene.gltf(
    #     filepath='/Users/mohannadahmad/Desktop/AppDev/Kadena/R2R/ready2render/r2r/kadcars/nft_5337.glb')
    bpy.ops.collection.create(name=collection_name)
    bpy.ops.object.select_all(action='SELECT')
    # bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.export_scene.gltf(
        # filepath="/Users/mohannadahmad/Desktop/AppDev/Kadena/R2R/ready2render/r2r/kadcars/{}.glb".format(
        filepath="C:/Users/Mohannad Ahmad\Desktop\AppDev\Crypto\Kadena\Kadcars\R2R/ready2render/r2r\kadcars\{}.glb".format(
            file),
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
        data = request.data

        # initialize bpy and digital ocean contexts
        bpy = BpyContext()
        digital_ocean = DigitalOcean()

        # initialize nfts
        target_nft = create_nft(bpy_context=bpy, data=data["target_nft"])
        attachment_nft = create_nft(
            bpy_context=bpy, data=data["attachment_nft"])

        # attach nft and export
        target_nft.attach_image_texture(attachment_nft)
        target_nft.export_nft(file_path="", format="GLB")

        # render nft
        bpy.render_handler.render_scene(
            render_output_path="", 
            output_format="", 
            render_res_x=0, 
            render_res_y=0, 
            write_still=True
        )

        # upload to ipfs

        # upload to digital ocean
        digital_ocean.upload_to_spaces()

        # download glbs
        # dest_nft_glb = download_glb_asset("") #TODO: nft asset
        # attachment_nft_image = download_glb_asset("") #TODO: nft asset

        uvs = 'C:/Users/Mohannad Ahmad\Desktop\AppDev\Crypto\Kadena\Kadcars\R2R/ready2render/r2r\kadcars/kadcar_w_uvs.glb'
        dest_nft_glb = 'C:/Users/Mohannad Ahmad\Desktop\AppDev\Crypto\Kadena\Kadcars\R2R/ready2render/r2r\kadcars\kadcar.glb'
        attachment_nft_image = 'C:/Users/Mohannad Ahmad\Desktop\AppDev\Crypto\Kadena\Kadcars\R2R/ready2render/r2r\kadcars/army.png'

        # uvs = '/Users/mohannadahmad/Desktop/AppDev/Kadena/R2R/ready2render/r2r/kadcars/kadcar_w_uvs.glb'
        # dest_nft_glb = '/Users/mohannadahmad/Desktop/AppDev/Kadena/R2R/ready2render/r2r/kadcars/nft_5337.glb'
        # attachment_nft_image = '/Users/mohannadahmad/Desktop/AppDev/Kadena/R2R/ready2render/r2r/kadcars/hood.png'

        # import nft glbs into scene
        bpy.scene_handler.import_scene_into_collection(
            dest_nft_glb, "destination")
        bpy.scene_handler.import_scene_into_collection(uvs, "uvs")

        # cleanup
        bpy.scene_handler.deselect_all_scene_objects()

        # select target object
        dest_object = bpy.object_handler.select_object_by_name_and_make_active(
            "Car_Body")
        bpy.object_handler.set_object_origin(
            type='ORIGIN_GEOMETRY', center='MEDIAN')

        # select kadcars with object
        uvs_object = bpy.object_handler.select_object_by_name_and_make_active(
            "Car_Body.001")
        bpy.object_handler.set_object_origin(
            type='ORIGIN_GEOMETRY', center='MEDIAN')

        # link objects
        bpy.object_handler.link_selected_objects_in_scene(type='OBDATA')

        # Fix the rotation
        bpy.object_handler.make_object_active(uvs_object)
        # uvs_object.rotation_quaternion.x = 1.0
        # bpy.object_handler.apply_transform_to_selected_object(uvs_object, location=True, rotation=True)

        bpy.scene_handler.deselect_all_scene_objects()
        bpy.scene_handler.delete_objects_from_collection_name('uvs')

        # Retrieve bsdf values and node tree
        print("SETTING UP SHADER NODES")
        bsdf = bpy.shader_handler.get_principled_bsdf_for_active_material(
            dest_object)
        base_color = bpy.shader_handler.get_input_value_from_bsdf(
            bsdf, 'Base Color')
        metallic_value = bpy.shader_handler.get_input_value_from_bsdf(
            bsdf, 'Metallic')
        node_tree = bpy.shader_handler.get_node_tree_for_selected_object(
            dest_object)
        nodes = node_tree.nodes

        # Create UV map node to specify destination
        uv_node = nodes.new("ShaderNodeUVMap")
        # TODO: this will be the name of the actual uv which will be in the image metadata
        uv_node.uv_map = "UVMap.002"
        uv_node.name = "UV_MAP_NODE"

        # Create texture shader node for sticker
        texture_node = nodes.new("ShaderNodeTexImage")
        texture_node.image = bpy.bpy.data.images.load(
            attachment_nft_image)  # TODO: load image
        texture_node.name = "STICKER_NODE"

        # Create Mix RGB node to set kadcar color
        mix_node = nodes.new("ShaderNodeMixRGB")
        mix_node.inputs['Color1'].default_value = base_color
        mix_node.name = "MIX_NODE"

        # Link all created nodes to the principled bsdf
        print("CONNECTING ALL SHADER NODES")
        node_tree.links.new(
            uv_node.outputs['UV'], texture_node.inputs['Vector'])
        node_tree.links.new(
            texture_node.outputs['Color'], mix_node.inputs['Color2'])
        node_tree.links.new(
            texture_node.outputs['Alpha'], mix_node.inputs['Fac'])
        node_tree.links.new(
            mix_node.outputs['Color'], bsdf.inputs['Base Color'])

        bpy.shader_handler.set_input_value_in_bsdf(
            bsdf, 'Metallic', metallic_value)

        # Complete scene details and export
        print("EXPORTING NOW")
        glb_path = 'K:/stickered.glb'  # TODO
        # glb_path = '/Users/mohannadahmad/Desktop/AppDev/Kadena/R2R/ready2render/r2r/kadcars/stickered.glb'  # TODO

        bpy.scene_handler.export_scene(glb_path, export_all=True, format="GLB")

        return HttpResponse("DONE")
