import http.client
import os
import re
import json
import http
import requests
import subprocess
from r2r.models.nft import NFT
from r2r.utils.io_utils import *
from config import IPFS_BEARER_TOKEN, IPFS_CAR_FILES_PATH, IPFS_DOWNLOAD_PATH

IPFS_URL_PREFIX = "https://api.nft.storage/"
DEFAULT_IPFS_GATEWAY = "ipfs.io"


def get_headers(content_type):
    headers = {
        'Content-type': content_type,
        'Authorization': 'Bearer {}'.format(IPFS_BEARER_TOKEN)
    }
    return headers


def get_asset_from_ipfs(cid):
    response = requests.get(str("https://api.nft.storage/{}".format(cid)), headers=get_headers("application/json"))
    print(response.json())


def upload_nft_files_to_ipfs(nft_asset_path, render_asset_path):
    destination = nft_asset_path.split('/')[len(nft_asset_path.split('/')) - 1] + ".car"

    car_file_dest_directory = IPFS_CAR_FILES_PATH
    car_file_dest_file = os.path.join(car_file_dest_directory, destination)

    pack_and_split_CAR_file(nft_asset_path, car_file_dest_file)
    glb_cid = iterate_over_car_files_and_upload(car_file_dest_directory, car_file_dest_file)
    glb_url = "ipfs://" + glb_cid
    print("GLB")
    print(glb_url)

    webp_cid = upload_asset_to_ipfs(render_asset_path, 'image/*')
    webp_url = "ipfs://" + webp_cid

    return glb_url, webp_url


def upload_asset_to_ipfs(asset_file, format):
    response = None
    try:
        response = requests.post(
            url=IPFS_URL_PREFIX + "upload/", 
            data=open(asset_file, 'rb'), 
            headers=get_headers(format)
        )
        print("Uploaded")
        print(response.json())
        if response.ok == True:
            cid = response.json()["value"]["cid"]
            return cid
    except Exception as error:
        print(error)
        print("Something went wrong with request")
        exit()


def pack_and_split_CAR_file(asset_path, output_path):
    in_path = '"{fname}"'.format(fname=asset_path)
    out_path = '"{fname}"'.format(fname=output_path)
    print(in_path)
    print(out_path)
    ipfs_car_command = "ipfs-car --pack " + str(in_path) + " --output " + str(out_path)
    carbites_command = "carbites split " + str(out_path) + " --size 100MB --strategy treewalk"

    # pack CAR file, capture CID
    ipfs_car_command_output = subprocess.run(ipfs_car_command, shell=True, capture_output=True)
    print(ipfs_car_command_output)
    # cid["value"] = re.match(r"b'root\sCID:\s(.+?)\\n.*", str(command_output.stdout)).groups()[0]

    # split CAR file
    # os.system("carbites split " + out_path + " --size 100MB --strategy treewalk")
    carbites_command_output = subprocess.run(carbites_command, shell=True, capture_output=True)
    print(carbites_command_output)

def pin_asset_using_cid(cid):
    command = "ipfs pin add " + cid

    print("Pinning asset " + cid)
    command_output = subprocess.run(command, shell=True, capture_output=True)
    print(command_output)

def iterate_over_car_files_and_upload(car_file_dest_directory, car_file_output_path):
    glb_cid = ""
    print("car files")
    print(os.listdir(car_file_dest_directory))
    for car_file in os.listdir(car_file_dest_directory):
        car_file_path = os.path.join(car_file_dest_directory, car_file)

        if car_file_path == car_file_output_path:
            print("AVOIDED " + car_file_path + "\n")
            continue

        glb_cid = upload_asset_to_ipfs(car_file_path, 'application/car')
        print(car_file_path + "   CID: " + glb_cid + "\n")

    return glb_cid

def download_glb_asset(glb_ipfs_dir_cid):
    glb_ipfs_asset_file_name = ""
    glb_ipfs_asset_cid = ""
    asset_file_path = None

    try:
        response = requests.get("https://" + DEFAULT_IPFS_GATEWAY + "/api/v0/ls?arg=/ipfs/" + glb_ipfs_dir_cid)

        if response.status_code == 200:
            glb_ipfs_asset_cid = response.json()["Objects"][0]["Links"][0]["Hash"]
            glb_ipfs_asset_file_name = response.json()["Objects"][0]["Links"][0]["Name"]

            print("https://" + glb_ipfs_dir_cid + ".ipfs.nftstorage.link/ipfs/" +
                  glb_ipfs_asset_cid + "?filename=" + glb_ipfs_asset_file_name)

            try:
                res = requests.get("https://" + glb_ipfs_dir_cid + ".ipfs.nftstorage.link/ipfs/" +
                                   glb_ipfs_asset_cid + "?filename=" + glb_ipfs_asset_file_name, allow_redirects=True)

                if res.status_code == 200:
                    asset_file_path = 'asset_glb.glb'
                    write_file(asset_file_path, res.content)
            except:
                print("Error downloading GLB")
    except:
        print("Failed to retrieve GLB ipfs directory data")

    return asset_file_path

def download_webp_asset(manifest):
    asset_file_path = None

    try:
        # download WEBP
        response = requests.get("https://" + manifest["uri"]["data"].split(
            "//")[1] + ".ipfs.nftstorage.link?download=true", allow_redirects=True)

        if response.status_code == 200:
            asset_file_path = 'asset_render.webp'
            write_file(asset_file_path, response.content)

    except:
        print()
        print("Failed to fetch asset from IPFS")

    return asset_file_path

def download_asset_from_ipfs(nft: NFT):
    cid = nft.get_asset_ipfs_cid()
    asset_filename = nft.get_asset_ipfs_file_name()
    download_dir_name = nft.get_asset_ipfs_download_dir_name()
    asset_download_full_path = f"{IPFS_DOWNLOAD_PATH}/{download_dir_name}/{asset_filename}"
    url = f"https://{cid}.ipfs.nftstorage.link/{asset_filename}"
    print(f"Downloading GLB from: {url}")

    try:
        with requests.get(url, stream=True) as response:
            print(response.status_code)
            response.raise_for_status()

            if os.path.isdir(f"{IPFS_DOWNLOAD_PATH}/{download_dir_name}") == False:
                os.mkdir(f"{IPFS_DOWNLOAD_PATH}/{download_dir_name}")
            
            with open(asset_download_full_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            file.close()
        print(f"GLB file downloaded successfully and saved as {asset_download_full_path}")
        return asset_download_full_path
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def get_file_name_from_ipfs_dir(cid):
    try:
        response = requests.post("http://127.0.0.1:5001/api/v0/ls?arg=/ipfs/" + cid)

        if response.status_code == 200:
            ipfs_asset_file_name = response.json()["Objects"][0]["Links"][0]["Name"]

            return ipfs_asset_file_name
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def add_ipfs_data_to_kc_metadata(asset_file_name, ipfs_url, destination):
    kadcar_metadata = extract_data_from_json(asset_file_name)
    print(kadcar_metadata)

    if destination == 'webp':
        kadcar_metadata["webp-ipfs"] = ipfs_url
    elif destination == 'glb':
        kadcar_metadata["view-refs"]["data"] = ipfs_url

    with open(asset_file_name, 'w') as out:
        json.dump(kadcar_metadata, out)
