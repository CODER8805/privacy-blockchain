import streamlit as st
import encryption
import signatures
import ipfs_manager

# Page configuration
st.set_page_config(page_title="Secure Off-Chain Storage", layout="centered")

st.title("🛡️ Secure Off-Chain Storage Pipeline")
st.markdown("Capstone Review 2 Demo: Cryptography & IPFS Integration")
st.divider()

# Input Section
st.header("1. Input Sensitive Data")
user_data = st.text_area("Enter patient data or sensitive logs:", "CONFIDENTIAL: Patient ID 4059 - Diagnosis: Type 2 Diabetes")

if st.button("Run Security Pipeline"):
    with st.spinner("Processing..."):
        
        # --- ENCRYPTION ---
        st.subheader("2. Encryption (AES-256-GCM)")
        aes_key = encryption.generate_aes_key()
        encrypted_data = encryption.encrypt_data(aes_key, user_data.encode())
        st.success("Data successfully encrypted!")
        st.code(f"AES Key (Hex): {aes_key.hex()}", language="text")
        st.code(f"Ciphertext (Hex): {encrypted_data.hex()[:80]}...", language="text")
        
        # --- DIGITAL SIGNATURE ---
        st.subheader("3. Digital Signature (SECP256K1)")
        # Load existing keys for 'node_a' exactly as defined in your signatures.py
        private_key = signatures.load_private_key("node_a")
        public_key = signatures.load_public_key("node_a")
        
        signature = signatures.sign_data(private_key, encrypted_data)
        st.success("Node A identity loaded and data signed!")
        st.code(f"Signature: {signature.hex()[:80]}...", language="text")
        
        # --- IPFS UPLOAD ---
        st.subheader("4. IPFS Upload")
        st.info("Uploading encrypted package to the decentralized IPFS network...")
        cid = ipfs_manager.upload_to_ipfs(encrypted_data)
        st.success(f"File stored on IPFS! Received CID: {cid}")
        
        st.divider()
        
        # --- RETRIEVAL & DECRYPTION ---
        st.header("5. Retrieval & Verification")
        st.info(f"Downloading file from IPFS using CID: {cid}")
        retrieved_data = ipfs_manager.download_from_ipfs(cid)
        
        # Verify the signature using your specific argument order
        is_valid = signatures.verify_signature(public_key, signature, retrieved_data)
        
        if is_valid:
            st.success("Signature Verified: Data is authentic and unaltered.")
            decrypted_data = encryption.decrypt_data(aes_key, retrieved_data).decode()
            st.code(f"Decrypted Data: {decrypted_data}", language="text")
            st.balloons()
        else:
            st.error("SECURITY ALERT: Signature verification failed. Data was tampered with!")