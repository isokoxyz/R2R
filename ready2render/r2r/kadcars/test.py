import bpy
import subprocess
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.digital_ocean import DigitalOcean


# dest_nft_glb = 'C:/Users/Mohannad Ahmad\Desktop\AppDev\Crypto\Kadena\Kadcars\R2R/ready2render/r2r\kadcars\kadcar.glb'
# collection_name = "lol"

# digital_ocean = DigitalOcean()
# nft_metadata = requests.get("https://kadcars-manifests.nyc3.digitaloceanspaces.com/1.json").json()
# nft_metadata["haha"] = "lol"
# digital_ocean.upload_to_spaces("kadcars", json.dumps(nft_metadata), "1.json", "public")

# ipfs_car_command = "ipfs-car --pack K:/UpgradeTest/exports/kadcara.glb --output K:/UpgradeTest/car_files/kadcar.glb.car"
# ipfs_car_command = "ipfs-car --pack " + os.path.dirname(__file__) + "/kadcar.glb --output kadcar.glb.car"
ipfs_car_command = "\"C:/Program Files/nodejs/ipfs-car.cmd\" --pack " + os.path.dirname(__file__) + "/kadcar.glb --output kadcar.glb.car"
# ipfs_car_command = ["ipfs-car", "--pack", os.path.dirname(__file__) + "kadcar.glb", "--output", os.path.dirname(__file__) + "kadcar.glb.car"]

# pack CAR file, capture CID
ipfs_car_command_output = subprocess.run(ipfs_car_command, shell=True, capture_output=True)
print(ipfs_car_command_output)
# cid["value"] = re.match(r"b'root\sCID:\s(.+?)\\n.*", str(command_output.stdout)).groups()[0]

# split CAR file
# os.system("carbites split " + out_path + " --size 100MB --strategy treewalk")
# carbites_command = "carbites split K:\\UpgradeTest/car_files\\kadcara.glb.car --size 100MB --strategy treewalk"
# carbites_command_output = subprocess.Popen(carbites_command, shell=True, capture_output=True)
# print(carbites_command_output)