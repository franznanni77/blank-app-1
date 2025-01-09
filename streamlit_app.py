import streamlit as st
from receipt_processor import process_receipts
import base64
from typing import List
import json

def convert_to_base64(file) -> str:
    return base64.b64encode(file.read()).decode('utf-8')

def main():
    st.title("Receipt Analyzer")
    
    uploaded_files = st.file_uploader("Upload receipts (max 10)", 
                                    type=['png', 'jpg', 'jpeg'],
                                    accept_multiple_files=True)
    
    if uploaded_files:
        if len(uploaded_files) > 10:
            st.error("Maximum 10 files allowed")
            return
            
        if st.button("Process Receipts"):
            with st.spinner("Processing..."):
                base64_images = [convert_to_base64(file) for file in uploaded_files]
                results = process_receipts(base64_images)
                
                for i, result in enumerate(results):
                    st.subheader(f"Receipt {i+1}")
                    st.json(result)
                
                json_str = json.dumps(results, indent=2)
                st.download_button(
                    "Download All Results",
                    json_str,
                    "receipt_results.json",
                    "application/json"
                )

if __name__ == "__main__":
    main()