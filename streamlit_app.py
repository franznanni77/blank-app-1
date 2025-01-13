import streamlit as st
from openai_processing import process_receipts

def main():
    st.title("Image Text Extractor")
    st.write("Upload an image to extract text from it")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Add a button to process the image
        if st.button('Extract Text'):
            with st.spinner('Processing image...'):
                # Reset the file pointer to the beginning
                uploaded_file.seek(0)
                
                # Process the image
                result = extract_text_from_image(uploaded_file)

                if result:
                    # Display the extracted text
                    extracted_text = result.choices[0].message.content
                    st.write("### Extracted Text:")
                    st.write(extracted_text)
                else:
                    st.error("Failed to extract text from the image")

if __name__ == "__main__":
    main()