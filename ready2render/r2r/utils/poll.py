import json
import time
from kad_py.main.kad_py_public import pact_fetch_local
from kad_py.main.kad_py_pvt import get_api_url, execute_network_request
from kad_py.config.constants import MAINNET_NETWORK_ID

class Poll:
    def __init__(self, sender, chain_id):
        self.sender = sender
        self.chain_id = chain_id

    def poll_request_key(self, tx_id):
        payload = {
            "requestKeys": [tx_id]
        }
        headers = {
            "Content-Type": "application/json"
        }

        network_url = get_api_url(network_id=MAINNET_NETWORK_ID, chain_id=self.chain_id, endpoint="poll")

        curr_time = 0
        response = None
        while curr_time < time.time() + 60*5:
            response = execute_network_request(network_url, json.dumps(payload), headers)
            if response["requestKey"].result.status == "success" or test == 5 or time.time() > timeout:
                break
            curr_time += 1
            time.sleep(5)
        
        return response
