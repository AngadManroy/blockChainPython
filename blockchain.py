import datetime
import hashlib
import json
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        self.chain = []
        self.createBlock(proof = 1,pvsHash = '0')# cz sha256 takes only strings
        
    def createBlock(self, proof, pvsHash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof, 
                 'prevHash': pvsHash
                 }
        self.chain.append(block)
        return block
    
    def getPvsBlock(self):
        return self.chain[-1]
    #POW a number that is hard to find but easy to mine
    
    def proofOfWork(self, pvsProof):
        newProof = 1#increment this in every iteration
        checkProof = False
        while checkProof is False:
            #4 leading zeroes, nonsymmetric function
            hashOperation = hashlib.sha256(str(newProof**2 - pvsProof**2).encode()).hexdigest()
            #.encode() -> b'5', checking if first 4 digits are 0
            if hashOperation[0:4] == '0000':
                checkProof = True
            else:
                newProof+=1 #increment till newProof is found
        return newProof
    
    #check if each block has corrcet POw(4 zeroes) & each pvshash = current hash
    
    def hash(self, block):
        encodedBlock = json.dumps(block, sort_keys= True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()
    
    def isChainValid(self, chain):
        pvsBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            if block['prevHash'] != self.hash(pvsBlock):
                return False
            pvsProof = pvsBlock['proof']
            proof = block['proof']
            hashOperation = hashlib.sha256(str(proof**2 - pvsProof**2).encode()).hexdigest()
            if hashOperation[:4] != '0000':
                return False
            pvsBlock = block
            blockIndex+=1
        return True
    
#Mining the Blockchain

#Create a Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

#Creating a blockchain
blockchain = Blockchain()

#Mining a block
@app.route('/mine_block', methods=['GET'])

def mine_block():
    pvsBlock = blockchain.getPvsBlock()
    pvsProof = pvsBlock['proof']
    proof = blockchain.proofOfWork(pvsProof)
    pvsHash = blockchain.hash(pvsBlock)
    block = blockchain.createBlock(proof, pvsHash)
    response = {'method':'Congratulations you just mines a block',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'prevHash': block['prevHash']}
    return jsonify(response), 200

#Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response= {'chain': blockchain.chain,
               'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/check', methods = ['GET'])
def check():
    response= {'Good':"Good"}
    return jsonify(response), 200

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    isValid = blockchain.isChainValid(blockchain.chain)
    if isValid:
        response = {'message': "All good, blockchain is valid"}
    else:
        response = {'message': "Houseton, we have a problem"}
    return jsonify(response), 200

#Running the App
app.run(host = '0.0.0.0', port = 5000)
