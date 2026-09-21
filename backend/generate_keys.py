import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# Define where to save the keys
KEYS_DIR = os.path.join(os.path.dirname(__file__), "keys")

def generate_node_identity(node_name: str):
    print(f"[*] Generating keys for {node_name}...")
    
    # 1. Generate private key
    private_key = ec.generate_private_key(ec.SECP256K1())
    # 2. Extract public key
    public_key = private_key.public_key()
    
    # 3. Format private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # 4. Format public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # 5. Save to files
    with open(os.path.join(KEYS_DIR, f"{node_name}_private.pem"), "wb") as f:
        f.write(private_pem)
    with open(os.path.join(KEYS_DIR, f"{node_name}_public.pem"), "wb") as f:
        f.write(public_pem)
        
    print(f"    -> Saved {node_name} keys to /keys folder.")

def main():
    print("========================================")
    print(" PHASE 2: GENERATING NODE IDENTITIES   ")
    print("========================================")
    # Generate keys for Node A and Node B
    generate_node_identity("node_a")
    generate_node_identity("node_b")
    print("\nComplete!")

if __name__ == "__main__":
    main()