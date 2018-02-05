import time

from block import Block
from transaction import Transaction


"""
Known limitations:
    - This currently has no transaction fees or block limits
    - Chain splits are not handled correctly
    - Transactions are not verified to ensure source account has appropriate coins
"""


def create_genesis_block(transactions):
    return Block(
        0,
        int(time.time()),
        transactions,
        0,
        0
    )


class BlockChain:
    def __init__(self, block_reward, target, mining_recipient):
        """Intialize a new blockchain with the specified settings.

        Settings parameters (a dictionary object):
        - block_reward - size of reward for mining
        - target - we have to find a hash result < this value to win the block
        """
        self.block_reward = block_reward
        self.target = target
        self.mining_recipient = mining_recipient

        self.blocks = []
        transactions = [Transaction(0, mining_recipient, block_reward)]
        self.blocks.append(create_genesis_block(transactions))
        self.account_balances = {mining_recipient: block_reward}

        self.transaction_pool = []

    def add_transaction(self, source, destination, amount, signature):
        """Add a transaction to the pool to be considered for inclusion into
        the next block.
        """
        try:
            transaction = Transaction(source, destination, amount, signature)
        except Exception:
            logging.warn('Invalid transaction received, ignoring')
            return
        self.transaction_pool.append(transaction)

    def select_transactions(self, reward_transaction):
        """Select a group of transactions to include in the block.

        In the future this will take gas prices, etc into account and verify
        account balances. We also need a way to keep transactions around in
        case a fork replaces our block.
        """
        transactions = [reward_transaction]
        while len(self.transaction_pool) > 0:
            transactions.append(self.transaction_pool.pop())
        return transactions

    def create_block(self, reward_transaction):
        """Create a new block with the specified transactions."""
        new_index = self.blocks[-1].index + 1
        now = int(time.time())
        previous_hash = self.blocks[-1].get_hash().hexdigest()

        # Get transactions from the pool for inclusion in the block
        transactions = self.select_transactions(reward_transaction)

        new_block = Block(new_index, now, transactions, previous_hash)
        new_block.find_nonce(self.target)
        self.import_block(new_block.get_json())

    def import_block(self, json_data):
        """Import an existing block that another node broadcast to us.
        
        Per the rules of the network, all blocks may contain 1 transaction (the
        first transaction) with `block_reward` tokens sent from address 0
        someone. This acts as the award for mining.
        """
        # Verify block and add it to the list
        previous_block = self.blocks[-1]
        assert json_data['index'] == previous_block.index + 1
        assert json_data['timestamp'] >= previous_block.timestamp
        assert json_data['previous_hash'] == previous_block.get_hash().hexdigest()
        new_block = Block(json_data['index'], json_data['timestamp'], json_data['transactions'], json_data['previous_hash'], nonce=json_data['nonce'])
        assert json_data['hash'] == new_block.get_hash().hexdigest()
        # TODO: Check transaction sources to make sure balances are valid
        self.blocks.append(new_block)

        # Update account balances
        for index, transaction in enumerate(new_block.transactions):
            self.account_balances[transaction.destination] += transaction.amount
            # Allow the first transaction to be the block reward
            if index == 0 and transaction.amount <= self.block_reward:
                continue
            self.account_balances[transaction.source] -= transaction.amount
