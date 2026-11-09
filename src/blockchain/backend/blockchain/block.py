import time

from blockchain.backend.config import MINE_RATE
from ...backend.utils.crypto_hash import crypto_hash
from ...backend.utils.hex_to_binary import hex_to_binary

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}


class Block:
    """
    Block: unit of storage.
    Store transactions in a block and add them to the blockchain.
    """

    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        """
        Serialize the block into a dictionary of its attributes
        :return: A dictionary of the block instance variables
        """
        return self.__dict__

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data, until a block hash
        is found that meets the leading 0's proof of work requirement.
        :param last_block:
        :param data:
        :return:
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def from_json(block_json):
        """
        Deserializes a block's JSON representation back into a block instance.
        :param block_json:
        :return:
        """
        return Block(**block_json)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate the adjusted difficulty according to the MINE_RATE.
            - Increase the difficulty for quickly mined blocks.
            - Decrease the difficulty for slowly mined blocks.
        :param last_block:
        :param new_timestamp:
        :return:
        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def is_block_valid(last_block, block):
        """
        Validates a given block according to the following rules:
            - The block must have the proper last_hash reference
            - The block must meet the proof of work requirement
            - The difficulty must only adjust by 1
            - The block hash must be a valid combination of the block fields
        :param last_block:
        :param block:
        :return:
        """
        if block.last_hash != last_block.hash:
            raise Exception('The block must have the proper last_hash reference')

        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('The block must meet the proof of work requirement')

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('The difficulty must only adjust by 1')

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.nonce,
            block.difficulty
        )

        if block.hash != reconstructed_hash:
            raise Exception('The block hash must be correct')

    @staticmethod
    def genesis():
        """
        Generates the genesis block.
        :return:
        """
        return Block(**GENESIS_DATA)


def main():
    genesis_block = Block.genesis()
    bad_block = Block.mine_block(genesis_block, 'foo')
    bad_block.last_hash = 'evil_data'

    try:
        Block.is_block_valid(genesis_block, bad_block)
    except Exception as e:
        print(f'is_block_valid: {e}')



if __name__ == "__main__":
    main()
