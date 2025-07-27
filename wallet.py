#ECDSA
class Wallet:
    def __init__(self):
        self.private_key = ec.generate_private_key(ec.SECP256K1())
        self.public_key = self.private_key.public_key()
        self.address = self.generate_address()
    
    def generate_address(self):
        public_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return hashlib.sha256(public_bytes).hexdigest()[:40]
    
    def sign_transaction(self, transaction):
        transaction.signature = self.private_key.sign(
            transaction.get_plain_text().encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return transaction
