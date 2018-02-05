import hashlib
import json
from Crypto.Hash import SHA256


MAX_NONCE = (2 ** 32) - 1  # 32 bit integer


class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, nonce=0):
        """Create a block.

        Args:
        - index - a value that increments for each block, starting at 0 for the genesis block
        - timestamp - epoch integer representing the current time
        - data - a string representing some data that is being stored in the block
        - previous_hash - hash of the previous block
        - nonce - a 32 bit number 
        """
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce

    def get_hash(self):
        digest = SHA256.new()
        digest.update(''.join([
            str(self.index),
            str(self.timestamp),
            ''.join([str(t.get_hash().digest()) for t in self.transactions]),
            str(self.previous_hash),
            str(self.nonce)
        ]).encode())
        return digest

    def find_nonce(self, target):
        """Find the block nonce given the specified target hash.

        This is the 'mining' operation that nodes perform in
        order to be able to mine blocks.
        """
        # If the target is too low we will need to increment an 'extra nonce'
        # in the merkle tree, or increase the size of the nonce
        # print('Current target: {0:0256b}'.format(target))
        for i in range(MAX_NONCE):
            self.nonce = i
            if int(self.get_hash().hexdigest(), 16) | target == target:
                # print('Target hash found: {0:0256b}'.format(int(self.get_hash(), 16)))
                return
        raise Exception('Failed to find a hash match. Need to increase nonce size, or implement extra nonce')

    def get_json(self):
        """Get json formatted representation of the block.

        In a real system this would be serialized and sent as bytes to save
        space, but we send it as a json string to make it simpler to
        understand.
        """
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'hash': self.get_hash().hexdigest(),
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
