import http.client
import bpy
import subprocess
import requests
import sys
import os
import http
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))



glb_ipfs_dir_cid = "bafybeidyebmqeg6ibtpmww5hqjk7a5exddyqzxt4c6obaxm43hbz36kjke"
glb_ipfs_asset_file_name = ""
glb_ipfs_asset_cid = ""
asset_file_path = None
for attempt in range(10):
    client = http.client.HTTPSConnection("ipfs.io")
    client.request("GET", "/ipfs/bafybeidyebmqeg6ibtpmww5hqjk7a5exddyqzxt4c6obaxm43hbz36kjke/nft_0.glb")
    # client.request("GET", "/ipfs/bafybeidyebmqeg6ibtpmww5hqjk7a5exddyqzxt4c6obaxm43hbz36kjke")
    response = client.getresponse()
    # Check if the request was successful
    if response.status == 200:
        # Read the data from the response
        data = response.read()
        print(data)

        # Write the data to a file
        # with open("lol.glb", 'wb') as file:
        #     file.write(data)
    else:
        print("fuck you")

# with requests.get("https://ipfs.io/ipfs/bafybeidyebmqeg6ibtpmww5hqjk7a5exddyqzxt4c6obaxm43hbz36kjke/nft_0.glb", timeout=None, stream=True, verify=False) as r:
#     r.raise_for_status()
#     with open("./lol1.glb", 'wb') as f:
#         for chunk in r.iter_content(chunk_size=None): 
#             # If you have chunk encoded response uncomment if
#             # and set chunk_size parameter to None.
#             if chunk: 
#                 f.write(chunk)

# session = requests.Session()
# with session.get("https://bafybeidyebmqeg6ibtpmww5hqjk7a5exddyqzxt4c6obaxm43hbz36kjke.ipfs.nftstorage.link/nft_0.glb") as r:
#     with open('lol.glb', 'wb') as f:
#         for chunk in r.iter_content(chunk_size=2048*2048): 
#             # If you have chunk encoded response uncomment if
#             # and set chunk_size parameter to None.
#             # if chunk: 
#             f.write(chunk)
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