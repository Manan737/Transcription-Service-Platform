import streamlit as st
import pandas as pd
import subprocess

# Security
import hashlib


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

# DB  Functions

    
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def clear_password():
    """Clears the password input"""
    password_widget = st.session_state['password']
    password_widget.value = ''
    st.session_state['password'] = ''

def main():
    

    

    menu = ["Home","Login","Sign Up"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("Transcription Service Platform ✍️")
        st.image("Best-Transcription-Services.jpg", caption="Transcription Service", use_column_width=True)
        st.subheader("YouTube Transcript Generator")
        st.write("🎥 Turn your video content into written gold! Our YouTube Transcript Generator converts your videos into accurate text transcripts.")
        st.subheader("Text Summarization")
        st.write("📚 Too much to read? Let us help! Our Text Summarization tool condenses lengthy articles into concise summaries.")
        st.subheader("Language Translation")
        st.write("🌍 Break language barriers! Our Language Translation service helps you communicate across the globe.")  
        st.subheader("Speech to Text")
        st.write("🗣️ Speak your mind, and we'll transcribe it! Our Speech to Text service converts spoken words into written text.")  

    if choice == "Login":
        st.title("Login👤")
        
        username = st.text_input("User Name👨🏻‍💻")
        password = st.text_input("Password🔑", type='password', value='', key='password')


        if st.button("Login"):
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:
                st.success("Logged In as {}".format(username))
                # import manan.Youtube_Transcript_Generator as yt
                # yt.main()
                st.empty()
                # menu = ["Home","Login","SignUp","YouTube Transcript Generator","Text Summarization","Language Translation",'Speech To Text']
                # choice = st.sidebar.selectbox("Menu",menu)
                # Replace 'your_command' with the actual command you want to run
                command = 'streamlit run Youtube_Transcript_Generator.py'

                try:
                    # Run the command and capture the output
                    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                    # Check the output
                    if result.returncode == 0:
                        print("Command executed successfully")
                        print("Output:")
                        print(result.stdout)
                    else:
                        print("Command failed with an error")
                        print("Error:")
                        print(result.stderr)

                except subprocess.CalledProcessError as e:
                    print("Command execution failed with an exception")
                    print("Error:")
                    print(e)
                except Exception as e:
                    print("An unexpected error occurred")
                    print("Error:")
                    print(e)
                                
                
                
            else:
                st.warning("Incorrect Username/Password")
    # Create a new password widget with the same key to clear it
        # st.text_input("Clear Password", type='password', value='', key='password')

    if choice == "Sign Up":
        st.title("Sign Up📝")
        
        st.subheader("Create New Account")
        new_user = st.text_input("Username👨🏻‍💻")
        new_password = st.text_input("Password🔑",type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")

  

if __name__ == '__main__':
    main()
