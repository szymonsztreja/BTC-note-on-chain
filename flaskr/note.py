from flask import (Flask, Blueprint, render_template, session, request, g, redirect, url_for)
from bitcoin.bitcoin_actions import (transaction_cost, get_address_info)
import requests
import subprocess
import json


bp = Blueprint('note', __name__, url_prefix='/note')


def get_balance():
    return  json.loads(subprocess.check_output(["bitcoin-cli", "-testnet", "-rpcwallet=testwallet", "getbalances"]))


@bp.route("/", methods=["GET", "POST"])
def note():
    if request.method == 'POST':
        note = request.form['note']

        error = None

        if len(note.encode('utf-8')) > 80:
            error = 'Incorrect note length (max 80 bytes).'


        if error is None:
            session.clear()
            user_id = note.encode().hex()
            session['user_id'] = user_id
            return redirect(url_for('note.wait_for_payment'))


        flash(error)

    elif request.method == 'GET':
        address_info = get_address_info()
        address = address_info["address"]

    return render_template('note/note.html', address=address)



from flask import jsonify

@bp.route("/calculate_transaction_cost", methods=["POST"])
def calculate_transaction_cost():
    note = request.form['note']
    # Call your Python function to calculate the transaction cost
    transaction_cost = calculate_transaction_cost(note)
    return jsonify(transaction_cost=transaction_cost)



@bp.route("/waiting")
def wait_for_payment():
    return render_template("note/wait_for_payment.html")


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



