from flask import Flask, jsonify, request
app = Flask(__name__)
bank = BankingApp()

@app.route('/create_account', methods=['POST'])
def create_account():
    username = request.json['username']
    address = bank.create_account(username)
    return jsonify({"address": address})

@app.route('/transfer', methods=['POST'])
def transfer():
    sender = bank.wallets[request.json['username']]
    recipient = request.json['recipient']
    amount = request.json['amount']
    success = bank.transfer(sender, recipient, amount)
    return jsonify({"success": success})

@app.route('/mine', methods=['POST'])
def mine():
    miner_address = bank.wallets[request.json['username']].address
    bank.blockchain.mine_pending_transactions(miner_address)
    bank.update_balances()
    return jsonify({"message": "New block mined"})

@app.route('/balance', methods=['GET'])
def balance():
    address = bank.wallets[request.json['username']].address
    return jsonify({"balance": bank.balances.get(address, 0)})
