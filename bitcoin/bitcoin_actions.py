import os
import subprocess
import json

TYPICAL_TX_SIZE = 200


def get_address_info(address="tb1q7nst4y7wccahqg5maqagg7vj9l5vwfa5ycqmv0"):
    address_info = json.loads(subprocess.check_output(["bitcoin-cli", "-regtest", "-rpcwallet=money", "listreceivedbyaddress"]))
    return address_info[0]
    #address_info = json.loads(subprocess.check_output(["bitcoin-cli", "-regtest", "-rpcwallet=money", "getaddressinfo", address]))
    #return address_info 


def get_utxo(address):
    utxo = json.loads(subprocess.check_output(["bitcoin-cli", "-regtest", "-rpcwallet=money", "listunspent", "0", "99999", f'["{address}"]']))[0]
    utxo_txid = utxo["txid"]
    utxo_vout = utxo["vout"]
    return utxo_txid,  utxo_vout


def get_balance(address):
    utxos = json.loads(subprocess.check_output(["bitcoin-cli", "-regtest", "-rpcwallet=money", "listunspent", "0", "9999999", f'["{address}"]']))
    
    if len(utxos) > 0:
        total_received = sum(utxo["amount"] for utxo in utxos)
        return total_received
    else:
        return 0


def generate_new_address(wallet_name="money"):
    try:
        output = subprocess.check_output(["bitcoin-cli", "-regtest", "-rpcwallet=" + wallet_name, "getnewaddress"])
        new_address = output.decode("utf-8").strip()
        return new_address
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None


def create_raw_transaction(utxo_txid, utxo_vout, op_return_data, change_address, change_amount):
    command = [
        "bitcoin-cli",
	"-regtest",
        "-named",
        "-rpcwallet=money",
        "createrawtransaction",
        f'[{{\"txid\":\"{utxo_txid}\",\"vout\":{utxo_vout}}}]',
        f'{{\"data\":\"{op_return_data}\",\"{change_address}\":{change_amount}}}'
    ]

    rawtxhex = subprocess.check_output(command).decode('utf-8').strip()

    return rawtxhex


def sign_transaction(tx_id_hex):
    wpp
    command = ["signrawtransactionwithwallet", "-regtest", "-rpcwallet=money", tx_id_hex]
    signed_hex = subprocess.run(command, check=True, capture_output=True, text=True)
    return signed_hex


def wpp(passph="passph"):
    command = ["walletpassphrase", "-regtest", "-rpcwallet=money", passph, "100"]
    signed_hex = subprocess.run(command, check=True, capture_output=True, text=True)
    return signed_hex


def sign_with_key(address, raw_transaction):
    command = ["dumpprivkey", "-regtest", "-rpcwallet=money", address]
    signed_hex = json.loads(subprocess.check_output(command)).decode('utf-8').strip()
    dump_command = [
        "bitcoin-cli",
        "signrawtransactionwithkey",
        "-regtest",
        "-rpcwallet=money",
        raw_transaction,
        json.dumps([key])
    ]
    private_key = subprocess.check_output(dump_command, text=True).strip()
    #signed_hex = json.loads(subprocess.check_output(command))["hex"]
    return private_key
  

def send_transaction(tx_hex):
    command = ["sendrawtransaction", "-regtest" "-rpcwallet=money", tx_hex]
    response = subprocess.check_output(command)
    return response.decode().strip()


def get_raw_change_address():
   raw_change_address = subprocess.check_output(["bitcoin-cli", "-regtest", "-rpcwallet=money", "getrawchangeaddress"])
   raw = raw_change_address.decode("utf-8").strip()
   return raw

def transaction_cost(op_data_str):
    op_data_hex = op_data_str.encode().hex()
    no_msg_transaction = 93
    tx_size = len(op_data_hex) + no_msg_transaction + TYPICAL_TX_SIZE 
    feerate = get_estimated_fee()
    tx_cost = calculate_fee(tx_size, feerate)  
    return round(tx_cost, 8)


def transaction_brutto(op_data_str):
    BTC_note_fee = 1.5 
    tx_cost = transaction_cost(op_data_str)
    return (BTC_note_fee * tx_cost) + tx_cost

# Returns fee for a transaction based on tx size and current fee rate 
def calculate_fee(tx_size, feerate):
    return (feerate / 1000) * tx_size # BTC


# Returns estimated fee based on number of blocks
# estimate fee rate in BTC/kB
def get_estimated_fee(blocks=6):
    result = subprocess.check_output(["bitcoin-cli", "-testnet", "estimatesmartfee", str(blocks)])
    fee_info = json.loads(result)
    return fee_info["feerate"]


def get_utxo_json(address):
    utxo = json.loads(subprocess.check_output(["bitcoin-cli", "-regtest", "-rpcwallet=money", "listunspent", "0", "99999", f'["{address}"]']))[0]
    utxo_txid = utxo["txid"]
    utxo_vout = utxo["vout"]
    script_pub_key = utxo["scriptPubKey"]
    amount = utxo["amount"]
    input_json = {
        "txid": utxo["txid"],
        "vout": utxo["vout"],
        "scriptPubKey": utxo["scriptPubKey"],
        "amount": utxo["amount"]
    }
    return input_json
