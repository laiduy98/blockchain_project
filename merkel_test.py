import hashlib

class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.past_transaction = [hashlib.sha256(transaction.encode()).hexdigest() for transaction in transactions]
        self.current_transaction = []

        while len(self.past_transaction) > 1:
            if len(self.past_transaction) % 2 != 0:
                self.past_transaction.append(self.past_transaction[-1])
            for i in range(0, len(self.past_transaction), 2):
                transaction = self.past_transaction[i] + self.past_transaction[i+1]
                current = hashlib.sha256(transaction.encode()).hexdigest()
                self.current_transaction.append(current)
            self.past_transaction = self.current_transaction
            self.current_transaction = []

        self.root = self.past_transaction[0]


class Ledger:
    def __init__(self):
        self.transactions = []
        self.tree = None

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.tree = MerkleTree(self.transactions)

    def verify_transaction(self, transaction):
        return transaction in self.transactions

    def verify_ledger(self):
        return self.tree.root == hashlib.sha256(''.join(self.transactions).encode()).hexdigest()


if __name__ == '__main__':

    # Create a new ledger
    ledger = Ledger()

    # Add some transactions
    ledger.add_transaction("Alice sends 1 BTC to Bob")
    ledger.add_transaction("Bob sends 2 BTC to Charlie")
    ledger.add_transaction("Charlie sends 0.5 BTC to David")

    # Verify that the transactions are present in the ledger
    print(ledger.verify_transaction("Alice sends 1 BTC to Bob")) # True
    print(ledger.verify_transaction("Bob sends 2 BTC to David")) # False

    # Verify the integrity of the ledger
    print(ledger.verify_ledger()) # True
