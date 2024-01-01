import streamlit as st
import requests
from currentsapi import CurrentsAPI
from dotenv import load_dotenv
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
load_dotenv()
currentsAPI_key=os.environ.get('currentsAPI_key')
api_host = os.environ.get("HOST", "api")
api_port = int(os.environ.get("PORT", 8080))

def extract_keywords(sentence):
    # Tokenize the sentence
    words = word_tokenize(sentence)
    
    # Tag words with parts of speech
    tagged_words = pos_tag(words)
    
    # Define POS tags for keywords (e.g., nouns, adjectives)
    keyword_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS']  # Nouns and Adjectives
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    
    # Extract words with specified POS tags and not in stopwords
    keywords = [word for word, tag in tagged_words if tag in keyword_tags and word.lower() not in stop_words]
    
    return keywords
def main():
    st.set_page_config(layout="wide")  # Set layout to wide for full browser width
    st.title('Welcome to Current News')
    
    url = 'https://api.currentsapi.services/v1/latest-news'
    params = {'apiKey': currentsAPI_key,'language': 'en','country':'In'}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        news_data = response.json()
    
    long_text = ""
    if len(news_data['news'])>10:
        for i in range(10):
            long_text = long_text + f'{i+1}.' + news_data['news'][i]['title'] +'\n' + news_data['news'][i]['description'] + '\n'
    else:
        for i in range(len(news_data['news'])):
            long_text = long_text + f'{i+1}.' + news_data['news'][i]['title'] +'\n' + news_data['news'][i]['description'] + '\n'

    with open('./information.txt', 'w') as file: file.write(long_text)

    url = f'http://{api_host}:{api_port}/'
    data = {"query": 'what are the latest news?'}

    response = requests.post(url, json=data)
    st.markdown(""" <br>""", unsafe_allow_html=True,)
    
    question = st.text_input("Interested in other news?", placeholder="write your interest here? (One word)")
    if question:
        sentence = question
        keywords = extract_keywords(sentence)
        

        url = 'https://api.currentsapi.services/v1/search?'
        params = {
            'apiKey': currentsAPI_key,
            'language': 'en',
            'keywords': keywords[-1]
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            news_data = response.json()
        
        long_text = ""
        if len(news_data['news'])>10:
            for i in range(10):
                long_text = long_text + f'{i+1}.' + news_data['news'][i]['title'] +'\n' + news_data['news'][i]['description'] + '\n'
        else:
            for i in range(len(news_data['news'])):
                long_text = long_text + f'{i+1}.' + news_data['news'][i]['title'] +'\n' + news_data['news'][i]['description'] + '\n'

        with open('information.txt', 'w') as file: file.write(long_text)
        
        url = f'http://{api_host}:{api_port}/'
        data = {"query": 'summarize the news'}
        

        response = requests.post(url, json=data)
        st.text('These are the related news.')
        
        st.write(response.json())
    else:
        st.text('These are the latest news.')
        st.write(response.json())
if __name__ == "__main__":
    main()