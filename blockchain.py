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

    def new_transactions(self, sender, receiver, msg):
        self.current_transactions.append({
            'sender':sender,
            'receiver':receiver,
            'msg': msg
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

    @staticmethod
    def broadcast_transcation(tr):
        print(tr)

    def broadcast_block(self,block):
        for node in self.nodes:
            headers = {"Content-Type": "application/json"}
            res = requests.post(node+'/broadcast/block', data=json.dumps(block),headers=headers)
            if res.status_code == 201:
                return True

    def update_chain(self,url):
        response = requests.get(url+'chain')
        new_chain = None
        if response.status_code == 200:
            new_chain = response.json()['chain']
            print(new_chain)
        if new_chain:
            self.chain = new_chain

