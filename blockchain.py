import json
from time import time
import encryption as en
import requests
import pow


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)
        self.nodes = set()
        self.Isolated_block = []

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain)+1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transactions(self, sender, receiver, msg, sender_public_key, receiver_public_key, id, signature):
        self.current_transactions.append({
            'sender':sender,
            'receiver':receiver,
            'msg': msg,
            'id': id,
            'sender_public_key': sender_public_key,
            'receiver_public_key': receiver_public_key,
            'signature': signature
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block,sort_keys=True).encode()
        return en.sha_256(block_string).encode('hex')

    def register_node(self,address):
        self.nodes.add(address)

    def valid_chain(self, chain):

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.hash(last_block):
                return False

            if not pow.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)
        for node in neighbours:
            response = requests.get(node+'/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def broadcast_transcation(self,tr):
        for node in self.nodes:
            headers = {"Content-Type": "application/json"}
            res = requests.post(node+'/transactions/new', data=json.dumps(tr),headers=headers)
            if res.status_code == 201:
                return True

    def broadcast_block(self,block):
        for node in self.nodes:
            headers = {"Content-Type": "application/json"}
            res = requests.post(node+'/broadcast/block', data=json.dumps(block),headers=headers)
            if res.status_code == 201:
                return True

    def update_chain(self, block):
        new_block = {
            'index': block['index'],
            'timestamp': block['timestamp'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']
        }
        if block['previous_hash'] == hash(self.last_block()):
            self.chain.append(new_block)
            for k in self.Isolated_block:
                if k['previous_hash'] == self.hash(self.last_block()):
                    self.chain.append(k)
        else:
            self.Isolated_block.append(new_block)

    def update_current_transcations(self, block):
        read_in_trascations = block['transacations']
        for k in read_in_trascations:
            for m in self.current_transactions:
                if m['id'] == k['id']:
                    self.current_transactions.remove(m)


