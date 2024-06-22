import os
import requests
from config import SENDER, MAINNET_NETWORK_ID, RENDER_OUTPUT_PATH, BLENDER_EXPORT_PATH, IPFS_DOWNLOAD_PATH

from r2r.ipfs_utils.ipfs_utils import upload_nft_files_to_ipfs
from r2r.bpy_handlers.BpyContext import BpyContext
from r2r.models.asset import Asset
from kad_py.main.kad_py_public import pact_build_and_fetch_local


class NFT(Asset):
    def __init__(
        self,
        bpy_context: BpyContext,
        token_id: str,
        nft_id: str,
        collection_id: str,
        collection_name: str,
        chain_id: str,
        uri: str
    ):
        super().__init__(bpy_context)
        self.token_id = token_id
        self.nft_id = nft_id
        self.collection_id = collection_id
        self.collection_name = collection_name
        self.chain_id = chain_id
        self.uri = uri
        self.metadata = None

    def fetch_nft_metadata(self, uri):
        nft_metadata = None

        try:
            nft_metadata = requests.get(uri).json()
        except requests.exceptions.RequestException as e:
            raise e

        return nft_metadata

    def fetch_nft_data_from_blockchain(self):
        try:
            nft_metadata = pact_build_and_fetch_local(
                sender=SENDER,
                pact_code='(marmalade-v2.ledger.get-token-info "{}")'.format(self.token_id),
                network_id=MAINNET_NETWORK_ID,
                chain_id=self.chain_id
            )

            self.metadata = nft_metadata

            return nft_metadata
        except Exception as e:
            print("Error fetching data from blockchain")
            return e

    def upload_nft_to_ipfs(self):
        pass

    def attach_image_nft(self):
        pass

    def export_nft(self, file_path, format="GLB"):
        print("EXPORTING NOW")
        self.bpy_context.scene_handler.export_scene(file_path, export_all=True, format=format)

    def get_asset_render_format(self):
        pass

    def get_asset_render_aspect_ratio(self):
        pass

    # Path getters
    def get_nft_export_file_path(self, dir_name):
        return '{}/{}/{}_{}'.format(BLENDER_EXPORT_PATH, dir_name, str(self.collection_name), str(self.nft_id))
    
    def get_asset_ipfs_cid(self):
        pass

    def get_asset_ipfs_file_name(self):
        pass

    def get_asset_glb_path(self):
        pass
    
    def get_asset_render_path(self):
        pass

    def get_asset_ipfs_download_dir_name(self, dir_name=""):
        self.make_directory(f"{IPFS_DOWNLOAD_PATH}/{dir_name}")
        return dir_name
    
    def get_asset_export_dir_name(self, dir_name=""):
        self.make_directory(f"{BLENDER_EXPORT_PATH}/{dir_name}")
        return dir_name

    def get_asset_render_dir_name(self, dir_name=""):
        self.make_directory(f"{RENDER_OUTPUT_PATH}/{dir_name}")
        return dir_name
    
    def make_directory(self, dir_full_path):
        if not os.path.isdir(dir_full_path):
            os.mkdir(dir_full_path)
    