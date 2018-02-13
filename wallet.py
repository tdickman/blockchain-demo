import datetime
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA

import os.path
from pathlib import Path

from blockchain import BlockChain
from transaction import Transaction, generate_transaction
 

if __name__ == '__main__':
    # os.path.isfile(./wallet.bin)
    my_file = Path("./wallet.bin")
    if my_file.is_file():
        # Open wallet
        print("Wallet Found")
        password = input("Enter Password: ")
        with open('walletp.bin','r') as g:
            private_key = RSA.importKey(g.read(),  passphrase=password)
        with open('wallet.bin','r') as f:
            public_key = f.read()

    else:
        # Generate wallet keys
        print("New Wallet Created")
        password = input("Enter Password: ")
        private_key = RSA.generate(1024)
        pkey = private_key.exportKey(passphrase=password)
        public_key = private_key.publickey().exportKey().decode()
        with open('wallet.bin','w+') as f:
            f.write(public_key)
            print(f.read())
        with open('walletp.bin','wb') as g:
            g.write(pkey)

    #wallet commands
    command = input("Enter Command: ")
    while command.strip() != 'exit':
        if command.strip() == 'address':
            with open('wallet.bin','r') as f:
                print(f.read())

        elif command.strip() == 'help':
            print("Use any of the supported commands below:")
            print("help  - - - - - List possible commands")
            print("address - - - - Return account address" )
            print("mine  - - - - - Start mining" )
            print("balance - - - - Account balance" )
            print("exit  - - - - - Exit wallet")

        elif command.strip() == 'mine':

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

        elif command.strip() == 'balance':
            print(blockchain.account_balances)

        else:
            print("Error: Not supported command, type 'help' for list of supported commands")
        command = input("Enter Command: ")
