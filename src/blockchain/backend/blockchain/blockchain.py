import blockchain
from blockchain.backend.blockchain.block import Block


class Blockchain:
    """
    Blockchain: is a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions.
    """

    def __init__(self):
        self.chain = [Block.genesis()]

    def __repr__(self):
        return f"Blockchain: {self.chain}"

    def create_genesis_block(self):
        """Generates the initial block in the blockchain."""
        genesis_block = Block.genesis()
        self.chain.append(genesis_block)

    @property
    def latest_block(self):
        """Returns the last block in the blockchain."""
        return self.chain[-1]

    def add_block(self, data)->None:
        """Creates, mines, and appends a new block to the chain"""
        self.chain.append(Block.mine_block(self.latest_block, data))

    def replace_chain(self, chain):
        """
        Replaces the local chain with the incoming one if the following applies:
            - The incoming chain is longer than the local one.
            - The incoming chain is valid.
        :param chain:
        :return:
        """
        if len(chain) <= len(self.chain):
            raise Exception("Cannot replace. Incoming chain must be longer")

        try:
            Blockchain.is_chain_valid(chain)
        except Exception as e:
            raise Exception(f"Cannot replace. Incoming chain is invalid: {e}")

        self.chain = chain

    def to_json(self):
        """
        Serializes the blockchain into a list of blocks.
        :return:
        """
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        """
        Deserializes a list of serialized blocks into a blockchain instance.
        The result will contain a list of Block instances.
        :param chain_json:
        :return:
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block_json: Block.from_json(block_json), chain_json))
        return blockchain

    @staticmethod
    def is_chain_valid(chain):
        """
        Validates the incoming chain.
        Enforce the following conditions:
            - The chain must start with the genesis block.
            - Blocks must be formatted correctly.
        :param chain:
        :return:
        """
        if chain[0] != Block.genesis():
            raise Exception("The chain must start with the genesis block")

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_block_valid(last_block, block)



def main():
    blockchain = Blockchain()

    blockchain.add_block("foo")
    blockchain.add_block("bar")

    print(blockchain)
    print(f"blockchain.py __name__: {__name__}")


if __name__ == "__main__":
    main()
