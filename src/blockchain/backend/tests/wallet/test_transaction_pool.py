from blockchain.backend.blockchain.blockchain import Blockchain
from blockchain.backend.wallet.transaction import Transaction
from blockchain.backend.wallet.transaction_pool import TransactionPool
from blockchain.backend.wallet.wallet import Wallet


def test_set_transaction():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), 'recipient', 10)
    transaction_pool.set_transaction(transaction)

    assert transaction_pool.transaction_map[transaction.id] == transaction


def test_existing_transaction():
    transaction_pool = TransactionPool()
    wallet = Wallet()
    transaction = Transaction(wallet, 'recipient', 10)
    transaction_pool.set_transaction(transaction)

    found_transaction = transaction_pool.existing_transaction(wallet.address)
    assert found_transaction == transaction
    assert transaction_pool.existing_transaction('non_existent_address') is None


def test_transaction_data():
    transaction_pool = TransactionPool()
    transaction_1 = Transaction(Wallet(), 'recipient-1', 10)
    transaction_2 = Transaction(Wallet(), 'recipient-2', 20)

    transaction_pool.set_transaction(transaction_1)
    transaction_pool.set_transaction(transaction_2)

    data = transaction_pool.transaction_data()
    assert len(data) == 2
    assert transaction_1.to_json() in data
    assert transaction_2.to_json() in data


def test_clear_blockchain_transactions():
    transaction_pool = TransactionPool()
    transaction_1 = Transaction(Wallet(), 'recipient-1', 10)
    transaction_2 = Transaction(Wallet(), 'recipient-2', 20)

    transaction_pool.set_transaction(transaction_1)
    transaction_pool.set_transaction(transaction_2)

    blockchain = Blockchain()
    blockchain.add_block([transaction_1.to_json()])

    transaction_pool.clear_blockchain_transactions(blockchain)

    assert transaction_1.id not in transaction_pool.transaction_map
    assert transaction_2.id in transaction_pool.transaction_map
