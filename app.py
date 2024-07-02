import pickle
import streamlit as st
import pandas as pd
import requests
import gzip

def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=eaac1bbefd2e7cce74b328ba44904893&language=en-US")
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['id']
        recommend_movies.append(movies.iloc[i[0]]['title'])
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters

# Load data
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

# Ensure 'id' is present
if 'id' not in movies.columns:
    print("Error: 'id' column not found in movies DataFrame")

# Load compressed similarity.pkl.gz
with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

# Streamlit application
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select movie',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)

    for col, name, poster in zip(cols, names, posters):
        col.text(name)
        col.image(poster)
