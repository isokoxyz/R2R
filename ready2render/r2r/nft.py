from asset import Asset

class NFT(Asset):
    def __init__(self, token_id, nft_id, collection_id, collection_name, chain_id):
        self.token_id = token_id
        self.nft_id = nft_id
        self.collection_id = collection_id
        self.collection_name = collection_name
        self.chain_id = chain_id