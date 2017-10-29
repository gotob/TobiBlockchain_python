import hashlib as hasher
import datetime
import json
from flask import Flask
from flask import request
from flask import jsonify



class Block():
    def __init__(self, index, data, prev_hash):
        self.index = index
        self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.data = data
        self.prev_hash = prev_hash
        self.blockHash = self.getHash()
    def getHash(self):
        sha = hasher.sha256()
        sha.update(str(self.index) +
                    str(self.time) +
                    str(self.data) +
                    str(self.prev_hash))
        return sha.hexdigest()
    def showHash(self):
        print self.blockHash
    def __str__(self):
        return str(self.data) + '\n' + self.blockHash

def createGenesisBlock():
    genesisData = {
          "from": "aaaaaa-random-key-a",
          "to": "bbbbbb-random-key-b",
          "amount": 7,
          "proof-of-work": 36
    }
    return Block(0, genesisData, '0')

def createNext(prev):
    thisIndex = prev.index + 1
    thisData = 'Sono il blocco ' + str(thisIndex)
    thisPrevHash = prev.blockHash
    return Block(thisIndex, thisData, thisPrevHash)

def proofOfWork(last_proof):
    incrementor = last_proof + 1
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    return incrementor

node = Flask(__name__)
this_node_transactions = []
miner_addr = 'ajnfkasjfkjshfkajsfhdkafshfuahszlvhfd'

nBlocks = 30
blockchain = [createGenesisBlock()]
prev_block = blockchain[0]


@node.route('/trans', methods=['POST'])
def transac():
    if request.method == 'POST':
        #per ogni richiesta di POST estraggo data dal json
        new_trans = request.get_json()
        this_node_transactions.append(new_trans)
        print 'New transaction'
        print "FROM: {}".format(new_txion['from'])
        print "TO: {}".format(new_txion['to'])
        print "AMOUNT: {}\n".format(new_txion['amount'])
        return 'Transaction went successfully\n'

@node.route('/mine', methods = ['GET'])
def mine():
    lastBlock = blockchain[len(blockchain) - 1]
    lastProof = lastBlock.data['proof-of-work']
    proof = proofOfWork(lastProof)
    this_node_transactions.append(
        {"from": "rete", "to": miner_addr, "amount": 1}
    )
    new_block_data = {
        'proof-of-work': proof,
        "transactions": list(this_node_transactions)
    }
    new_block_index = lastBlock.index + 1
    new_block_prevHash = lastBlock.blockHash
    #svuoto la lista delle transazioni di questo nodo
    this_node_transactions[:] = []

    bloccoMinato = Block(new_block_index, new_block_data, new_block_prevHash)
    blockchain.append(bloccoMinato)
    return json.dumps({
      "index": new_block_index,
      "time": str(bloccoMinato.time),
      "data": new_block_data,
      "hash": bloccoMinato.blockHash
      }) + "\n"

@node.route('/blocchi', methods=['GET'])
def get_blocchi():
    chain = blockchain
    for block in chain:
        block_index = str(block.index)
        block_time = str(block.time)
        block_data = str(block.data)
        block_hash = block.blockHash
        block = {
            "index": block_index,
            "time": block_time,
            "data": block_data,
            "hash": block_hash
        }
    #chain = json.dumps(chain)
    return jsonify(chain)
node.run()

##for i in range(nBlocks):
#    new_block = createNext(prev_block)
#    blockchain.append(new_block)
#    prev_block = new_block
#for i in blockchain:
#    print i
