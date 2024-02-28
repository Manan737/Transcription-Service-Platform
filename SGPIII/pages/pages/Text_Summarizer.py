import streamlit as st
from transformers import pipeline
st.title("Text Summarizer")
st.sidebar.success("Select the required model")
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

    
