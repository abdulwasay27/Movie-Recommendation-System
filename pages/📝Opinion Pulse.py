import streamlit as st
import sys
import pickle
import sklearn
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import requests
import pandas as pd
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

stemmer=PorterStemmer()

def load_model_and_vectorizer(model_path, vectorizer_path):
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    with open(vectorizer_path, 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    return model, vectorizer


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
stop_words = set(stopwords.words('english'))
def text_preprocessing(text):
    text = text.lower()
    text = re.sub("<br />", '', text)
    text = re.sub(r"https\S+|www\S+|http\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[^\w\s]","", text)
    text = re.sub(r"\@w+|\#", '', text)
    text_tokens=word_tokenize(text, language="english")
    filtered_text=[word for word in text_tokens if word not in stop_words]
    # print(filtered_text)
    return " ".join(filtered_text)

def stemming_text(text):
    stemmed_words = []
    for word in text.split():
        stemmed_words.append(stemmer.stem(word))
    return " ".join(stemmed_words)

def fetch_movie_id(movie_name):
    
    url = f"https://www.imdb.com/find/?q={movie_name}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        st.error("Error while fetching movie ID. Please try again later.")
        st.stop()

    soup = BeautifulSoup(response.text, "html.parser")
    try:
        movie = soup.select(".ipc-metadata-list-summary-item__tc")[0]
        movie_a_tag = movie.find("a")
        movie_id = movie_a_tag.get("href").split("/")[2]
        return movie_id
    except Exception:
        st.error("Error while fetching movie ID. Please try again later.")
        st.stop()


def fetch_movie_reviews(movie_id):

    url = f"https://www.imdb.com/title/{movie_id}/reviews?sort=totalVotes"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        st.error("Error while loading reviews. Please try again later.")
        st.stop()
    else:
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            review_containers=soup.findAll("div", class_=["lister-item", "mode-detail", "imdb-user-review"])
            
            total_reviews=[]
            content={}
            for single_review_container in review_containers:
                title=single_review_container.find("a", class_=["title"])
                review=single_review_container.find("div", class_=["text", "show-more__control"])
                content["title"]=title.getText()
                content["review"]=review.getText()
                total_reviews.append(content.copy())
                
            return total_reviews
        except Exception:
            st.error("Error while parsing reviews. Please try again later.")
            st.stop()

model, vectorizer = load_model_and_vectorizer("model.pkl", "vectorizer.pkl")
movie_name=st.text_input(label="Enter a movie")
if movie_name:
    movie_id = fetch_movie_id(movie_name)
    movie_reviews=fetch_movie_reviews(movie_id)
    for movie in movie_reviews:
            processed_text = text_preprocessing(movie["review"])
            processed_text = stemming_text(processed_text)
            transformed_text = vectorizer.transform([processed_text])
            prediction = model.predict(transformed_text.toarray())
            sentiment="positive" if prediction == 1 else "negative"
            if sentiment == "positive":
                sentiment_color="#5AA333"
            else:
                sentiment_color="#BD3F3A"
            st.container()
            st.markdown(
                                    f"""
                                    <div style="
                                        border: 2px solid #ddd;
                                        border-radius: 5px;
                                        padding: 10px;
                                        margin-bottom: 10px;
                                    ">
                                        <h3>{movie['title']}</h3>
                                        <h5>Sentiment: <span  style="color: {sentiment_color};">{sentiment}</span></h5>
                                        <p>{movie['review']}</p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                            )
        
