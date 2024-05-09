import csv
import re
import subprocess
from ipfs_utils import pin_asset_using_cid

def pin_cids_to_ipfs():
    # subprocess.call([r'ipfs_daemon.bat'])
    with open('webps.txt', 'r') as fd:
        lines = fd.readlines()

        for line in lines:
            match = re.findall(r'"(.*?)"', line)
            if len(match) > 0:
                pin_asset_using_cid(match[0])

pin_cids_to_ipfs()