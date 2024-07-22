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
# nft_metadata = pact_build_and_fetch_local(
#     sender="k:b9b798dd046eccd4d2c42c18445859c62c199a8d673b8c1bf7afcfca6a6a81e3",
#     pact_code='(marmalade-v2.ledger.get-token-info "t:ExXnE3JpmRKRRyVwIcjY8GakAEGTqNzydrSx-0NdV50")',
#     network_id="mainnet01",
#     chain_id="8"
# )
# print(nft_metadata)
# lol = {"hash": "fRTCG4fyAcg6kjRZuP9NJdffMqgIYCJ7mfl2BWD2H2I", "data": [{"hash": "AxGsPlvzfZTSKhJNR72_lUl61oZOdQJzQy8VAUjaJ5M", "uri": {"data": "mutable-state-data", "scheme": "pact:schema"}, "datum": {"components": [{"stats": [{"key": "body-type", "val": "K:2"}, {"key": "body-material", "val": {"id": "Glossy-Ultraviolet", "type": "material"}}, {"key": "trim-material", "val": {"id": "Carbon Fiber", "type": "texture"}}, {"key": "hood-trim-material", "val": {"id": "matte metallic-darkgray", "type": "material"}}, {"key": "grill-inner-material", "val": {"id": "matte-black", "type": "material"}}, {"key": "grill-outer-material", "val": {"id": "matte-black", "type": "material"}}, {"key": "headlight-panels", "val": {"id": "Carbon Fiber", "type": "texture"}}, {"key": "seats-material", "val": {"id": "matte-lightgray", "type": "material"}}, {"key": "emblem-material", "val": {"id": "matte metallic-purple", "type": "material"}}, {"key": "headlights-material", "val": {"id": "orange", "type": "material"}}, {"key": "max-length", "val": {"value": 5.12352, "unit": "m"}}, {"key": "max-height", "val": {"value": 2.08889, "unit": "m"}}, {"key": "max-width", "val": {"value": 2.49419, "unit": "m"}}, {"key": "wheel-base", "val": {"value": 2.82967, 
# "unit": "m"}}, {"key": "ground-clearance", "val": {"value": 0.297131, "unit": "m"}}, {"key": "weight", 
# "val": {"value": 1600, "unit": "kg"}}, {"key": "aerodynamic-factor", "val": {"value": 70, "unit": "%"}}, {"key": "downforce", "val": {"value": 50, "unit": "%"}}, {"key": "handling", "val": {"value": 65, "unit": "%"}}], "name": "body"}, {"stats": [{"key": "wheel-type", "val": "offroad"}, {"key": "rim-type", "val": "Vault"}, {"key": "wheel-units", "val": 4}, {"key": "rim-material", "val": {"id": "matte-black", 
# "type": "material"}}, {"key": "size", "val": {"value": "391/50 R 23", "unit": "<width>/<height/width> R <rim diameter>"}}, {"key": "weight", "val": {"value": 156, "unit": "kg"}}, {"key": "braking-power", "val": {"value": 70, "unit": "%"}}], "name": "wheel"}, {"stats": [{"key": "power-units", "val": [{"weight": {"value": 185, "unit": "kg"}, "torque": {"value": 372, "unit": "nm@4800 rpm"}, "range": {"value": 375, "unit": "km"}, "unit-type": "v6 3.5 liter", "horse-power": {"value": 340, "unit": "hp"}}, {"weight": {"value": 92, "unit": "kg"}, "torque": {"value": 350, "unit": "nm"}, "range": {"value": 65, "unit": "km"}, "unit-type": "electric motor", "horse-power": {"value": 207, "unit": "hp"}}, {"weight": {"value": 
# 92, "unit": "kg"}, "torque": {"value": 350, "unit": "nm"}, "range": {"value": 65, "unit": "km"}, "unit-type": "electric motor", "horse-power": {"value": 207, "unit": "hp"}}]}], "name": "power-unit"}, {"stats": [{"key": "drive-train", "val": [{"drive-train-type": "4WD"}, {"gears": "8 speed", "transmission-type": "automatic"}]}], "name": "drive-train"}, {"stats": [{"key": "top-speed", "val": {"value": 265.7704142964, "unit": "km/h"}}, {"key": "acceleration", "val": {"value": 3.6, "unit": "s"}}, {"key": "weight", "val": {"value": 2132, "unit": "kg"}}, {"key": "aerodynamic-factor", "val": {"value": 73, "unit": "%"}}, {"key": "downforce", "val": {"value": 56, "unit": "%"}}, {"key": "handling", "val": {"value": 71, "unit": "%"}}, {"key": "horsepower", "val": {"value": 754, "unit": "hp"}}, {"key": "braking-power", "val": {"value": 70, "unit": "%"}}], "name": "derived-stats"}, {"stats": [{"key": "name", "val": "Digital Den"}], "name": "background"}, {"stats": [{"key": "spoiler-type", "val": "Slip Stream"}, {"key": "handling", "val": {"value": 6, "unit": "%"}}, {"key": "downforce", "val": {"value": 6, "unit": "%"}}, {"key": 
# "aerodynamic-factor", "val": {"value": 3, "unit": "%"}}, {"key": "weight", "val": {"value": 7, "unit": 
# "kg"}}], "name": "spoiler"}]}}, {"hash": "n0Ixx0AzCMLCiJHr-gFty5b1p_o64sVsxkBx-aazSYI", "uri": {"data": "immutable-state-data", "scheme": "pact:schema"}, "datum": {"mint-time": {"timep": "2023-02-10T06:30:17.926451Z"}, "vehicle-information": {"model": "K:2", "make": "Kadcars", "vin": "4990"}}}, {"hash": "cUQyNFXWjF66xG7q9gZN9BnHnjj8xgHg3Kxcghqu6R8", "uri": {"data": "view-references", "scheme": "pact:schema"}, "datum": {"art-asset": {"data": "ipfs://bafybeiaj7xvhlkgardeaw2hi2k4gkjhe7tuouc3zbe7dfje23sh5pkom6a", 
# "scheme": "ipfs://"}}}, {"datum": {"datum": {"id": "4990", "name": "Kadcars NFT #4990", "attributes": [{"trait_type": "Background", "value": "Digital Den", "score": 8.18558282208589}, {"trait_type": "Type", "value": "K:2", "score": 1.5322997416020672}, {"trait_type": "Trim", "value": "Carbon Fiber", "score": 2.3063958513396714}, {"trait_type": "Headlights", "value": "Orange", "score": 7.3613793103448275}, {"trait_type": "Spoiler", "value": "Slip Stream", "score": 4.328467153284672}, {"trait_type": "Rims", "value": "Vault", "score": 6.106407322654462}, {"trait_type": "Paint Job", "value": "Ultraviolet", "score": 12.02027027027027}, {"trait_type": "Finish", "value": "Glossy", "score": 3.2092603728202045}], "rarity_score": 45.050062844402056, "rarity_level": "RARE"}}}], "uri": {"data": "https://kadcars-nft-metadata.nyc3.digitaloceanspaces.com/4990.webp", "scheme": "ipfs"}, "attachments": [{"token_id": "t:hGgcj7Y1p8VnPk4GqdZgGMKqMbcqyOOW2Zzhm-sPvK4", "nft_id": "test_sticker", "collection_id": "collection:Ufj5r2bYxa6OX4xnXFalmZXdc_NEjs4Vi0PVdMD6_uw", "collection_name": "kadcars-stickers", "chain_id": "8", "uri": "https://isoko-testing.nyc3.cdn.digitaloceanspaces.com/barb.jpeg", "uv_map": "UVMap.002"}, {"token_id": "t:hGgcj7Y1p8VnPk4GqdZgGMKqMbcqyOOW2Zzhm-sPvK4", "nft_id": "test_sticker", "collection_id": "collection:Ufj5r2bYxa6OX4xnXFalmZXdc_NEjs4Vi0PVdMD6_uw", "collection_name": "kadcars-stickers", "chain_id": "8", "uri": 
# "https://isoko-testing.nyc3.cdn.digitaloceanspaces.com/barb.jpeg", "uv_map": "UVMap.002"}]}
# digital_ocean = DigitalOcean()
# digital_ocean.upload_file("/Users/mohannadahmad/Desktop/AppDev/Kadena/R2R/ready2render/r2r/kadcars/hood.png", "kadcars-renders", "hood.png")
# digital_ocean.upload_to_spaces("kadcars-nft-metadata", json.dumps(lol), "lol.json", "public-read-write")
# import bpy

# bpy.context.preferences.addons["cycles"].preferences.get_devices()
# print(bpy.context.preferences.addons["cycles"].preferences.compute_device_type)
# for d in bpy.context.preferences.addons["cycles"].preferences.devices:
#     d["use"] = 1 # Using all devices, include GPU and CPU
#     print(d["name"], d["use"])