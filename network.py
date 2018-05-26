from uuid import uuid4
from flask import Flask,jsonify,request
from blockchain import Blockchain
import pow

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

block_chain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = block_chain.last_block
    last_proof = last_block['proof']
    proof = pow.proof_of_work(last_proof)

    block_chain.new_transactions(
        sender="0",
        receiver=node_identifier,
        msg="rewards",
    )

    # Forge the new Block by adding it to the chain
    block = block_chain.new_block(proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'receiver', 'msg']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = block_chain.new_transaction(values['sender'], values['receiver'], values['msg'])

    response = {'message': 'Transaction will be added to Block '+index}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': block_chain.chain,
        'length': len(block_chain.chain),
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)