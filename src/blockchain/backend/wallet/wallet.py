import hashlib
import json
from typing import Any, Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_dss_signature,
    encode_dss_signature,
)

from blockchain.backend.config import STARTING_BALANCE


class Wallet:
    """
    An individual wallet for a miner or participant.
    Manages cryptographic keys, transaction signing, and balance queries.
    """

    def __init__(self, blockchain=None):
        self.blockchain = blockchain
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(),
            default_backend()
        )
        self.public_key = self._serialize_public_key(self.private_key.public_key())
        self.public_key_pem = self.public_key
        self.address = self._generate_address(self.public_key_pem)

    @staticmethod
    def _serialize_public_key(public_key: ec.EllipticCurvePublicKey) -> str:
        """
        Serialize an EllipticCurvePublicKey into a PEM formatted string.
        """
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

    def serialize_public_key(self):
        """
        Reset the public key to its serialized version.
        """
        self.public_key = self._serialize_public_key(self.private_key.public_key())
        self.public_key_pem = self.public_key

    @staticmethod
    def _generate_address(public_key_pem: str) -> str:
        """
        Derive address deterministically from the public key.
        """
        return hashlib.sha256(public_key_pem.encode('utf-8')).hexdigest()[:16]

    @property
    def balance(self) -> float:
        return Wallet.calculate_balance(self.blockchain, self.address)

    def sign(self, data: Any) -> Tuple[int, int]:
        """
        Generate a deterministic signature for data using the private key.
        """
        encoded_data = json.dumps(data, sort_keys=True).encode('utf-8')
        return decode_dss_signature(
            self.private_key.sign(
                encoded_data,
                ec.ECDSA(hashes.SHA256())
            )
        )

    @staticmethod
    def verify(public_key: str | bytes, data: Any, signature: Tuple[int, int]) -> bool:
        """
        Safely verify a signature against original data and PEM public key.
        """
        try:
            if isinstance(public_key, str):
                public_key_bytes = public_key.encode('utf-8')
            elif isinstance(public_key, bytes):
                public_key_bytes = public_key
            else:
                return False

            deserialized_public_key = serialization.load_pem_public_key(
                public_key_bytes,
                default_backend()
            )

            if not isinstance(deserialized_public_key, ec.EllipticCurvePublicKey):
                return False

            r, s = signature
            encoded_data = json.dumps(data, sort_keys=True).encode('utf-8')

            deserialized_public_key.verify(
                encode_dss_signature(r, s),
                encoded_data,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except (InvalidSignature, ValueError, TypeError, Exception):
            return False

    @staticmethod
    def calculate_balance(blockchain, address: str) -> float:
        """
        Calculate address balance from blockchain transaction history.
        """
        balance = STARTING_BALANCE

        if not blockchain:
            return balance

        for block in blockchain.chain:
            for transaction in block.data:
                if isinstance(transaction, dict):
                    if transaction.get('input', {}).get('address') == address:
                        # Any time the address conducts a new transaction,
                        # it resets its balance
                        balance = transaction.get('output', {}).get(address, 0)
                    elif address in transaction.get('output', {}):
                        balance += transaction['output'][address]

        return balance


def main():
    wallet = Wallet()
    print(f'wallet.__dict__: {wallet.__dict__}')

    data = {'foo': 'bar'}
    signature = wallet.sign(data)
    print(f'signature: {signature}')

    should_be_valid = Wallet.verify(wallet.public_key, data, signature)
    print(f'should_be_valid: {should_be_valid}')

    should_be_invalid = Wallet.verify(Wallet().public_key, data, signature)
    print(f'should_be_invalid: {should_be_invalid}')


if __name__ == '__main__':
    main()
