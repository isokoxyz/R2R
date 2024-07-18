import os
import requests
from config import SENDER, MAINNET_NETWORK_ID, RENDER_OUTPUT_PATH, BLENDER_EXPORT_PATH, IPFS_DOWNLOAD_PATH

from r2r.bpy_handlers.BpyContext import BpyContext
from r2r.models.asset import Asset
from kad_py.main.kad_py_public import pact_build_and_fetch_local


class NFT(Asset):
    """
    This class defines an NFT asset and handles interactions with them
    """
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
        """
        This function fetches the NFT's data by querying the uri it receives

        Returns:
            dict: json dict object containing the NFT's metadata
        """
        nft_metadata = None

        try:
            nft_metadata = requests.get(uri).json()
        except requests.exceptions.RequestException as e:
            raise e

        return nft_metadata

    def fetch_nft_data_from_blockchain(self):
        """
        This function fetches the NFT's token info from the blockchain
        
        Returns:
            dict: json dict object containing the NFT's token info
        """
        try:
            nft_metadata = pact_build_and_fetch_local(
                sender=SENDER,
                pact_code='(marmalade-v2.ledger.get-token-info "{}")'.format(self.token_id),
                network_id=MAINNET_NETWORK_ID,
                chain_id=self.chain_id
            )
            print(nft_metadata)
            self.metadata = nft_metadata

            return nft_metadata
        except Exception as e:
            print("Error fetching data from blockchain")
            return e

    def upload_nft_to_ipfs(self):
        """
        This function uploads the NFT asset to IPFS
        """
        pass

    def attach_image_nft(self):
        """
        This function handles attaching an image NFT to this NFT
        """
        pass

    def export_nft(self, file_path, format="GLB"):
        """
        This function exports the NFT in the given format
        """
        print("EXPORTING NOW")
        self.bpy_context.scene_handler.export_scene(file_path, export_all=True, format=format)

    def get_nft_name(self):
        """
        This function returns the NFT's name
        """
        pass

    def get_nft_render_file_name(self):
        """
        This function returns the name of the render file
        """
        pass

    def get_asset_render_format(self):
        """
        This function handles rendering the NFT asset in blender
        """
        pass

    def get_asset_render_aspect_ratio(self):
        """
        This function gets the aspect ratio for the rendered asset
        """
        pass

    def get_s3_md_bucket_name(self):
        """
        This function gets the name of the Kadcar NFT's metadata bucket name

        Returns:
            string: name of the S3 bucket
        """
        pass
    
    def get_s3_render_bucket_name(self):
        """
        This function gets the name of the Kadcar NFT's render bucket name

        Returns:
            string: name of the S3 bucket
        """
        pass

    def get_asset_s3_uri(self):
        """
        This function gets the digital ocean URL for the NFT render
        """
        pass

    def get_md_s3_uri(self):
        """
        This function gets the digital ocean URL for the NFT metadata
        """
        pass

    # Path getters
    def get_nft_export_file_path(self, dir_name):
        """
        This function gets the destination file path for exported NFTs
        """
        return '{}/{}/{}_{}'.format(BLENDER_EXPORT_PATH, dir_name, str(self.collection_name), str(self.nft_id))
    
    def get_asset_ipfs_cid(self):
        """
        This function gets the NFTs CID on IPFS
        """
        pass

    def get_asset_ipfs_file_name(self):
        """
        This function gets the NFTs file name on IPFS
        """
        pass

    def get_asset_glb_path(self):
        """
        This function gets the NFT asset's GLB path
        """
        pass
    
    def get_asset_render_path(self):
        """
        This function gets the path where the NFT render file will be saved
        """
        pass

    def get_asset_ipfs_download_dir_name(self, dir_name=""):
        """
        This function gets the file path where the IPFS asset gets downloaded
        """
        self.make_directory(f"{IPFS_DOWNLOAD_PATH}/{dir_name}")
        return dir_name
    
    def get_asset_export_dir_name(self, dir_name=""):
        """
        This function gets the directory where assets get exported
        """
        self.make_directory(f"{BLENDER_EXPORT_PATH}/{dir_name}")
        return dir_name

    def get_asset_render_dir_name(self, dir_name=""):
        """
        This function gets the directory where the NFT asset render is saved
        """
        self.make_directory(f"{RENDER_OUTPUT_PATH}/{dir_name}")
        return dir_name
    
    def make_directory(self, dir_full_path):
        """
        This function creates a directory at the specified location
        """
        if not os.path.isdir(dir_full_path):
            os.mkdir(dir_full_path)