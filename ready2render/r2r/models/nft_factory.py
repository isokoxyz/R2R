from r2r.models.kadcar import Kadcar
from r2r.models.image import Image
from r2r.models.nft import NFT


def create_nft(bpy_context, data):
    nft = None
    nft_type = data["nft_type"]

    if nft_type == "kadcar":
        nft = Kadcar(
            bpy_context=bpy_context,
            token_id=data["token_id"],
            nft_id=data["nft_id"],
            collection_id=data["collection_id"],
            collection_name=data["collection_name"],
            chain_id=data["chain_id"],
            uri=data["nft_uri"]
        )
    elif nft_type == "image":
        nft = Image(
            bpy_context=bpy_context,
            token_id=data["token_id"],
            nft_id=data["nft_id"],
            collection_id=data["collection_id"],
            collection_name=data["collection_name"],
            chain_id=data["chain_id"],
            uri=data["nft_uri"],
            uv_map=data["uv_map"]
        )
    else:
        nft = NFT(
            bpy_context=bpy_context,
            token_id=data["token_id"],
            nft_id=data["nft_id"],
            collection_id=data["collection_id"],
            collection_name=data["collection_name"],
            chain_id=data["chain_id"],
            uri=data["nft_uri"]
        )

    return nft
