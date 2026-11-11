import time
import uuid

from blockchain.backend.config import MINING_REWARD, MINING_REWARD_INPUT
from blockchain.backend.wallet.wallet import Wallet


class Transaction:
    def __init__(
            self,
            sender_wallet=None,
            recipient=None,
            amount=None,
            id=None,
            output=None,
            input=None
    ):
        """
        Document an exchange in currency from a sender to one or more recipients.
        :param sender_wallet:
        :param recipient:
        :param amount:
        """
        self.id = id or str(uuid.uuid4())[:8]
        self.output = output or self.create_output(
            sender_wallet,
            recipient,
            amount
        )
        self.input = input or self.create_input(
            sender_wallet,
            self.output
        )

    def update(self, sender_wallet, recipient, amount):
        """
        Updates the transaction with an existing or new recipient.
        :param sender_wallet:
        :param recipient:
        :param amount:
        :return:
        """
        sender_address = sender_wallet.address
        if amount > self.output.get(sender_address, 0):
            raise Exception('Amount exceeds balance')

        self.output[recipient] = self.output.get(recipient, 0) + amount
        self.output[sender_address] -= amount

        self.input = self.create_input(sender_wallet, self.output)

    def to_json(self):
        """
        Serialize the transaction.
        Convert large signature integers into strings to prevent JSON serialization errors.
        :return:
        """
        return self.__dict__

    @staticmethod
    def from_json(transaction_json):
        """
        Deserialize a transaction's JSON.
        :param transaction_json:
        :return:
        """
        return Transaction(**transaction_json)

    @staticmethod
    def create_output(sender_wallet, recipient, amount):
        """
        Structure the output data for the transaction.
        :param sender_wallet:
        :param recipient:
        :param amount:
        :return:
        """
        if amount > sender_wallet.balance:
            raise Exception('Amount exceeds balance')

        return {
            recipient: amount,
            sender_wallet.address: sender_wallet.balance - amount
        }

    @staticmethod
    def create_input(sender_wallet, output):
        """
        Structure the input data for the transaction.
        Sign the transaction and includes the sender's public key and address.
        :param sender_wallet:
        :param output:
        :return:
        """
        return {
            'timestamp': time.time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output)
        }

    @staticmethod
    def is_transaction_valid(transaction):
        """
        Validates the transaction fields.
        Raises an exception if the transaction is invalid.
        :param transaction:
        :return:
        """
        if transaction.input == MINING_REWARD_INPUT:
            if list(transaction.output.values()) != [MINING_REWARD]:
                raise Exception('Invalid mining reward')
            return

        output_total = sum(transaction.output.values())
        if transaction.input['amount'] != output_total:
            raise Exception('Invalid transaction output values')

        if not Wallet.verify(
                transaction.input['public_key'],
                transaction.output,
                transaction.input['signature']
        ):
            raise Exception('Invalid signature')

    @staticmethod
    def reward_transaction(miner_wallet):
        """
        Generates a reward transaction that awards a miner for mining a block.
        :param miner_wallet:
        :return:
        """
        return Transaction(
            output={miner_wallet.address: MINING_REWARD},
            input=MINING_REWARD_INPUT
        )


def main():
    transaction = Transaction(Wallet(), 'recipient', 15)
    print(f'transaction.__dict__: {transaction.__dict__}\n')

    transaction_json = transaction.to_json()
    restored_transaction = Transaction.from_json(transaction_json)
    print(f'\nrestored_transaction.__dict__: {restored_transaction.__dict__}')


if __name__ == '__main__':
    main()
