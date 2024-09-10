import streamlit as st
import os
from groq import Groq

# Replace 'YOUR_API_KEY' with your actual Groq API key
api_key = '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'

# Initialize Groq client
client = Groq(api_key=api_key)

st.set_page_config(page_title="Audio to text", page_icon="pic.png")

# Streamlit App
st.title('AI Audio Analyzer')

st.write('Upload an audio file to transcribe it to text')

uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "m4a"])

if uploaded_file is not None:
    # Display the uploaded file
    st.audio(uploaded_file, format='audio/wav')
    
    if st.button('Transcribe'):
        # Save the uploaded file temporarily
        temp_filename = "temp_audio_file.m4a"
        with open(temp_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Read and process the audio file
        try:
            with open(temp_filename, "rb") as file:
                # Transcribe the audio file using the Groq API
                transcription = client.audio.transcriptions.create(
                    file=(temp_filename, file.read()),
                    model="whisper-large-v3",
                    prompt="Specify context or spelling",  # Optional
                    response_format="json",  # Optional
                    language="en",  # Optional
                    temperature=0.0  # Optional
                )
                st.write('Transcribed Text:')
                st.write(transcription.text)
        except Exception as e:
            st.error(f'Error: {str(e)}')
        finally:
            # Clean up the temporary file
            try:
                os.remove(temp_filename)
            except PermissionError:
                st.error(f'Could not delete temporary file: {temp_filename}. Please delete it manually.')
