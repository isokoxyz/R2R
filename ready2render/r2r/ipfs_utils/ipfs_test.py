import os
from ipfs_utils import *
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from io_utils import *
import re

dirname = os.path.dirname(__file__)
print(dirname)
metadata_dir = os.path.join(dirname, "../metadata_json")
# kadcar_dirs_root = os.path.join(dirname, "../assets/completed_nfts/")
# car_folder_path = 'C:/Users/Mohannad Ahmad\Desktop/AppDev/Crypto/Kadena\KadcarBackendApi/kadcars_backend_api_local_bpy/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets/car_files/'
# car_folder_path = dirname + '/../assets/car_files/'
car_folder_path = 'K:/car_files/'
batch_config_file = extract_data_from_json(os.path.join(dirname, "../json_config_files/batch_config.json"))

# print("Enter batch number")
# batch_number = input()

# print("Press y to confirm batch number " + str(batch_number))
# answer = input()
# if answer != 'y':
#     print("Invalid input")
#     exit()

def car_file_generator(batch_number):
    kadcar_dirs_root = os.path.join("K:/completed_nfts/batch_" + str(batch_number))
    counter = 0
    for dir in os.listdir(kadcar_dirs_root):
        current_kc_folder = os.path.join(kadcar_dirs_root, dir)
        if os.path.isdir(current_kc_folder) == False:
            continue
        for kc_dir in os.listdir(current_kc_folder):
            current_bg_folder = os.path.join(current_kc_folder, kc_dir)
            for nft_dir_name in os.listdir(current_bg_folder):
                nft_dir_path = os.path.join(current_bg_folder, nft_dir_name)
                
                # output_file_name = reformat_name(output_file_name.split('_'))

                ############################
                ## Rename files correctly ##
                ############################
                
                vin_int = counter + (103 * int(batch_number))
                vin = str(vin_int)
                
                counter += 1
                if vin_int < 5402:
                    continue
                print(vin_int)
                glb_path = os.path.join(nft_dir_path, "nft_" + vin + ".glb")
                webp_render_path = os.path.join(nft_dir_path, "render_" + vin + ".webp")
                json_path = os.path.join(nft_dir_path, "metadata_" + vin + ".json")
                print(glb_path)
                print(json_path)

                if os.path.exists(glb_path) == False:
                    os.rename(nft_dir_path + "/nft.glb", glb_path)
                if os.path.exists(webp_render_path) == False:
                    os.rename(nft_dir_path + "/" + nft_dir_name + "_render.webp", webp_render_path)
                if os.path.exists(json_path) == False:
                    os.rename(nft_dir_path + "/" + nft_dir_name + ".json", json_path)

                ##############################
                ## Upload CAR files to IPFS ##
                ##############################

                #Create directory for car files
                car_file_dest_directory = os.path.join(car_folder_path, nft_dir_name)
                car_file_output_path = os.path.join(car_file_dest_directory, "car_file_" + vin + ".car")

                create_dir_at_path(car_file_dest_directory)

                #Create the car files
                pack_and_split_CAR_file(glb_path, car_file_output_path)
                print(os.listdir(car_file_dest_directory))

                glb_cid = ""
                for car_file in os.listdir(car_file_dest_directory):
                    car_file_path = os.path.join(car_file_dest_directory, car_file)

                    if car_file_path == car_file_output_path:
                        print("AVOIDED " + car_file_path + "\n")
                        continue
                    
                    glb_cid = upload_asset_to_ipfs(car_file_path, 'application/car')
                    print(car_file_path + "   CID: " + glb_cid + "\n")

                add_ipfs_data_to_kc_metadata(json_path, "ipfs://" + glb_cid, "glb")
                # if not remove_dir_at_path(car_file_dest_directory):
                #     print("Error removing directory")

                print("FINISHED : " + car_file_dest_directory)

                #########################
                ## Upload WEBP to IPFS ##
                #########################

                webp_cid = upload_asset_to_ipfs(webp_render_path, 'image/*')
                print(webp_render_path + "   CID: " + webp_cid + "\n")

                add_ipfs_data_to_kc_metadata(json_path, "ipfs://" + webp_cid, "webp")

                f1 = open(kadcar_dirs_root + '/glb_cids.txt', 'a')
                f1.write(glb_cid + '\n')
                f1.close()
                
                f2 = open(kadcar_dirs_root + '/webp_cids.txt', 'a')
                f2.write(webp_cid + '\n')
                f2.close()
                
                

def reformat_name(tokens):
    name = ""
    for i in range(len(tokens)):
        if tokens[i] == "fiber":
            continue
        elif tokens[i] == "rims":
            name += "r"
        elif tokens[i] == "spoiler":
            name += "sp_"
            continue
        elif tokens[i] == 'metallic':
            name += "mtl_"
            continue
        elif tokens[i] == 'glossy':
            name += "glo_"
            continue
        elif tokens[i] == "carbon":
            name += "cf_"
            continue
        name += tokens[i]

        if i < len(tokens) - 1:
            name += "_"
    print(name)
    return name

print("How many batches are you uploading?")
num_batches = input()
num_batches = int(num_batches)

print("Type starting batch number")
starting_batch = input()
starting_batch = int(starting_batch)

print("Press y to confirm, starting at " + str(starting_batch) + " for a total of " + str(num_batches))
answer = input()
if answer != 'y':
    print("Invalid input")
    exit()

if num_batches < 1:
    print("Invalid number of batches")
    exit() 

for i in range(num_batches):
    car_file_generator(starting_batch)
    starting_batch += 1

########################
## FAILED: 
##   1. batch 16
##
## MATTHEW:
##   batches 19 - 27