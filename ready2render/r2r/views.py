from django.http import HttpResponse
from rest_framework import views
from multiprocessing import Pool
import time

from r2r.models.nft_factory import create_nft
from r2r.models.nft import NFT
from r2r.utils.io_utils import *
from r2r.bpy_handlers.BpyContext import BpyContext
from r2r.models.digital_ocean import DigitalOcean
from r2r.ipfs_utils.ipfs_utils import upload_asset_to_ipfs
from config import RENDER_OUTPUT_PATH, BLENDER_EXPORT_PATH
from kad_py.main.kad_py_public import pact_build_and_fetch_local
from kad_py.main.kad_py_pvt import get_api_url


class CombineView(views.APIView):
    def post(self, request):
        data = request.data

        # initialize bpy and digital ocean contexts
        bpy = BpyContext()
        digital_ocean = DigitalOcean()

        # initialize nfts
        target_nft = create_nft(bpy_context=bpy, data=data["target_nft"])
        # attachment_nft = create_nft(bpy_context=bpy, data=data["attachment_nft"])

        # # attach nft and export
        # target_nft.attach_image_texture(attachment_nft)
        # target_nft.export_nft(file_path=BLENDER_EXPORT_PATH, format="GLB")

        # # render nft
        # bpy.render_handler.render_scene(
        #     render_output_path=RENDER_OUTPUT_PATH,
        #     output_format="",
        #     render_res_x=0,
        #     render_res_y=0,
        #     write_still=True
        # )

        # upload to ipfs and update metadata
        updated_tgt_metadata = target_nft.upload_nft_to_ipfs()

        # upload to digital ocean
        # digital_ocean.upload_to_spaces(target_nft.collection_name, updated_tgt_metadata, "public")

        return HttpResponse("DONE")
