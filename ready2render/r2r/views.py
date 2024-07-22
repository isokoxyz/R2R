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
from kad_py.main.kad_py_public import pact_build_and_fetch_local, execute_cont_cmd, pact_fetch_local
from kad_py.main.kad_py_pvt import get_api_url
from kad_py.config.constants import DEFAULT_GAS_PRICE, DEFAULT_GAS_LIMIT, MAINNET_NETWORK_ID, CLI
from kad_py.commands.env_data import EnvData
from kad_py.commands.capability import Capability


class CombineView(views.APIView):
    def post(self, request):
        """
        This endpoint performs the upgrade process on a 3D model, 
        renders the result and updates the metadata
        """
        data = request.data

        # initialize bpy and digital ocean contexts
        bpy = BpyContext()
        digital_ocean = DigitalOcean()
        poll = Poll(DEFAULT_SENDER, data["chain_id"])
        
        # poll exec step of defpact
        # tx_result = poll.poll_request_key(data["request_key"])
        # if tx_result == None or tx_result == "failure":
        #     return HttpResponse(404)

        # fetch local blueprint
        # pact_code = "(n_f1c962776331c4773136dc1587a8355c9957eae1.upgrades.get-blueprint \"" + data["blueprint_hash"] + "\")"
        # upgrade_blueprint = pact_build_and_fetch_local(data["sender"], pact_code, MAINNET_NETWORK_ID, data["chain_id"])
        # print(upgrade_blueprint)
        
        # initialize nfts
        target_nft = create_nft(bpy_context=bpy, data=json.loads(data["blueprint"])["target_nft"])
        attachment_nft = create_nft(bpy_context=bpy, data=json.loads(data["blueprint"])["attachment_nft"])

        # attach nft and export
        if data["action"] == "attach":
            target_nft.attach_image_texture(attachment_nft)
        elif data["action"] == "remove":
            target_nft.remove_image_texture(attachment_nft.token_id)
        
        target_nft.export_nft(file_path=target_nft.get_asset_glb_path(), format="GLB")

        # render nft
        print("RENDERING SCENE NOW")
        bpy.render_handler.render_scene(
            render_output_path=target_nft.get_asset_render_path(),
            output_format=target_nft.get_asset_render_format(),
            render_res_x=target_nft.get_asset_render_aspect_ratio()["res_x"],
            render_res_y=target_nft.get_asset_render_aspect_ratio()["res_y"],
            write_still=True
        )
        target_nft.set_kadcar_image_uri(target_nft.get_asset_s3_uri())
        digital_ocean.upload_file(
            target_nft.get_asset_render_path(), 
            target_nft.get_s3_render_bucket_name(), 
            target_nft.get_nft_render_file_name(),
            "public-read",
            "image/webp"
        )

        # upload to ipfs and update metadata
        # updated_tgt_metadata = target_nft.upload_nft_to_ipfs()

        # upload to digital ocean
        digital_ocean.upload_to_spaces(
            target_nft.get_s3_md_bucket_name(), 
            json.dumps(target_nft.metadata), 
            target_nft.get_nft_name() + ".json", 
            "public-read-write",
            "application/json"
        )
        print(target_nft.get_s3_md_bucket_name())
        print(target_nft.get_md_s3_uri())
        print(json.dumps(target_nft.metadata))

        # complete the defpact and upgrade
        caps = [
            Capability("gas", "GAS", "coin.GAS", []),
            Capability("unlock", "UNLOCK", "n_f1c962776331c4773136dc1587a8355c9957eae1.upgrades.UNLOCK", [f"{data['owner']}"])
        ]

        cont_res="DONE"
        # cont_res = execute_cont_cmd(
        #     sender=data["owner"],
        #     chain_id=data["chain_id"],
        #     gas_price=DEFAULT_GAS_PRICE,
        #     gas_limit=DEFAULT_GAS_LIMIT,
        #     ttl=600,
        #     network_id=MAINNET_NETWORK_ID,
        #     step=1,
        #     rollback=False,
        #     env_data=EnvData(data=data["env_data"]),
        #     pact_tx_hash=data["request_key"],
        #     sign_method=CLI,
        #     signers=[data["owner"]],
        #     caps=caps,
        #     proof=None
        # )

        # print("--------------------------------------------")
        # print("cont response")
        # print(cont_res)
        

        return HttpResponse(cont_res)
