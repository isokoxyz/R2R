import os
import re
import json
import requests
import subprocess
from r2r.utils.io_utils import *
from config import IPFS_BEARER_TOKEN

IPFS_URL_PREFIX = "https://api.nft.storage/"
DEFAULT_IPFS_GATEWAY = "ipfs.io"


def get_headers(content_type):
    headers = {
        'Content-type': content_type,
        'Authorization': 'Bearer {}'.format(IPFS_BEARER_TOKEN)
    }
    return headers


def get_asset_from_ipfs(cid):
    response = requests.get(str(
        "https://api.nft.storage/bafybeihtn6sk44pxizjedv7u2nqdq3ncijwmcdxgin3tcnnqh55hckvpfm"), headers=get_headers("application/json"))
    print(response.json())


def upload_nft_files_to_ipfs(nft_asset_path, render_asset_path):
    destination = nft_asset_path.split(
        '/')[len(nft_asset_path.split('/')) - 1] + ".car"

    car_file_dest_directory = 'K:/car_file/'
    car_file_dest_file = os.path.join(car_file_dest_directory, destination)

    pack_and_split_CAR_file(nft_asset_path, car_file_dest_file)
    glb_cid = iterate_over_car_files_and_upload(
        car_file_dest_directory, car_file_dest_file)
    glb_url = "ipfs://" + glb_cid

    webp_cid = upload_asset_to_ipfs(render_asset_path, 'image/*')
    webp_url = "ipfs://" + webp_cid

    return glb_url, webp_url


def upload_asset_to_ipfs(asset_file, format):
    response = None
    try:
        # with open(asset_file, 'rb') as f:
        #     response = requests.post(IPFS_URL_PREFIX + 'upload/', headers=headers, files={asset_file: f})

        response = requests.post(url=IPFS_URL_PREFIX + "upload/",
            data=open(asset_file, 'rb'), headers=get_headers(format))
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
    command = "ipfs-car --pack " + str(in_path) + " --output " + str(out_path)

    cid = {"name": "cid"}

    # pack CAR file, capture CID
    command_output = subprocess.run(command, shell=True, capture_output=True)
    # cid["value"] = re.match(r"b'root\sCID:\s(.+?)\\n.*", str(command_output.stdout)).groups()[0]

    # split CAR file
    os.system("carbites split " + out_path + " --size 100MB --strategy treewalk")


def pin_asset_using_cid(cid):
    command = "ipfs pin add " + cid

    print("Pinning asset " + cid)
    command_output = subprocess.run(command, shell=True, capture_output=True)
    print(command_output)


def iterate_over_car_files_and_upload(car_file_dest_directory, car_file_output_path):
    glb_cid = ""
    for car_file in os.listdir(car_file_dest_directory):
        car_file_path = os.path.join(car_file_dest_directory, car_file)

        if car_file_path == car_file_output_path:
            print("AVOIDED " + car_file_path + "\n")
            continue

        glb_cid = upload_asset_to_ipfs(
            car_file_path, 'application/car')
        print(car_file_path + "   CID: " + glb_cid + "\n")

    return glb_cid


def download_glb_asset(glb_ipfs_dir_cid):
    glb_ipfs_asset_file_name = ""
    glb_ipfs_asset_cid = ""
    asset_file_path = None

    try:
        response = requests.get(
            "https://" + DEFAULT_IPFS_GATEWAY + "/api/v0/ls?arg=" + glb_ipfs_dir_cid)

        if response.status_code == 200:
            glb_ipfs_asset_cid = response.json(
            )["Objects"][0]["Links"][0]["Hash"]
            glb_ipfs_asset_file_name = response.json(
            )["Objects"][0]["Links"][0]["Name"]

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

# TODO: make output file path more dynamic; firebase?


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


def add_ipfs_data_to_kc_metadata(asset_file_name, ipfs_url, destination):
    kadcar_metadata = extract_data_from_json(asset_file_name)
    print(kadcar_metadata)

    if destination == 'webp':
        kadcar_metadata["webp-ipfs"] = ipfs_url
    elif destination == 'glb':
        kadcar_metadata["view-refs"]["data"] = ipfs_url

    with open(asset_file_name, 'w') as out:
        json.dump(kadcar_metadata, out)
