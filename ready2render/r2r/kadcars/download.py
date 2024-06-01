import bpy
import subprocess
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))



glb_ipfs_dir_cid = "bafybeidyebmqeg6ibtpmww5hqjk7a5exddyqzxt4c6obaxm43hbz36kjke"
glb_ipfs_asset_file_name = ""
glb_ipfs_asset_cid = ""
asset_file_path = None

# with requests.get("https://bafybeidyebmqeg6ibtpmww5hqjk7a5exddyqzxt4c6obaxm43hbz36kjke.ipfs.nftstorage.link/nft_0.glb", timeout=None, stream=True, verify=False) as r:
#     r.raise_for_status()
#     with open("./lol.glb", 'wb') as f:
#         for chunk in r.iter_content(chunk_size=None): 
#             # If you have chunk encoded response uncomment if
#             # and set chunk_size parameter to None.
#             if chunk: 
#                 f.write(chunk)

session = requests.Session()
with session.get("https://bafybeidyebmqeg6ibtpmww5hqjk7a5exddyqzxt4c6obaxm43hbz36kjke.ipfs.nftstorage.link/nft_0.glb") as r:
    with open('lol.glb', 'wb') as f:
        for chunk in r.iter_content(chunk_size=2048*2048): 
            # If you have chunk encoded response uncomment if
            # and set chunk_size parameter to None.
            # if chunk: 
            f.write(chunk)
# response = requests.get("https://ipfs.io/api/v0/get?arg="+glb_ipfs_dir_cid)

# if response.status_code == 200:
#     glb_ipfs_asset_cid = response.json()["Objects"][0]["Links"][0]["Hash"]
#     glb_ipfs_asset_file_name = response.json()["Objects"][0]["Links"][0]["Name"]

#     print("https://" + glb_ipfs_dir_cid + ".ipfs.nftstorage.link/ipfs/" +
#             glb_ipfs_asset_cid + "?filename=" + glb_ipfs_asset_file_name)

#     try:
#         res = requests.get("https://" + glb_ipfs_dir_cid + ".ipfs.nftstorage.link/ipfs/" +
#                             glb_ipfs_asset_cid + "?filename=" + glb_ipfs_asset_file_name, allow_redirects=True)

#         if res.status_code == 200:
#             asset_file_path = 'asset_glb.glb'
#             write_file(asset_file_path, res.content)
#     except:
#         print("Error downloading GLB")