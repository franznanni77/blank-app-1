import streamlit as st
import base64
import os
from PIL import Image
import io
from openai import OpenAI

def encode_image(image_file):
    """
    Encode the uploaded image file to base64
    """
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def extract_text_from_image(image_file):
    """
    Send the image to OpenAI API and get text extraction
    """
    # Get API key from environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        st.error("Please set the OPENAI_API_KEY environment variable")
        return None

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Encode the image
    base64_image = encode_image(image_file)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract all the text in this image. "
                                   "If there is a header or a footer, just ignore it. "
                                   "Extract tables as markdown tables. "
                                   "Don't use the subtitles for the list items, just return the list as text."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        return response
    except Exception as e:
        st.error(f"Error making request to OpenAI API: {str(e)}")
        return None

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