import pandas as pd
import ast
import requests
import os

from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables
load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

# ---------------- LOAD DATA ---------------- #

movies = pd.read_csv('dataset/tmdb_5000_movies.csv')
credits = pd.read_csv('dataset/tmdb_5000_credits.csv')

movies = movies.merge(credits, on='title')

movies = movies[['movie_id',
                 'title',
                 'overview',
                 'genres',
                 'keywords',
                 'cast',
                 'crew']]

movies.dropna(inplace=True)

# ---------------- PREPROCESSING ---------------- #

def convert(text):
    L = []

    for i in ast.literal_eval(text):
        L.append(i['name'])

    return L


movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)


def convert_cast(text):
    L = []
    counter = 0

    for i in ast.literal_eval(text):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break

    return L


movies['cast'] = movies['cast'].apply(convert_cast)


def fetch_director(text):
    L = []

    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
            break

    return L


movies['crew'] = movies['crew'].apply(fetch_director)

movies['overview'] = movies['overview'].apply(lambda x: x.split())

movies['genres'] = movies['genres'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['keywords'] = movies['keywords'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['cast'] = movies['cast'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['crew'] = movies['crew'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

# ---------------- TAG CREATION ---------------- #

movies['tags'] = movies['overview'] + \
                 movies['genres'] + \
                 movies['keywords'] + \
                 movies['cast'] + \
                 movies['crew']

new_df = movies[['movie_id', 'title', 'genres', 'tags']]

new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

# ---------------- TF-IDF ---------------- #

tfidf = TfidfVectorizer(max_features=5000, stop_words='english')

vectors = tfidf.fit_transform(new_df['tags']).toarray()

similarity = cosine_similarity(vectors)

# ---------------- TMDB API ---------------- #

def fetch_movie_details(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    response = requests.get(url)

    data = response.json()

    poster_path = data.get('poster_path')

    full_path = None

    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

    return {
        "poster": full_path,
        "rating": data.get("vote_average", "N/A"),
        "release_date": data.get("release_date", "N/A"),
        "overview": data.get("overview", "No overview available.")
    }


# ---------------- RECOMMEND FUNCTION ---------------- #

def recommend(movie, selected_genre=None):

    movie_index = new_df[new_df['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:20]

    recommended_movies = []

    for i in movies_list:

        similarity_score = round(i[1] * 100, 1)

        movie_data = new_df.iloc[i[0]]

        # Genre filter
        if selected_genre:

            genres_lower = [g.lower() for g in movie_data['genres']]

            if selected_genre.lower() not in genres_lower:
                continue

        details = fetch_movie_details(movie_data.movie_id)

        recommended_movies.append({
            "title": movie_data.title,
            "poster": details["poster"],
            "rating": details["rating"],
            "release_date": details["release_date"],
            "overview": details["overview"],
            "similarity": similarity_score
        })

        if len(recommended_movies) == 5:
            break

    return recommended_movies