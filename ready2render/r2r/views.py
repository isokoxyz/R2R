from django.http import HttpResponse
from rest_framework import views
from multiprocessing import Pool
import time

from r2r.utils.poll import Poll
from r2r.models.nft_factory import create_nft
from r2r.models.nft import NFT
from r2r.utils.io_utils import *
from r2r.bpy_handlers.BpyContext import BpyContext
from r2r.models.digital_ocean import DigitalOcean
from r2r.ipfs_utils.ipfs_utils import upload_asset_to_ipfs
from config import RENDER_OUTPUT_PATH, BLENDER_EXPORT_PATH, DEFAULT_SENDER
from kad_py.main.kad_py_public import pact_build_and_fetch_local
from kad_py.main.kad_py_pvt import get_api_url


class CombineView(views.APIView):
    def post(self, request):
        data = request.data

        # initialize bpy and digital ocean contexts
        bpy = BpyContext()
        digital_ocean = DigitalOcean()
        poll = Poll(DEFAULT_SENDER, data["chain_id"])
        
        upgrade_blueprint = poll.poll_request_key(data["request_key"])
        if not upgrade_blueprint:
            return HttpResponse(404)

        # initialize nfts
        target_nft = create_nft(bpy_context=bpy, data=upgrade_blueprint["target_nft"])
        attachment_nft = create_nft(bpy_context=bpy, data=upgrade_blueprint["attachment_nft"])

        # attach nft and export
        target_nft.attach_image_texture(attachment_nft)
        target_nft.export_nft(file_path=target_nft.get_asset_glb_pawwwwth(), format="GLB")

        # render nft
        print("RENDERING SCENE NOW")
        bpy.render_handler.render_scene(
            render_output_path=target_nft.get_asset_render_path(),
            output_format=target_nft.get_asset_render_format(),
            render_res_x=target_nft.get_asset_render_aspect_ratio()["res_x"],
            render_res_y=target_nft.get_asset_render_aspect_ratio()["res_y"],
            write_still=True
        )

        # upload to ipfs and update metadata
        # updated_tgt_metadata = target_nft.upload_nft_to_ipfs()

        # upload to digital ocean
        # digital_ocean.upload_to_spaces(target_nft.collection_name, updated_tgt_metadata, "public")

        return HttpResponse("DONE")
