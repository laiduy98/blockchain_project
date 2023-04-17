import hashlib

# Implementation of a Merkle tree
class MerkleTree:
    # Initialize the Merkle tree with a list of transactions
    def __init__(self, transactions):
        # Store the list of transactions
        self.transactions = transactions
        # Calculate the SHA-256 hash of each transaction and store it in a list
        self.past_transaction = [hashlib.sha256(transaction.encode()).hexdigest() for transaction in transactions]
        self.current_transaction = []

        # Repeat the hash merging process until there is only one hash left
        while len(self.past_transaction) > 1:
            # If the number of hashes is odd, duplicate the last hash
            if len(self.past_transaction) % 2 != 0:
                self.past_transaction.append(self.past_transaction[-1])
            # Merge adjacent hashes by concatenating them and hashing the result
            for i in range(0, len(self.past_transaction), 2):
                transaction = self.past_transaction[i] + self.past_transaction[i+1]
                current = hashlib.sha256(transaction.encode()).hexdigest()
                self.current_transaction.append(current)
            # Update the list of hashes with the merged hashes
            self.past_transaction = self.current_transaction
            self.current_transaction = []

        # The root of the Merkle tree is the final hash
        self.root = self.past_transaction[0]

# Implementation of a Bitcoin client ledger using a Merkle tree
class Ledger:
    # Initialize the ledger with an empty list of transactions and a None Merkle tree
    def __init__(self):
        self.transactions = []
        self.tree = None

    # Add a new transaction to the ledger and update the Merkle tree
    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.tree = MerkleTree(self.transactions)

    # Verify if a transaction is present in the ledger
    def verify_transaction(self, transaction):
        return transaction in self.transactions

    # Verify the integrity of the ledger using the Merkle tree
    def verify_ledger(self):
        # If the Merkle tree is not initialized, the ledger is not valid
        if self.tree is None:
            return False
        # Calculate the SHA-256 hash of all the transactions and compare it with the root of the Merkle tree
        return self.tree.root == hashlib.sha256(''.join(self.transactions).encode()).hexdigest()
