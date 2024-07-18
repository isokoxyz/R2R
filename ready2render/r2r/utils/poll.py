import json
import time
from kad_py.main.kad_py_public import pact_fetch_local
from kad_py.main.kad_py_pvt import get_api_url, execute_network_request
from kad_py.config.constants import MAINNET_NETWORK_ID

class Poll:
    """
    This class provides functionality to poll transactions over a period of time
    until a response is received from the targeted endpoint
    """
    def __init__(self, sender, chain_id):
        self.sender = sender
        self.chain_id = chain_id

    def poll_request_key(self, tx_id):
        """
        This function receives a transaction ID and polls the status of the transaction
        by querying the Kadena blockchain repeatedly

        Returns:
            string: status of the transaction when its complete
        """
        payload = {
            "requestKeys": [tx_id]
        }
        headers = {
            "Content-Type": "application/json"
        }

        network_url = get_api_url(network_id=MAINNET_NETWORK_ID, chain_id=self.chain_id, endpoint="poll")

        curr_time = 0
        result = None
        timeout = time.time() + 60*5
        while curr_time < timeout:
            response = execute_network_request(network_url, json.dumps(payload), headers, timeout)

            if tx_id in response:
                result = response[tx_id]["result"]["status"]
                break
            elif time.time() > timeout:
                break
            curr_time += 1
            time.sleep(5)
        
        return result
