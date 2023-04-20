import java.util.ArrayList;
import java.util.List;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

// Implementation of a Merkle tree
public class MerkleTree {
    private List<String> transactions;
    private List<String> pastTransaction;
    private List<String> currentTransaction;
    private String root;

    // Initialize the Merkle tree with a list of transactions
    public MerkleTree(List<String> transactions) {
        this.transactions = transactions;
        pastTransaction = new ArrayList<String>();
        currentTransaction = new ArrayList<String>();

        // Calculate the SHA-256 hash of each transaction and store it in a list
        for (String transaction : transactions) {
            pastTransaction.add(sha256(transaction));
        }

        // Repeat the hash merging process until there is only one hash left
        while (pastTransaction.size() > 1) {
            // If the number of hashes is odd, duplicate the last hash
            if (pastTransaction.size() % 2 != 0) {
                pastTransaction.add(pastTransaction.get(pastTransaction.size() - 1));
            }
            // Merge adjacent hashes by concatenating them and hashing the result
            for (int i = 0; i < pastTransaction.size(); i += 2) {
                String transaction = pastTransaction.get(i) + pastTransaction.get(i + 1);
                currentTransaction.add(sha256(transaction));
            }
            // Update the list of hashes with the merged hashes
            pastTransaction = new ArrayList<String>(currentTransaction);
            currentTransaction.clear();
        }

        // The root of the Merkle tree is the final hash
        root = pastTransaction.get(0);
    }

    // Calculate the SHA-256 hash of a string
    private String sha256(String input) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(input.getBytes());
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }

    // Get the root hash of the Merkle tree
    public String getRoot() {
        return root;
    }
}

// Implementation of a Bitcoin client ledger using a Merkle tree
public class Ledger {
    private List<String> transactions;
    private MerkleTree tree;

    // Initialize the ledger with an empty list of transactions and a null Merkle tree
    public Ledger() {
        transactions = new ArrayList<String>();
        tree = null;
    }

    // Add a new transaction to the ledger and update the Merkle tree
    public void addTransaction(String transaction) {
        transactions.add(transaction);
        tree = new MerkleTree(transactions);
    }

    // Verify if a transaction is present in the ledger
    public boolean verifyTransaction(String transaction) {
        return transactions.contains(transaction);
    }

    // Verify the integrity of the ledger using the Merkle tree
    public boolean verifyLedger() {
        // If the Merkle tree is not initialized, the ledger is not valid
        if (tree == null) {
            return false;
        }
        // Calculate the SHA-256 hash of all the transactions and compare it with the root of the Merkle tree
        StringBuilder allTransactions = new StringBuilder();
        for (String transaction : transactions) {
            allTransactions.append(transaction);
        }
        return tree.getRoot().equals(sha256(all
