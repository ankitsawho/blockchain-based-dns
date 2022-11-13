from web3 import Web3
from solcx import compile_standard, install_solc
import json
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")

with open("./ZonesStorage.sol", "r") as file:
    simple_storage_file = file.read()


print("Installing ...")
install_solc("0.8.0")

compile_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "ZonesStorage.sol": {
            "content": simple_storage_file
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }
        }
    }
},
    solc_version="0.8.0"
)

with open("compiled_code.json", "w") as file:
    json.dump(compile_sol, file)


# get bytecode
bytecode = compile_sol["contracts"]["ZonesStorage.sol"]["ZonesStorage"]["evm"]["bytecode"]["object"]

# get abi
abi = compile_sol["contracts"]["ZonesStorage.sol"]["ZonesStorage"]["abi"]


# connecting to blockchain
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
addr = config['ADDR']
pvt_key = config['PRIVATE_KEY']


# Create a contract
ZonesStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(addr)


# Build Transaction
transaction = ZonesStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": addr, "nonce": nonce, "gasPrice": w3.eth.gas_price})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=pvt_key)

# send signed Transaction
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

print("Waiting for transaction to finish...")
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
contract_addr = txn_receipt.contractAddress
print(f"Done! Contract deployed to {contract_addr}")
