import requests
import time
from ready2render.r2r.utils.io_utils import *
from kad_py.main.kad_py_public import *
from kad_py.commands.env_data import EnvData
from kad_py.commands.capability import Capability
from kad_py.commands.signer import Signer
from ready2render.config import SENDER, DEFAULT_GAS_LIMIT, DEFAULT_GAS_PRICE, MAINNET_NETWORK_ID
from ready2render.r2r.models.digital_ocean import DigitalOcean

def run_r2r_upgrade():
    timing = str(time.time())
    blueprint_hash = str(hash(timing + "t:ExXnE3JpmRKRRyVwIcjY8GakAEGTqNzydrSx-0NdV50"))
    pact_code = f'(n_f1c962776331c4773136dc1587a8355c9957eae1.upgrades.perform-upgrade "{blueprint_hash}" "{SENDER}")'
    body = {
        "target-token-id": "t:ExXnE3JpmRKRRyVwIcjY8GakAEGTqNzydrSx-0NdV50",
        "target-nft-name": "Kadcars NFT #4990",
        "target-nft-uri": "https://kadcars-nft-metadata.nyc3.digitaloceanspaces.com/4990.json",
        "target-collection-id": "collection:4feG01EViLC9bR5gA-mBEFF-TEAKs12h-9tPnDVJ5qI",
        "target-collection-name": "kadcars-nft-metadata",
        "target-collection-standard": "marmalade-v2",
        "attachment-token-id": "t:hGgcj7Y1p8VnPk4GqdZgGMKqMbcqyOOW2Zzhm-sPvK4",
        "attachment-nft-name": "test_sticker",
        "attachment-nft-uri": "https://isoko-testing.nyc3.cdn.digitaloceanspaces.com/barb.jpeg",
        "attachment-collection-id": "collection:Ufj5r2bYxa6OX4xnXFalmZXdc_NEjs4Vi0PVdMD6_uw",
        "attachment-collection-name": "kadcars-stickers",
        "attachment-collection-standard": "marmalade-v2",
        "target-location": "UVMap.002",
        "chain-id": "8"
    }
    blueprint_data = {
        "target_nft": {
            "nft_type": "kadcar",
            "token_id": body["target-token-id"],
            "nft_id": body["target-nft-name"],
            "collection_id": body["target-collection-id"],
            "collection_name": body["target-collection-name"],
            "chain_id": body["chain-id"],
            "nft_uri":body["target-nft-uri"]
        },
        "attachment_nft": {
            "nft_type": "image",
            "token_id": body["attachment-token-id"],
            "nft_id": body["attachment-nft-name"],
            "collection_id": body["attachment-collection-id"],
            "collection_name": body["attachment-collection-name"],
            "chain_id": body["chain-id"],
            "nft_uri": body["attachment-nft-uri"],
            "uv_map": "UVMap.002"
        },
        "chain_id": "8"
    }
    print(blueprint_data)

    env_data = EnvData(data=body)
    requests.post("http://127.0.0.1:8000/r2r/combine_nfts/", {
            "request_key": "",
            "chain_id": "8",
            "owner": SENDER,
            "sender": SENDER,
            "blueprint_hash": blueprint_hash,
            "env_data": json.dumps(body),
            "blueprint": json.dumps(blueprint_data),
            "action": "attach"
        })
    exit()

    caps = [
        Capability("gas", "GAS", "coin.GAS", []),
        Capability("lock", "lock", "n_f1c962776331c4773136dc1587a8355c9957eae1.upgrades.LOCK", [f"{SENDER}"])
    ]

    exec_response = execute_exec_cmd(
        sender=SENDER,
        code=pact_code,
        chain_id="8",
        gas_price=DEFAULT_GAS_PRICE * 2,
        gas_limit=DEFAULT_GAS_LIMIT,
        signers=[SENDER],
        env_data=env_data,
        caps=caps,
        ttl=600,
        network_id=MAINNET_NETWORK_ID,
        nonce="1234",
        sign_method=CLI
    )
    print("--------------------------------------------")
    print("exec response")
    print(exec_response)
    print("--------------------------------------------")

    if "requestKeys" in exec_response:
        res = requests.post("http://127.0.0.1:8000/r2r/combine_nfts/", {
            "request_key": exec_response["requestKeys"][0],
            "chain_id": "8",
            "owner": SENDER,
            "sender": SENDER,
            "blueprint_hash": blueprint_hash,
            "env_data": json.dumps(body),
            "blueprint": json.dumps(blueprint_data),
            "action": "attach"
        })

run_r2r_upgrade()