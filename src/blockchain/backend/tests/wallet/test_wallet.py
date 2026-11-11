from blockchain.backend.blockchain.blockchain import Blockchain
from blockchain.backend.config import STARTING_BALANCE
from blockchain.backend.wallet.wallet import Wallet


def test_wallet_initialization():
    wallet = Wallet()
    assert wallet.address is not None
    assert len(wallet.address) == 16
    assert isinstance(wallet.public_key, str)
    assert wallet.public_key_pem == wallet.public_key
    assert wallet.balance == STARTING_BALANCE


def test_wallet_sign_and_verify_valid():
    wallet = Wallet()
    data = {'amount': 50, 'recipient': 'recipient-address'}
    signature = wallet.sign(data)

    assert Wallet.verify(wallet.public_key, data, signature) is True
    assert Wallet.verify(wallet.public_key.encode('utf-8'), data, signature) is True


def test_wallet_verify_invalid_signature():
    wallet1 = Wallet()
    wallet2 = Wallet()
    data = {'amount': 50, 'recipient': 'recipient-address'}
    signature = wallet1.sign(data)

    assert Wallet.verify(wallet2.public_key, data, signature) is False


def test_wallet_verify_modified_data():
    wallet = Wallet()
    data = {'amount': 50, 'recipient': 'recipient-address'}
    signature = wallet.sign(data)
    tampered_data = {'amount': 50, 'recipient': 'different-address'}

    assert Wallet.verify(wallet.public_key, tampered_data, signature) is False


def test_wallet_verify_malformed_key():
    wallet = Wallet()
    data = {'amount': 50}
    signature = wallet.sign(data)

    assert Wallet.verify('invalid-pem-key', data, signature) is False


def test_wallet_deterministic_json_keys():
    wallet = Wallet()
    data1 = {'a': 1, 'b': 2}
    data2 = {'b': 2, 'a': 1}
    signature = wallet.sign(data1)

    assert Wallet.verify(wallet.public_key, data2, signature) is True


def test_wallet_calculate_balance():
    blockchain = Blockchain()
    wallet = Wallet(blockchain)

    assert wallet.balance == STARTING_BALANCE

    # Block with transaction where wallet received funds
    received_tx = {
        'input': {'address': 'other-address'},
        'output': {wallet.address: 100, 'other-address': 900}
    }
    blockchain.add_block([received_tx])

    assert wallet.balance == STARTING_BALANCE + 100

    # Block with transaction where wallet sent funds (resets balance)
    sent_tx = {
        'input': {'address': wallet.address},
        'output': {wallet.address: 300, 'recipient': 800}
    }
    blockchain.add_block([sent_tx])

    assert wallet.balance == 300
