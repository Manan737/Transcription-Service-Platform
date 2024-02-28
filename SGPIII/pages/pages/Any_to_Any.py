import googletrans
import streamlit as st

# print(googletrans.LANGUAGES)

from googletrans import Translator
translator = Translator()

# default_key='en'
st.sidebar.success("Select the required model")

st.title("Language Translation")

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
translated_text = translator.translate(text,src=selected_key1, dest=selected_key2)
st.write(f"Translation: {translated_text.text}")

# print(translated_text.text)