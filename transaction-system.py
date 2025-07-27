from cryptography.hazmat.primitives import hashes

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
        self.signature = None
    
    def get_plain_text(self):
        return f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
    
    def is_valid(self):
        if self.sender == "BANK_REWARD":  # Mining reward
            return True
        
        # Verify signature
        try:
            public_key = serialization.load_pem_public_key(self.sender)
            public_key.verify(
                self.signature,
                self.get_plain_text().encode(),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except:
            return False
