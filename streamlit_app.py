import streamlit as st
from receipt_processor import process_receipts
import base64
import json
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

def convert_to_base64(file) -> str:
    return base64.b64encode(file.read()).decode('utf-8')

def main():
    st.title("Receipt Analyzer")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload receipts (max 10)", 
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True
    )
    
    if uploaded_files and st.button("Process Receipts"):
        try:
            # Converti le immagini in base64
            base64_images = []
            for file in uploaded_files:
                base64_image = convert_to_base64(file)
                base64_images.append(base64_image)
            
            # Processa le immagini
            results = process_receipts(base64_images)
            
            # Mostra i risultati
            for i, result in enumerate(results):
                st.subheader(f"Receipt {i+1}")
                st.json(result)
            
            # Bottone per il download
            json_str = json.dumps(results, indent=2)
            st.download_button(
                "Download All Results",
                json_str,
                "receipt_results.json",
                "application/json"
            )
                
        except Exception as e:
            st.error(f"Error during processing: {str(e)}")
            st.exception(e)  # Questo mostrerà il traceback completo

if __name__ == "__main__":
    main()