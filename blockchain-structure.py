import hashlib
import json
import time
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 4  # Mining difficulty
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
    
    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True
    
    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0'*self.difficulty) and 
                block_hash == block.compute_hash())
    
    def mine_pending_transactions(self, miner_reward_address):
        # Add mining reward transaction
        reward_tx = Transaction(
            "BANK_REWARD",
            miner_reward_address,
            1.0  # Mining reward amount
        )
        self.pending_transactions.append(reward_tx)
        
        block = Block(
            len(self.chain),
            self.pending_transactions,
            time.time(),
            self.last_block.hash
        )
        
        # Proof-of-Work
        proof = self.proof_of_work(block)
        
        self.add_block(block, proof)
        self.pending_transactions = []
    
    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0'*self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash
    
    @property
    def last_block(self):
        return self.chain[-1]
