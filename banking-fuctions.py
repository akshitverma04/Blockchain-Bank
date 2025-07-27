class BankingApp:
    def __init__(self):
        self.blockchain = Blockchain()
        self.wallets = {}  # username: Wallet object
        self.balances = {}  # address: balance
    
    def create_account(self, username):
        wallet = Wallet()
        self.wallets[username] = wallet
        self.balances[wallet.address] = 0.0
        return wallet.address
    
    def transfer(self, sender, recipient_address, amount):
        if self.balances.get(sender.address, 0) < amount:
            return False
        
        tx = Transaction(sender.address, recipient_address, amount)
        signed_tx = sender.sign_transaction(tx)
        
        if signed_tx.is_valid():
            self.blockchain.pending_transactions.append(signed_tx)
            return True
        return False
    
    def update_balances(self):
        # Scan blockchain to calculate balances
        balances = {}
        for block in self.blockchain.chain:
            for tx in block.transactions:
                # Handle sender
                if tx.sender != "BANK_REWARD":
                    balances[tx.sender] = balances.get(tx.sender, 0) - tx.amount
                # Handle recipient
                balances[tx.recipient] = balances.get(tx.recipient, 0) + tx.amount
        self.balances = balances
