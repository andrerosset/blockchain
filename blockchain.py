"""
Created on Thu Jul 12 21:18:25 2018
@author: andre-rosset

Module 1 - Create a Blockchain

To be installed
Flask==0.12.2: pip install Flask==0.12.2
Postman HTTP Client: https://www.getpostman.com/

"""

#Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a Blackchain

# Class of Blockchain
class Blockchain:
    # Initializing the self class
    def __init__(self):
        # Creating the array attribute chain
        self.chain = []
        # Creating the funcion to create a block
        self.create_block(proof = 1, previous_hash = '0')
        
    # Initialing the function to create a block
    def create_block(self, proof, previous_hash):
        # Creating the dictionary variable block
        block = {'index': len(self.chain) + 1, 
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block
    
    # Creating a funcion to return the previous block of the chain
    def get_previou_block(self):
        # Returning the last inserted block of the chain
        return self.chain[-1]
    
    # Creating a function to resolve the proof of work
    def proof_of_work(self, previous_proof):
        # Creating the varible to store the new proof
        new_proof = 1
        # Creating the variable to check if the proof of work is solved
        check_proof = False
        # Creating the while to iterate the hash_operation variable to find the four leading zeros
        while check_proof is False:
            # Creating the hash sha 256 variable, with square os new_proof and previous_proof. 
            # The hexdigest() funcion outputs the entire hash string
            hash_operation = hashlib.sha3_256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # Checking if the hash_operation variable starts the four leading zeros
            if hash_operation[:4] == '0000':
                # If True, set the check_proof variable to True, stopping the while
                check_proof = True
            else:
                # If False, increment the new_proof variable + 1
                new_proof += 1
        # Returning the new_proof to later on, create the new block on the chain
        return new_proof
    
    # Creating the funciont to return the hash of the block
    def hash(self, block):
        # Creating and init the variable that encodes the block into a json format
        encoded_block = json.dumps(block, sort_keys = True).encode()
        # Returning the sha 256 encoded json block
        return hashlib.sha256(encoded_block).hexdigest()
    
    # Creating the function to validate if the chain is valid
    def is_chain_valid(self, chain):
        # Variable to keep the previous block, initialized with the first block of the chain
        previous_block = chain[0]
        # The index variable to control the while loop
        block_index = 1
        # Iterate while the block_index is smaller than the length of the chain
        while block_index < len(chain):
            # Variable to keep the current block of the chain
            block = chain[block_index]
            # Cheking if the previous hash key from current block is different from the previous hash key from the previous block
            if block['previous_hash'] != self.hash(previous_block):
                # If it's different, return False
                return False
            
            # Proof of the previous block
            previous_proof = previous_block['proof']
            # Proof of the current block
            proof = block['proof']
            # Hash operation between the proofs, encoded in string
            hash_operation = hashlib.sha3_256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            # Checking if the hash_operation start with the four leading zeros
            if hash_operation[:4] != '0000':
                # If not, return False
                return False
            # Set the previous block as the current block
            previous_block = block
            # Increment the block index to control the while loop
            block_index += 1
        return True            


# Part 2 - Mining our Blockchain

# Creating a Web App with Flask
app = Flask(__name__)

# Creating a Blockchain instance
blockchain = Blockchain()

# Creating a new Route to Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    # Getting the previous block
    previous_block = blockchain.get_previou_block()
    # Getting the previous proof from the previous block
    previous_proof = previous_block['proof']
    # Getting the current proof based on the previous proof
    proof = blockchain.proof_of_work(previous_proof)
    # Getting the hash from the previous block
    previous_hash = blockchain.hash(previous_block)
    # Creating a new block and returning the block
    block = blockchain.create_block(proof, previous_hash)
    # Creating the response
    response = {'messege': 'Congratulations, you just mined a block!',
                'index': block['index'], 
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    # Returning the response with the 200 (OK) http status
    return jsonify(response), 200
    
# Creating a new route to get the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    # Creating the response with the full chain and it length
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    # Returning the response with the 200 (OK) http status
    return jsonify(response), 200

# Creating a new route to check if the full chain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    # Getting the full chain
    chain = blockchain.chain
    # Checking if the chain is valid
    is_chain_valid = blockchain.is_chain_valid(chain)
    # Checking if the return variable is True
    if is_chain_valid:
        # Setting the messege for True
        response_str = 'All good. The Blockchain is valid.'
    else:
        # Setting the messege for False
        response_str = 'Houston, we have a problem. The Blockchain is not valid.'
    # Creatting the response
    response = {'message': response_str}
    # Returning the response with 200 (OK) http status
    return jsonify(response), 200

# Running the app with the localhost address (http://127.0.0.1:5000/)
app.run(host = '0.0.0.0', port = 5000)





