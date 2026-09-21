import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

# Point to your keys directory
KEYS_DIR = os.path.join(os.path.dirname(__file__), "keys")

def load_private_key(node_name: str):
    """Loads a node's private key from the .pem file."""
    path = os.path.join(KEYS_DIR, f"{node_name}_private.pem")
    with open(path, "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None)

def load_public_key(node_name: str):
    """Loads a node's public key from the .pem file."""
    path = os.path.join(KEYS_DIR, f"{node_name}_public.pem")
    with open(path, "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())

def sign_data(private_key, data: bytes) -> bytes:
    """Creates a digital signature for the data."""
    signature = private_key.sign(
        data,
        ec.ECDSA(hashes.SHA256())
    )
    return signature

def verify_signature(public_key, signature: bytes, data: bytes) -> bool:
    """Verifies the signature. Returns True if valid, False if invalid."""
    if not signature:
        return False
    try:
        public_key.verify(
            signature,
            data,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        return False

def run_tests():
    print("==========================================")
    print(" PHASE 3: DIGITAL SIGNATURE SECURITY TESTS ")
    print("==========================================")
    
    # Load keys for Node A and Node B
    node_a_priv = load_private_key("node_a")
    node_a_pub = load_public_key("node_a")
    node_b_pub = load_public_key("node_b")
    
    original_data = b"Temperature = 30 C"
    tampered_data = b"Temperature = 100 C"
    
    print("\n[TEST 1] Genuine Update (Correct Data + Correct Signature)")
    signature = sign_data(node_a_priv, original_data)
    is_valid = verify_signature(node_a_pub, signature, original_data)
    print(f"Result: {'ACCEPT' if is_valid else 'REJECT'}")
    
    print("\n[TEST 2] Modified Data Attack (Tampered Data + Old Signature)")
    is_valid = verify_signature(node_a_pub, signature, tampered_data)
    print(f"Result: {'ACCEPT' if is_valid else 'REJECT'}")

    print("\n[TEST 3] Unsigned Update (Missing Signature)")
    is_valid = verify_signature(node_a_pub, b"", original_data)
    print(f"Result: {'ACCEPT' if is_valid else 'REJECT'}")

    print("\n[TEST 4] Wrong Signer (Signed by A, Verified by B)")
    is_valid = verify_signature(node_b_pub, signature, original_data)
    print(f"Result: {'ACCEPT' if is_valid else 'REJECT'}")
    
    print("\nSecurity testing complete.")

if __name__ == "__main__":
    run_tests()