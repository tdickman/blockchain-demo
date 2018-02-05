import datetime
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA

from blockchain import BlockChain
from transaction import Transaction, generate_transaction


if __name__ == '__main__':
    # Generate our keys
    private_key = RSA.generate(1024)
    public_key = private_key.publickey().exportKey().decode()

    # Setup our blockchain
    leading_zeros = 10
    blockchain = BlockChain(100, (2 ** (256 - leading_zeros)) - 1, public_key)

    # Add some blocks
    transaction = generate_transaction(0, public_key, 100, private_key)
    blockchain.create_block(transaction)
    transaction = generate_transaction(0, public_key, 100, private_key)
    blockchain.create_block(transaction)
    print(blockchain.blocks[0].get_json())
    print(blockchain.blocks[1].get_json())
    print(blockchain.blocks[2].get_json())
    print(blockchain.account_balances)
