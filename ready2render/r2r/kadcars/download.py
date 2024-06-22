import http.client
import bpy
import subprocess
import requests
import sys
import os
import http
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pygltflib import GLTF2
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))



glb_ipfs_dir_cid = "bafybeidyebmqeg6ibtpmww5hqjk7a5exddyqzxt4c6obaxm43hbz36kjke"
glb_ipfs_asset_file_name = ""
glb_ipfs_asset_cid = ""
asset_file_path = None

def download_glb_from_ipfs(ipfs_hash, glb_filename):
    url = f"https://bafybeidyebmqeg6ibtpmww5hqjk7a5exddyqzxt4c6obaxm43hbz36kjke.ipfs.nftstorage.link/nft_0.glb"
    print(url)
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(glb_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
        print(f"GLB file downloaded successfully and saved as {glb_filename}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Replace with your IPFS directory hash and GLB filename
ipfs_directory_hash = "bafybeidyebmqeg6ibtpmww5hqjk7a5exddyqzxt4c6obaxm43hbz36kjke"
glb_filename = "nft_0.glb"

# download_glb_from_ipfs(ipfs_directory_hash, glb_filename)
gltf = GLTF2()
# gltf = gltf.load("K:/UpgradeTest/ipfs_downloads/kadcars/nft_405.glb")
gltf = gltf.load("K:/UpgradeTest/exports/kadcars/kadcar_1333.glb")
print(gltf.extras)