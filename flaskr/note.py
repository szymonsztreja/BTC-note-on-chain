from flask import (Flask, Blueprint, render_template, session, request, g, redirect, url_for, jsonify)
from bitcoin.bitcoin_actions import (transaction_cost, get_address_info, get_utxo, get_balance,  generate_new_address, transaction_brutto,create_raw_transaction, sign_transaction, send_transaction)
import requests
import subprocess
import json


bp = Blueprint('note', __name__, url_prefix='/note')



@bp.route("/", methods=["GET", "POST"])
def note():
    if request.method == 'POST':
        note = request.form['note']
        amount_to_pay = request.form['transaction_cost']
        address = request.form["address"]
        error = None

        if len(note.encode('utf-8')) > 80:
            error = 'Incorrect note length (max 80 bytes).'


        if error is None:
            session.clear()
            user_id = note.encode().hex()
            session['user_id'] = user_id
            session["amount_to_pay"] = amount_to_pay
            session["address"] = address
            session["note"] = note
            print(amount_to_pay)
            return redirect(url_for('note.wait_for_payment'))


        flash(error)

    elif request.method == 'GET':
        address_info = get_address_info()
        address = address_info["address"]
        #address = generate_new_address()

    return render_template('note/note.html', address=address)


@bp.route("/success", methods=["GET"])
def success():
    address = session["address"]
    note = session["note"]
    balance = get_balance(address)
    balance_after_fee = balance - transaction_cost(note)
    op_data_hex = note.encode().hex()
    utxo_txid,  utxo_vout = get_utxo(address)
    txhex = create_raw_transaction(utxo_txid, utxo_vout, op_data_hex, address, balance_after_fee)
    signed_hex = sign_transaction(txhex)
    send_hex = send_transaction(signed_hex)
    return render_template('note/success.html', send_hex=send_hex)


@bp.route("/tx_cost", methods=["POST"])
def calculate_transaction_cost():
    jsonData = request.get_json()
    note = jsonData["note"]
    tx_cost = transaction_brutto(note)
    return jsonify(tx_cost=tx_cost)


@bp.route("/get_utxo", methods=["GET"])
def check_payment():
    address = session["address"]
    total_recived = get_balance(address)
    return jsonify(total_recived=total_recived)


@bp.route("/waiting")
def wait_for_payment():
    amount_to_pay = session["amount_to_pay"]
    address = session["address"]
    return render_template("note/wait_for_payment.html",amount_to_pay=amount_to_pay, address=address)


@bp.route('/quit_session')
def quit_session():
    session.clear()
    return redirect(url_for('note.note'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = {'user_id': user_id}



