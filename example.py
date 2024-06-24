import requests
from kad_py.main.kad_py_public import *
from kad_py.commands.env_data import EnvData
from ready2render.config import SENDER, DEFAULT_GAS_LIMIT, DEFAULT_GAS_PRICE, MAINNET_NETWORK_ID

def run_r2r_upgrade():
    blueprint_hash = "hash"
    pact_code = f'(n_f1c962776331c4773136dc1587a8355c9957eae1.upgrade-handler.perform-upgrade "{blueprint_hash}" "{SENDER}")'
    env_data = EnvData({
        "target-token-id": "",
        "target-nft-name": "",
        "target-nft-uri": "",
        "target-collection-id": "",
        "target-collection-name": "",
        "target-collection-standard": "",
        "attachment-token-id": "",
        "attachment-nft-name": "",
        "attachment-nft-uri": "",
        "attachment-collection-id": "",
        "attachment-collection-name": "",
        "attachment-collection-standard": "",
        "target-location": ""
    })

    exec_response = execute_exec_cmd(
        sender=SENDER,
        code=pact_code,
        chain_id="8",
        gas_price=DEFAULT_GAS_PRICE * 2,
        gas_limit=DEFAULT_GAS_LIMIT,
        signers=[SENDER],
        env_data=env_data,
        caps=[],
        ttl=600,
        network_id=MAINNET_NETWORK_ID,
        nonce="1234",
        sign_method=CLI
    )
    print("--------------------------------------------")
    print("exec response")
    print(exec_response)
    print("--------------------------------------------")

    if "requestKeys" in exec_response:
        res = requests.post("http://127.0.0.1:8000/r2r/combine_nfts/", {
            "request_key": exec_response["requestKeys"][0],
            "chain_id": "8",
            "owner": SENDER,
            "blueprint_hash": blueprint_hash
        })

        print(res.json())

    #     cont_response = execute_cont_cmd(
    #         sender=SENDER,
    #         chain_id="8",
    #         gas_price=DEFAULT_GAS_PRICE,
    #         gas_limit=DEFAULT_GAS_LIMIT,
    #         ttl=600,
    #         network_id=MAINNET_NETWORK_ID,
    #         step=1,
    #         rollback=False,
    #         env_data=EnvData({}),
    #         pact_tx_hash=exec_response["requestKeys"][0],
    #         sign_method=CLI,
    #         signers=[SENDER],
    #         proof=None
    #     )