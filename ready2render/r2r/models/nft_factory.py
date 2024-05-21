from r2r.models.kadcar import Kadcar
from r2r.models.nft import NFT
from r2r.bpy_handlers.BpyContext import BpyContext

def create_nft(data):
    nft = None
    bpy_context = BpyContext()

    if data["collection_name"] == "kadcars":
        nft = Kadcar(
            bpy_context=bpy_context,
            token_id=data["dest_token_id"], 
            nft_id=data["dest_nft_id"], 
            collection_id=data["dest_collection_id"], 
            collection_name=data["dest_collection_name"], 
            chain_id=data["chain_id"]
        )
    else:
        nft = NFT(
            bpy_context=bpy_context,
            token_id=data["dest_token_id"], 
            nft_id=data["dest_nft_id"], 
            collection_id=data["dest_collection_id"], 
            collection_name=data["dest_collection_name"], 
            chain_id=data["chain_id"]
        )
    
    return nft