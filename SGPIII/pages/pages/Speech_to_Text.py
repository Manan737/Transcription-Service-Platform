import streamlit as st
import speech_recognition as sr

# Create a Streamlit UI
st.title("Real-Time Speech Recognition")

# Initialize the recognizer
r = sr.Recognizer()

# Create a button to start/stop recording
recording = st.button("Start Recording")

if recording:
    st.write("Recording...")
    
    # Initialize the microphone
    mic = sr.Microphone()
    
    # Open the microphone for recording
    with mic as source:
        audio = r.listen(source, timeout=None)  # Timeout set to None for continuous recording
    
    # Perform speech recognition
    try:
        text = r.recognize_google(audio)
        st.write("Transcription:")
        st.write(text)
    except sr.UnknownValueError:
        st.write("Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")

# Add an optional instructions text
st.markdown("### Instructions:")
st.write(
    "1. Click the 'Start Recording' button to begin recording your speech in real-time."
)

# st.write("2. Click the 'Stop Recording' button when you are done speaking.")
