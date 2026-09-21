import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

def generate_aes_key() -> bytes:
    """Generates a secure 256-bit (32-byte) AES key."""
    # Note for Capstone: In a real system, this key is securely shared 
    # between authorized nodes using a protocol like Diffie-Hellman.
    # For this prototype, we generate it locally.
    return AESGCM.generate_key(bit_length=256)

def encrypt_data(aes_key: bytes, plaintext: bytes) -> bytes:
    """Encrypts data using AES-256-GCM and prepends the nonce."""
    aesgcm = AESGCM(aes_key)
    # GCM requires a unique 12-byte nonce (Number used ONCE) for every encryption
    nonce = os.urandom(12) 
    
    # Encrypt the plaintext. GCM automatically appends an authentication tag.
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)
    
    # We store the nonce and the ciphertext together so we can decrypt it later
    return nonce + ciphertext

def decrypt_data(aes_key: bytes, encrypted_data: bytes) -> bytes:
    """Extracts the nonce and decrypts the AES-256-GCM data."""
    # The first 12 bytes are the nonce, the rest is the ciphertext + tag
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]
    
    aesgcm = AESGCM(aes_key)
    # This will throw an InvalidTag exception if the ciphertext was tampered with
    return aesgcm.decrypt(nonce, ciphertext, associated_data=None)

def run_tests():
    print("==========================================")
    print(" PHASE 4: AES-256-GCM ENCRYPTION TESTS    ")
    print("==========================================")
    
    # 1. Setup
    original_data = b"CONFIDENTIAL: Patient Blood Pressure is 120/80."
    aes_key = generate_aes_key()
    
    # 2. Encrypt
    print("\n[TEST 1] Encryption and Decryption")
    print(f"Original Text: {original_data.decode('utf-8')}")
    encrypted_bytes = encrypt_data(aes_key, original_data)
    print(f"Encrypted (Hex): {encrypted_bytes.hex()[:60]}... (Unreadable!)")
    
    # 3. Decrypt
    decrypted_bytes = decrypt_data(aes_key, encrypted_bytes)
    print(f"Decrypted Text: {decrypted_bytes.decode('utf-8')}")
    print(f"Result: {'SUCCESS' if original_data == decrypted_bytes else 'FAILED'}")

    # 4. Tamper Test
    print("\n[TEST 2] Encrypted Data Tampering Attack")
    # Attacker flips a byte in the encrypted data
    tampered_bytes = bytearray(encrypted_bytes)
    tampered_bytes[15] = tampered_bytes[15] ^ 0xFF 
    
    try:
        decrypt_data(aes_key, bytes(tampered_bytes))
        print("Result: FAILED (System accepted tampered data!)")
    except InvalidTag:
        print("Result: SUCCESS (System caught the tampering and rejected decryption!)")

if __name__ == "__main__":
    run_tests()