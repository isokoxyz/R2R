import requests
from config import SENDER, MAINNET_NETWORK_ID

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
        chain_id: str
    ):
        super().__init__(bpy_context)
        self.token_id = token_id
        self.nft_id = nft_id
        self.collection_id = collection_id
        self.collection_name = collection_name
        self.chain_id = chain_id

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
                pact_code='(marmalade-v2.ledger.get-token-info "{}")'.format(self.nft_id),
                network_id=MAINNET_NETWORK_ID,
                chain_id=self.chain_id
            )
        except Exception as e:
            print("Error fetching data from blockchain")
            return e

        return nft_metadata

    def attach_image_nft(self):
        pass

    def export_nft(self, file_path, format="GLB"):
        print("EXPORTING NOW")
        self.bpy_context.scene_handler.export_scene(
            file_path, export_all=True, format=format)
