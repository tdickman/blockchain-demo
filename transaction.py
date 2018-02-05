import hashlib
import json
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5


class Transaction:
    def __init__(self, source, destination, amount, signature=None):
        self.source = source
        self.destination = destination
        self.amount = amount
        self.signature = signature
        if signature:
            self.verify()

    def __repr__(self):
        return json.dumps(self.__dict__)

    def verify(self):
        """Make sure the signature matches the public key of the source."""
        verifier = PKCS1_v1_5.new(self.source)
        assert self.signature == verifier.verify(self.get_hash(), self.signature)

    def get_hash(self):
        digest = SHA256.new()
        digest.update(''.join([
            str(self.source),
            str(self.destination),
            str(self.amount)
        ]).encode())
        return digest


def generate_transaction(source, destination, amount, private_key):
    """Create a new transaction and sign it with our public key."""
    transaction = Transaction(source, destination, amount)
    transaction_hash = transaction.get_hash()
    signer = PKCS1_v1_5.new(private_key)
    transaction.signature = signer.sign(transaction_hash).hex()
    return transaction
