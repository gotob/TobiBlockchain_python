import hashlib as hasher
import datetime
import json
import flask

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
    return Block(0, 'ciao', '0')

def createNext(prev):
    thisIndex = prev.index + 1
    thisData = 'Sono il blocco ' + str(thisIndex)
    thisPrevHash = prev.blockHash
    return Block(thisIndex, thisData, thisPrevHash)

nBlocks = 30
blockchain = [createGenesisBlock()]
prev_block = blockchain[0]
for i in range(nBlocks):
    new_block = createNext(prev_block)
    blockchain.append(new_block)
    prev_block = new_block
for i in blockchain:
    print i
