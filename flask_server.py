from flask import Flask
import requests
import subprocess
import json

app = Flask(__name__)



def get_balance():
    return  json.loads(subprocess.check_output(["bitcoin-cli", "-testnet", "-rpcwallet=testwallet", "getbalances"]))


@app.route("/note")
def get_wallet():
    balance = get_balance()
    confirmed = balance["mine"]["trusted"]
    unconfirmed = balance["mine"]["untrusted_pending"]
    return "<h2>Adres konta: tb1q7nst4y7wccahqg5maqagg7vj9l5vwfa5ycqmv0</h2><p>" + str(confirmed) + " " + str(unconfirmed) +"</p>"


def create_raw_transaction(utxo_txid, utxo_vout, op_return_data, change_address, change_amount):
    # Construct the command
    command = [
        "bitcoin-cli", "-named", "createrawtransaction",
        f"inputs='[{{\"txid\": \"{utxo_txid}\", \"vout\": {utxo_vout}}}]'",
        f"outputs='{{\"data\": \"{op_return_data}\", \"{change_address}\": \"{change_amount}\"}}'"
    ]

    # Execute the command and capture the output
    rawtxhex = subprocess.check_output(command).decode('utf-8').strip()
	
    return rawtxhex


# Returns fee for a transaction based on tx size and current fee rate 
def calculate_fee(tx_size, feerate):
    return (feerate / 1000) * tx_size  # BTC


# Returns estimated fee based on number of blocks
# estimate fee rate in BTC/kB
def get_estimated_fee(num_of_blocks: blocks):
    result = subprocess.check_output(["bitcoin-cli", "-testnet", "estimatesmartfee", str(blocks)])
    fee_info = json.loads(result)
    return fee_info["feerate"]
