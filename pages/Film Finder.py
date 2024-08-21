import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

API_KEY = st.secrets["tmdb"]["TMDB_API_KEY"]


def cal_recommendations(selected_movie, movies, similarity_vectors):
    movie_id = movies.loc[movies["title"] == selected_movie].index[0]
    movie_indexes = sorted(
        enumerate(similarity_vectors[movie_id]), reverse=True, key=lambda x: x[1]
    )[1:10]
    movies_list = []
    for i in movie_indexes:
        movies_list.append(movies.iloc[i[0]].movie_id)
    return movies_list


def get_movie_details(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=videos"
    )
    response = response.json()
    movie_title = response.get("original_title", "Unknown movie")#["original_title"]
    poster_path=response.get("poster_path", "")
    poster = "https://image.tmdb.org/t/p/original" + poster_path if poster_path else ""
    return movie_title, poster



similarity_vectors = pickle.load(open("similarity_vectors.pkl", "rb"))
movies = pickle.load(open("movies.pkl", "rb"))
# st.title("Movie Recommendation System🌟")
movies = pd.DataFrame(movies)
titles = movies["title"].values
selected_title = st.selectbox(label="Enter a movie", options=titles)

if st.button(label="Recommend"):
    movie_list = cal_recommendations(selected_title, movies, similarity_vectors)
    recommended_movies = []
    for i in movie_list:
        movie, poster = get_movie_details(i)
        content = {"movie": movie, "poster": poster}
        recommended_movies.append(content)

    columns_per_row = 3
    for i in range(0, len(recommended_movies), columns_per_row):
        row_movies = recommended_movies[i : i + columns_per_row]
        cols = st.columns(columns_per_row)
        for col, movie_content in zip(cols, row_movies):
            with col:
                st.header(movie_content["movie"])
                if movie_content["poster"]!="":
                    st.image(movie_content["poster"])
                    

