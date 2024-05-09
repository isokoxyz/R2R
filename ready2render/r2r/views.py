from django.shortcuts import render
from blender_ops.scene import import_scene_into_collection, deselect_all_scene_objects, \
    select_object_by_name_and_make_active, link_selected_objects_in_scene, make_object_active, \
    apply_transform_to_selected_object
from blender_ops.camera import set_scene_camera
from blender_ops.render import configure_render_settings, set_render_output_settings
from kad_py.main.kad_py_public import pact_build_and_fetch_local
from ipfs_utils.ipfs_utils import download_glb_asset
from config import SENDER, MAINNET_NETWORK_ID

class CombineView():
    
    def attach_nft(destination_nft_id, attachment_nft_id, chain_id):
        # get nft manifests from blockchain
        dest_nft_manifest = pact_build_and_fetch_local(
            sender=SENDER, 
            pact_code='(marmalade-v2.ledger.get-token-info "{}")'.format(destination_nft_id), 
            network_id=MAINNET_NETWORK_ID, 
            chain_id=chain_id
        )
        attachment_nft_manifest = pact_build_and_fetch_local(
            sender=SENDER, 
            pact_code='(marmalade-v2.ledger.get-token-info "{}")'.format(destination_nft_id), 
            network_id=MAINNET_NETWORK_ID, 
            chain_id=chain_id
        )

        # download glbs
        dest_nft_glb = download_glb_asset("")
        attachment_nft_glb = download_glb_asset("")

        # clear scene selection
        deselect_all_scene_objects()

        # import nft glbs into scene
        import_scene_into_collection(dest_nft_glb, "destination")
        import_scene_into_collection(attachment_nft_glb, "attachment")

        # select nft objects
        deselect_all_scene_objects()
        dest_object = select_object_by_name_and_make_active("")
        attachment_object = select_object_by_name_and_make_active("")

        # combine the nfts (uv map stuff)
        link_selected_objects_in_scene("")
        make_object_active(dest_object)
        dest_object.rotation_quaternion.x = 1.0


        # save and export glbs

        
        # update metadata from gltf


        # configure render settings
