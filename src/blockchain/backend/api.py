from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from blockchain.backend.blockchain.blockchain import Blockchain
from blockchain.backend.wallet.wallet import Wallet
from blockchain.backend.wallet.transaction import Transaction
from blockchain.backend.wallet.transaction_pool import TransactionPool

app = FastAPI(title="Blockchain API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()


class TransactRequest(BaseModel):
    recipient: str = Field(..., description="Recipient public address")
    amount: float = Field(..., gt=0, description="Amount to transfer")


@app.get("/")
@app.get("/api")
def root():
    return {
        "status": "healthy",
        "service": "Blockchain Node API",
        "blocks_count": len(blockchain.chain),
    }


@app.get("/blockchain")
@app.get("/api/blockchain")
def get_blockchain():
    return blockchain.to_json()


@app.get("/blockchain/length")
@app.get("/api/blockchain/length")
def get_blockchain_length():
    return len(blockchain.chain)


@app.post("/blockchain/mine")
@app.post("/api/blockchain/mine")
def mine_block():
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    blockchain.add_block(transaction_data)
    block = blockchain.latest_block
    transaction_pool.clear_blockchain_transactions(blockchain)
    return block.to_json()


@app.get("/wallet/info")
@app.get("/api/wallet/info")
def get_wallet_info():
    return {
        "address": wallet.address,
        "balance": wallet.balance,
        "public_key": wallet.public_key,
    }


@app.post("/wallet/transact")
@app.post("/api/wallet/transact")
def create_transaction(request: TransactRequest):
    transaction = transaction_pool.existing_transaction(wallet.address)

    try:
        if transaction:
            transaction.update(wallet, request.recipient, request.amount)
        else:
            transaction = Transaction(wallet, request.recipient, request.amount)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    transaction_pool.set_transaction(transaction)
    return transaction.to_json()


@app.get("/transactions/pool")
@app.get("/api/transactions/pool")
def get_transaction_pool():
    return transaction_pool.transaction_data()
