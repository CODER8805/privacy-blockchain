import requests

# The default API port for your local IPFS node
IPFS_API_URL = "http://127.0.0.1:5001/api/v0"

def upload_to_ipfs(data: bytes) -> str:
    """Uploads encrypted bytes to IPFS and returns the unique CID."""
    print("[*] Uploading encrypted data to IPFS...")
    # IPFS expects a file-like dictionary via the HTTP API
    response = requests.post(f"{IPFS_API_URL}/add", files={'file': data})
    
    if response.status_code == 200:
        cid = response.json()['Hash']
        print(f"    -> Success! Received CID: {cid}")
        return cid
    else:
        raise Exception(f"Failed to upload to IPFS: {response.text}")

def download_from_ipfs(cid: str) -> bytes:
    """Downloads a file from IPFS using its CID."""
    print(f"[*] Downloading CID {cid} from IPFS...")
    # 'cat' is the IPFS command to read the contents of a file
    response = requests.post(f"{IPFS_API_URL}/cat?arg={cid}")
    
    if response.status_code == 200:
        print("    -> Success! Data retrieved.")
        return response.content
    else:
        raise Exception(f"Failed to download from IPFS: {response.text}")

def test_ipfs():
    print("==========================================")
    print(" PHASE 7: IPFS UPLOAD & DOWNLOAD TEST     ")
    print("==========================================")
    
    # 1. Create fake encrypted data for the test
    fake_encrypted_data = b"0xABCDEF1234567890 (Pretend this is AES encrypted ciphertext)"
    
    # 2. Upload it to your real node
    cid = upload_to_ipfs(fake_encrypted_data)
    
    # 3. Download it back using the CID
    retrieved_data = download_from_ipfs(cid)
    
    # 4. Verify it matches perfectly
    print(f"\nOriginal Data : {fake_encrypted_data}")
    print(f"Retrieved Data: {retrieved_data}")
    
    if fake_encrypted_data == retrieved_data:
        print("\nRESULT: SUCCESS! IPFS storage pipeline is working.")
    else:
        print("\nRESULT: FAILED! Data mismatch.")

if __name__ == "__main__":
    test_ipfs()