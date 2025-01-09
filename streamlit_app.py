import streamlit as st
from openai_processing import process_receipts

def main():
    st.title("Estrazione dati scontrini")

    st.write(
        """
        Carica da 2 a 10 file immagine di scontrini (jpeg, png, ecc.).
        Verrà chiamato il servizio di elaborazione per estrarre i dati e
        restituire un JSON di riepilogo.
        """
    )

    # Permetti il caricamento multiplo di file da 2 a 10
    uploaded_files = st.file_uploader(
        "Carica i tuoi scontrini",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    # Verifica quantità minima e massima di file
    if uploaded_files:
        if len(uploaded_files) < 2:
            st.warning("Devi caricare almeno 2 file.")
        elif len(uploaded_files) > 10:
            st.warning("Puoi caricare al massimo 10 file.")
        else:
            # Bottone per l'elaborazione
            if st.button("Elabora Scontrini"):
                with st.spinner("Elaborazione in corso..."):
                    output_json = process_receipts(uploaded_files)

                # Mostra i risultati
                st.subheader("Risultato dell'elaborazione:")
                st.json(output_json)

if __name__ == "__main__":
    main()
