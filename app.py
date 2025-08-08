import pickle
import streamlit as st
import requests
from concurrent.futures import ThreadPoolExecutor

# -------------------------------
# Cached Poster Fetcher
# -------------------------------
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b8e78c1f626f644d32c8efc2affe01fb&language=en-US"
    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=No+Image"

# -------------------------------
# Recommend Movies Function
# -------------------------------
def recommend(movie_name):
    index = movies[movies['title'] == movie_name].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_names = []
    movie_ids = []

    for i in distances[1:6]:  
        recommended_names.append(movies.iloc[i[0]].title)
        movie_ids.append(movies.iloc[i[0]].movie_id)

    # Fetch posters in parallel
    with ThreadPoolExecutor() as executor:
        recommended_posters = list(executor.map(fetch_poster, movie_ids))

    return recommended_names, recommended_posters

# -------------------------------
# Streamlit UI
# -------------------------------
st.header('🎬 Movie Recommender System Using Machine Learning')
st.markdown("This is a simple movie recommendation system that suggests movies based on your input. It uses machine learning techniques to find similar movies.")

movies = pickle.load(open(r"C:\data-Scientist\Data-Science\project in movie_recommendation\movies.pkl", 'rb'))
similarity = pickle.load(open(r"C:\data-Scientist\Data-Science\project in movie_recommendation\similarity.pkl", 'rb'))

movie_list = movies['title'].values
selected_movie_name = st.selectbox(
    'Type or select a movie to get recommendations',
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx])

# Footer
st.markdown("Made with ❤️ by **Ragul V**")
st.markdown('[Source code on GitHub](https://github.com/RAGULcse25/1_project.movie_recommendation-)')
