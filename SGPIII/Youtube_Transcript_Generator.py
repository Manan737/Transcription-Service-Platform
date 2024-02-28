import streamlit as st
import os
import ffmpeg
import whisper
import os
import glob
from pytube import YouTube
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
import streamlit as st
import googletrans
import streamlit as st
from googletrans import Translator
import speech_recognition as sr
from transformers import pipeline
import sqlite3
import pyperclip

conn = sqlite3.connect('data.db')
c = conn.cursor()
yt_text1=""
folder_path = "/Users/mananshah/Desktop/SGPIII"
menu = ["YouTube Transcript Generator","Text Summarizer","Language Translation",'Speech To Text',"Previous YouTube Transcripts","Previous Summarizations","Previous Translations","Previous Dictations"]
choice = st.sidebar.selectbox("Select Appropriate Tool",menu)
translator = Translator()
# Function to download a video from YouTube
def download_video_mp4(youtube_url):
    # Create a YouTube object
    yt = YouTube(youtube_url)

    # Get the video with the highest resolution and file size
    video = yt.streams.filter(progressive=True,file_extension='mp4').order_by('resolution').desc().first()
    
    # Download the video to the current working directory
    video.download()

    st.write('Video downloaded!')

# Function to create an audio file from the video
def create_audio_file(video_filename):
    # Use ffmpeg to extract the audio track from the video and create an .mp4 audio file
    audio_filename = video_filename.replace(".mp4", ".mp3")
    stream = ffmpeg.input(video_filename)
    stream = ffmpeg.output(stream, audio_filename)
    ffmpeg.run(stream)
    return audio_filename

# Function to transcribe audio
def transcribe(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

# Function to generate a summary
def generate_summary(transcript):
    summariser = pipeline('summarization')
    summary = ''
    for i in range(0, (len(transcript)//1000)+1):
        summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
        summary = summary + summary_text + ' '
    return summary

    

# Streamlit UI

if choice=="YouTube Transcript Generator":
    st.title("YouTube Video Transcription🎥")
    st.sidebar.success("Select the Appropriate Tool")

        # Input for the YouTube video URL
    youtube_url = st.text_input("Enter YouTube Video URL:")

        # Check if the URL is provided
    if youtube_url:
        if st.button("Download and Transcribe"):
                # Download the video
            download_video_mp4(youtube_url)

                # Get the list of files in the current directory
            file_list = os.listdir()
            files = os.listdir(folder_path)

            # Iterate through the files and find the index of the first .mp4 file
            for index, file in enumerate(files):
                if file.endswith('.mp4'):
                    print(f"The first .mp4 file is at index {index}: {file}")
                    break
            else:
                print("No .mp4 files found in the directory")
            st.write(file_list)
            create_audio_file(os.listdir()[index])
                # st.write("audio created")
                # Find the video and audio files
                # video_file = [f for f in file_list if f.endswith('.mp4')]
                # audio_file = [f for f in file_list if f.endswith('.mp3')]
            files = os.listdir(folder_path)

            # Iterate through the files and find the index of the first .mp4 file
            for index1, file in enumerate(files):
                if file.endswith('.mp3'):
                    print(f"The first .mp3 file is at index {index}: {file}")
                    break
            else:
                print("No .mp3 files found in the directory")
            video_file=os.listdir()[index]
            v=str(os.listdir()[index])
            print(video_file)
            audio_file=os.listdir()[index1]


                # Check if video and audio files exist
            if video_file and audio_file:
                st.write("Video downloaded and audio extracted.")
                st.write("Transcribing audio...")

                    # Transcribe the audio
                file_list = os.listdir()
                st.write(file_list)
                yt_text = transcribe(os.listdir()[index1])
                yt_text1=yt_text
                    # Display the transcription
                st.write("Transcription:")
                st.write(yt_text)
                c.execute('CREATE TABLE IF NOT EXISTS YoutubeTranscript(id INTEGER PRIMARY KEY AUTOINCREMENT,Link TEXT,Name TEXT,Transcript TEXT)')
                c.execute('INSERT INTO YoutubeTranscript(Link,Name,Transcript) VALUES (?,?,?)', (youtube_url,v,yt_text,))
                conn.commit()
                extension = "*.mp3"
                extension1="*.mp4"  # Replace with the extension you want to target, e.g., "*.jpg" for JPEG files

                file_list = glob.glob(os.path.join(folder_path, extension))

                for file_path in file_list:
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {str(e)}")
                    
                file_list1 = glob.glob(os.path.join(folder_path, extension1))
                for file_path in file_list1:
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {str(e)}")
            else:
                st.write("Error: Video or audio file not found.")

elif choice=="Text Summarizer":
    st.title("Text Summarizer🗒️")
    st.sidebar.success("Select the Appropriate Tool")
    def get_summary(transcript):
        summariser = pipeline('summarization')
        summary = ''
        for i in range(0, (len(transcript)//1000)+1):
            summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
            summary = summary + summary_text + ' '
        
        return summary

    user_input = st.text_input("Enter your Text:")
    if user_input:
        if st.button("Summarize Text"):
            summ=get_summary(user_input)
            st.write(summ)
            if st.button("Copy Text"):
                pyperclip.copy(summ)
            c.execute('CREATE TABLE IF NOT EXISTS Summarization(id INTEGER PRIMARY KEY AUTOINCREMENT, Text TEXT, Summary TEXT)')

            c.execute('INSERT INTO Summarization(Text,Summary) VALUES (?,?)', (user_input,summ))
            conn.commit()
elif choice=="Language Translation":
    st.title("Language Translation🗣️")
    st.sidebar.success("Select the Appropriate Tool")
    selected_option = st.selectbox('Select a language for input:', list(googletrans.LANGUAGES.keys()), format_func=lambda key: f'{key} - {googletrans.LANGUAGES[key]}')

    if selected_option:
        selected_key1 = selected_option
        selected_value1 = googletrans.LANGUAGES[selected_option]
        st.write(f'You selected: {selected_key1} - {selected_value1}')

    text = st.text_input("Enter text here:", "")

    selected_option = st.selectbox('Select a language for translation:', list(googletrans.LANGUAGES.keys()), format_func=lambda key: f'{key} - {googletrans.LANGUAGES[key]}')

    if selected_option:
        selected_key2 = selected_option
        selected_value2 = googletrans.LANGUAGES[selected_option]
        st.write(f'You selected: {selected_key2} - {selected_value2}')


    # text=input("Enter text(in English): ")
    translated_text =translator.translate(text,src=selected_key1, dest=selected_key2)
    st.write(f"Translation: {translated_text.text}")
    t=translated_text.text
    c.execute('CREATE TABLE IF NOT EXISTS Translation(id INTEGER PRIMARY KEY AUTOINCREMENT,Input TEXT,Source TEXT,Destination TEXT,Translation TEXT)')
    c.execute('INSERT INTO Translation(Input,Source,Destination,Translation) VALUES (?,?,?,?)', (text,selected_value1,selected_value2,t))
    conn.commit()
elif choice=='Speech To Text':
    
    
    st.title("Real-Time Speech Recognition🎤")
    st.markdown("### Instructions:")
    st.write(
            "1. Click the 'Start Recording' button to begin recording your speech in real-time."
        )

    st.sidebar.success("Select the Appropriate Tool")

    # Initialize the recognizer
    r = sr.Recognizer()

    # Create a button to start/stop recording
    recording = st.button("Start Recording")
    

    if recording:
        # recording_duration = st.slider("Recording Duration (seconds)", min_value=1, max_value=60, value=10)
        st.write("Recording...")
        
        # Allow the user to specify the recording duration
        
        
        # Initialize the microphone
        mic = sr.Microphone()
        
        # Open the microphone for recording
        with mic as source:
            audio = r.listen(source, timeout=None)
        st.write("Recording Done..")

        # Perform speech recognition
        try:
            text = r.recognize_google(audio)
            st.write("Transcription:")
            st.write(text)

            # SQLite database
            c.execute('CREATE TABLE IF NOT EXISTS Speech(id INTEGER PRIMARY KEY AUTOINCREMENT, Dictation TEXT)')
            c.execute('INSERT INTO Speech(Dictation) VALUES (?)', (text,))
            conn.commit()

        except sr.UnknownValueError:
            st.write("Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")

        # Add an optional instructions text
        
        # st.write("2. Click the 'Stop Recording' button when you are done speaking.")

elif choice=="Previous Translations":
    st.title("Previous Translations🗣️")
    c.execute('SELECT * FROM Translation')
    column_names = [description[0] for description in c.description]
    st.table(column_names)
    data1 = c.fetchall()
    st.table(data1)

elif choice=="Previous YouTube Transcripts":
    st.title("Previous Youtube Transcripts🎥")
    c.execute('SELECT * FROM YouTubeTranscript')
    column_names = [description[0] for description in c.description]
    st.table(column_names)
    data1 = c.fetchall()
    st.table(data1)

elif choice=="Previous Summarizations":
    st.title("Previous Summarizations🗒️")
    c.execute('SELECT * FROM Summarization')
    column_names = [description[0] for description in c.description]
    st.table(column_names)
    data1 = c.fetchall()
    st.table(data1)

elif choice=="Previous Dictations":
    st.title("Previous Dictations🎤")
    c.execute('SELECT * FROM Speech')
    column_names = [description[0] for description in c.description]
    st.table(column_names)
    data1 = c.fetchall()
    st.table(data1)




