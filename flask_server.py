from flask import Flask
import requests
import subprocess
import json

app = Flask(__name__)



def get_balance():
    return  json.loads(subprocess.check_output(["bitcoin-cli", "-testnet", "-rpcwallet=testwallet", "getbalances"]))


@app.route("/note")
def get_wallet():
    #address = generate_new_address()
    address_info = get_address_info()
    address = address_info["address"]
    balance = address_info["amount"]
    utxo = get_utxo(address)
    raw =  get_raw_change_address()
    #confirmed = balance["mine"]["trusted"]
    #unconfirmed = balance["mine"]["untrusted_pending"]
    op_data_str = "Pies"
    op_data_hex = op_data_str.encode().hex()
    estm_fee_rate = get_estimated_fee()
    fee = calculate_fee(125, estm_fee_rate)
    balance_after_fee = balance - fee
    if balance_after_fee < 0:
        balance_after_fee = balance


    try:
    	txhex = create_raw_transaction(utxo[0], utxo[1], op_data_hex, address, balance_after_fee)
    except subprocess.CalledProcessError as e:
        print("Error:", e)


    # return "<h2>Adres konta:" + address + "</h2>" +  "<p> txid: " + str(utxo[0]) + "</p><p>  vout: " + str(utxo[1]) + "</p>" + "<p> " + str(raw) + "</p>"
    return (
        f"<h2>Adres konta: {address}</h2>\n"
        f"<p>Balance: {balance}</p>\n"
        f"<p>UTXO txid: {utxo[0]}</p>\n"
        f"<p>UTXO vout: {utxo[1]}</p>\n"
        f"<p>Raw change address: {raw}</p>\n"
        f"<p>Estimated fee rate: {estm_fee_rate}</p>\n"
        f"<p>Calculated fee: {fee}</p>\n"
        f"<p>Balance after fee: {balance_after_fee}</p>\n"
        f"<p>OP_RETURN data (string): {op_data_str}</p>\n"
        f"<p>OP_RETURN data (hex): {op_data_hex}</p>\n"
	f"<p>thhex: {txhex}<p>\n"
    )


def get_address_info():
    address_info = json.loads(subprocess.check_output(["bitcoin-cli", "-testnet", "-rpcwallet=testwallet", "listreceivedbyaddress", "0","true"]))
    return address_info[0] 


def get_utxo(address):
    utxo = json.loads(subprocess.check_output(["bitcoin-cli", "-testnet", "-rpcwallet=testwallet", "listunspent", "0", "99999", f'["{address}"]']))
    utxo = utxo[0]
    utxo_txid = utxo["txid"]
    utxo_vout = utxo["vout"]
    return utxo_txid,  utxo_vout


def generate_new_address(wallet_name="testwallet"):
    try:
        output = subprocess.check_output(["bitcoin-cli", "-testnet", "-rpcwallet=" + wallet_name, "getnewaddress"])
        new_address = output.decode("utf-8").strip()
        return new_address
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None


def create_raw_transaction(utxo_txid, utxo_vout, op_return_data, change_address, change_amount):
    # Construct the command
    command = [
        "bitcoin-cli", "-named", "createrawtransaction",
        f"inputs='[{\"txid\": \"{utxo_txid}\", \"vout\": {utxo_vout}}]'",
        f"outputs='{{\"data\": \"{op_return_data}\", \"{change_address}\": \"{change_amount}\"}}'"
    ]

    # Execute the command and capture the output
    rawtxhex = subprocess.check_output(command).decode('utf-8').strip()
	
    return rawtxhex


def get_raw_change_address():
   raw_change_address = subprocess.check_output(["bitcoin-cli", "-testnet", "-rpcwallet=testwallet", "getrawchangeaddress"])
   return raw_change_address

# Returns fee for a transaction based on tx size and current fee rate 
def calculate_fee(tx_size, feerate):
    return (feerate / 1000) * tx_size  # BTC


# Returns estimated fee based on number of blocks
# estimate fee rate in BTC/kB
def get_estimated_fee(blocks=6):
    result = subprocess.check_output(["bitcoin-cli", "-testnet", "estimatesmartfee", str(blocks)])
    fee_info = json.loads(result)
    return fee_info["feerate"]
