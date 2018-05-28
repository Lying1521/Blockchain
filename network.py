import json
from uuid import uuid4

from flask import Flask, jsonify, request

import pow
from blockchain import Blockchain

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

block_chain = Blockchain()


def verify_only_one_rewards():
    pass


@app.route('/mine', methods=['GET'])
def mine():
    last_block = block_chain.last_block
    last_proof = last_block['proof']
    proof = pow.proof_of_work(last_proof)
    if last_block['previous_hash'] == block_chain.last_block['previous_hash']:

        block_chain.new_transactions(
            sender="0",
            receiver=node_identifier,
            msg="1",
        )

        block = block_chain.new_block(proof)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
            'last_proof': last_proof
        }
        block_chain.broadcast_block(response)
        return jsonify(response), 200
    else:
        return 'failure', 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'receiver', 'msg']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = block_chain.new_transactions(values['sender'], values['receiver'], values['msg'])

    response = {'message': 'Transaction will be added to Block '+str(index)}

    return jsonify(response), 201


@app.route('/broadcast/block',methods=['POST'])
def receive_broadcast_block():
    values = request.get_json()
    print(json.dumps(values))

    required = ['index', 'transactions', 'last_proof', 'message', 'previous_hash', 'proof']
    if not all(k in values for k in required):
        return 'Missing values', 400

    if not pow.valid_proof(int(values['last_proof']),int(values['proof'])):
        return 'Wrong proof', 400

    verify_only_one_rewards()

    if len(block_chain.chain)>values['index']:
        return 'update chain', 400
    elif len(block_chain.chain)<values['index']:
        block_chain.resolve_conflicts()
        block_chain.broadcast_block(values)

    res = {'message': 'Success to Create New Block'}

    return jsonify(res), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    print(request.remote_addr)
    print(request.host_url)
    print(request.url_root)
    print(request.base_url)
    response = {
        'chain': block_chain.chain,
        'length': len(block_chain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        block_chain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(block_chain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = block_chain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': block_chain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': block_chain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)