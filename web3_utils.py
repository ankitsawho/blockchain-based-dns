from web3 import Web3
import json
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")

contract_addr = config['CONTRACT_ADDR']
addr = config['ADDR']
pvt_key = config['PRIVATE_KEY']


def preprocess(data):
    result = {
        "$ttl": data[0],
        "soa": {
            "mname": data[1],
            "rname": data[2],
            "serial": data[3],
            "refresh": data[4],
            "retry": data[5],
            "expire": data[6],
            "minimum": data[7]
        },
        "ns": [
            {"host": i} for i in data[8]
        ],
        "a": [
            {"name": "@", "ttl": 400, "value": i} for i in data[9]
        ]
    }
    return result


def store(origin, ttl, mname, rname, serial, refresh, retry, expire, minimum, host, ip):
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    chain_id = 1337
    with open("compiled_code.json", "r") as file:
        compile_sol = json.load(file)
        abi = compile_sol["contracts"]["ZonesStorage.sol"]["ZonesStorage"]["abi"]
    nonce = w3.eth.getTransactionCount(addr)

    # Working with contract
    zones_storage = w3.eth.contract(address=contract_addr, abi=abi)

    # Store Value
    store_txn = zones_storage.functions.addZone(
        origin,
        ttl,
        mname,
        rname,
        serial,
        refresh,
        retry,
        expire,
        minimum,
        host,
        ip
    ).buildTransaction({
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": addr,
        "nonce": nonce
    })
    signed_txn = w3.eth.account.sign_transaction(
        store_txn, private_key=pvt_key
    )
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("Updating stored Value...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    print(tx_receipt)


def retrieve(domain):
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    with open("compiled_code.json", "r") as file:
        compile_sol = json.load(file)
        abi = compile_sol["contracts"]["ZonesStorage.sol"]["ZonesStorage"]["abi"]
    # Working with contract
    zones_storage = w3.eth.contract(address=contract_addr, abi=abi)
    result = zones_storage.functions.retrieve(domain).call()
    if (result[0] == 0):
        return
    res = preprocess(result)
    res["$origin"] = domain
    return res
