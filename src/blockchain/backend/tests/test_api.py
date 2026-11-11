from fastapi.testclient import TestClient
from blockchain.backend.api import app, blockchain, wallet, transaction_pool

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_blockchain():
    response = client.get("/blockchain")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_blockchain_length():
    response = client.get("/blockchain/length")
    assert response.status_code == 200
    assert response.json() >= 1


def test_get_wallet_info():
    response = client.get("/wallet/info")
    assert response.status_code == 200
    data = response.json()
    assert "address" in data
    assert "balance" in data
    assert "public_key" in data


def test_transact_and_pool():
    recipient = "recipient-test-address"
    amount = 50.0

    response = client.post("/wallet/transact", json={"recipient": recipient, "amount": amount})
    assert response.status_code == 200
    tx_data = response.json()
    assert tx_data["output"][recipient] == amount

    pool_response = client.get("/transactions/pool")
    assert pool_response.status_code == 200
    assert len(pool_response.json()) >= 1


def test_mine_block():
    initial_length = len(blockchain.chain)
    response = client.post("/blockchain/mine")
    assert response.status_code == 200
    assert len(blockchain.chain) == initial_length + 1
    assert len(transaction_pool.transaction_map) == 0
