from blockchain.backend.blockchain.block import Block

class Blockchain:
    """
    Blockchain: is a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions.
    """
    def __init__(self):
        self.chain = [Block.genesis()]




def main():
    print(f"Hello, from {__name__}")

if __name__ == "__main__":
    main()