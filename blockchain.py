import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):

    def __init__(self):
        self.current_transaction=[]
        self.chain=[]

        self.new_block(previous_hash=1,proof=100)

    def new_block(self,proof,previous_hash=None):
        block={
            'index':len(self.chain)+1,
            'timestamp':time(),
            'transactions':self.current_transaction,
            'proof':proof,
            'previous_hash':previous_hash,

        }
        self.current_transaction=[]
        self.chain.append(block)
        return block

    def new_transaction(self,sender,recipient,amount):
        self.current_transaction.append({
            'sender':sender,
            'recipient':recipient,
            'amount':amount,
        })
        return self.last_block['index']+1

    # Instantiate our Node
    app = Flask(__name__)

    # Generate a globally unique address for this node
    node_identifier = str(uuid4()).replace('-', '')

    # Instantiate the Blockchain
    blockchain = Blockchain()




    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string=json.dump(block,sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @app.route('/mine', methods=['GET'])
    def mine():
        return "We'll mine a new Block"

    @app.route('/transactions/new', methods=['POST'])
    def new_transaction():
        return "We'll add a new transaction"

    @app.route('/chain', methods=['GET'])
    def full_chain():
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }
        return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



