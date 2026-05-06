# 🎬 Movie Recommendation System

A modern content-based Movie Recommendation System built using Python, Pandas, Scikit-learn, and Streamlit. The application recommends similar movies based on metadata such as genres, keywords, cast, director, and movie overview using TF-IDF vectorization and cosine similarity.

---

# 📌 Project Overview

This project is a machine learning-based recommendation system that suggests movies similar to a user-selected movie.

Unlike collaborative filtering systems that depend on user ratings and watch history, this project uses a content-based recommendation approach. The recommendation engine analyzes movie metadata and calculates similarity between movies.

The project also integrates the TMDB API to display:

* Movie posters
* Ratings
* Release dates
* Movie overviews

The frontend is built using Streamlit with a modern dark-themed UI inspired by streaming platforms.

---

# 🚀 Features

## ✅ Content-Based Recommendation System

* Recommends movies similar to the selected movie
* Uses metadata such as:

  * Genres
  * Keywords
  * Cast
  * Director
  * Overview

## ✅ TF-IDF Vectorization

* Converts movie metadata into numerical feature vectors
* Helps measure textual similarity between movies

## ✅ Cosine Similarity

* Calculates similarity score between movie vectors
* Recommends the most relevant movies

## ✅ Genre Filtering

* Allows users to filter recommendations by genre
* Improves recommendation relevance

## ✅ TMDB API Integration

* Fetches:

  * Movie posters
  * Ratings
  * Release dates
  * Overviews

## ✅ Interactive Streamlit UI

* Modern dark-themed interface
* Dropdown-based movie selection
* Responsive recommendation cards

## ✅ Similarity Match Percentage

* Displays how closely recommended movies match the selected movie

---

# 🧠 Machine Learning Workflow

## 1. Data Collection

The project uses the TMDB 5000 Movie Dataset containing:

* Movie titles
* Genres
* Keywords
* Cast
* Crew
* Overview

Dataset files:

* `tmdb_5000_movies.csv`
* `tmdb_5000_credits.csv`

---

## 2. Data Preprocessing

The dataset contains JSON-like string data.

Preprocessing steps:

* Merged movie and credits datasets
* Removed missing values
* Extracted:

  * Genres
  * Keywords
  * Top cast members
  * Director
* Converted overview text into tokens
* Removed spaces from multi-word names
* Combined metadata into a single `tags` column

---

## 3. Feature Engineering

The combined `tags` column acts as the movie profile.

Example:

```text
Action Adventure SciFi ChristopherNolan Batman Gotham Hero
```

---

## 4. TF-IDF Vectorization

TF-IDF converts textual movie metadata into numerical vectors.

This helps the system understand important words while reducing the impact of common words.

---

## 5. Cosine Similarity

Cosine similarity measures the similarity between movie vectors.

Movies with higher cosine similarity are considered more related.

---

## 6. Recommendation Generation

The system:

1. Finds the selected movie
2. Retrieves similarity scores
3. Sorts movies by similarity
4. Returns the top recommended movies

---

# 🛠️ Technologies Used

| Technology    | Purpose                                    |
| ------------- | ------------------------------------------ |
| Python        | Core programming language                  |
| Pandas        | Data preprocessing and manipulation        |
| NumPy         | Numerical operations                       |
| Scikit-learn  | TF-IDF vectorization and cosine similarity |
| Streamlit     | Frontend web application                   |
| Requests      | TMDB API integration                       |
| Python-dotenv | Secure API key management                  |

---

# 📂 Project Structure

```text
movie-recommendation-system/
│
├── dataset/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
│
├── .env
├── .gitignore
├── app.py
├── model.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation and Setup

## 1. Clone Repository

```bash
git clone https://github.com/sahilkelkar2005/movie-recommendation-system.git
```

---

## 2. Navigate to Project Folder

```bash
cd movie-recommendation-system
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create `.env` File

Create a `.env` file in the root directory.

Add your TMDB API key:

```text
TMDB_API_KEY=your_api_key_here
```

---

## 5. Run the Application

```bash
python -m streamlit run app.py
```

---

# 🔑 TMDB API Setup

1. Create an account on TMDB
2. Generate an API key
3. Add the API key inside `.env`

Example:

```text
TMDB_API_KEY=abc123xyz456
```

---

# 📸 Application Features

## 🎞️ Movie Recommendation

Users can select a movie and receive similar movie recommendations.

## 🎭 Genre Filter

Users can filter recommendations by genre.

## ⭐ Ratings

Displays movie ratings fetched from TMDB.

## 📅 Release Date

Displays movie release year/date.

## 🖼️ Movie Posters

Shows posters for all recommended movies.

## 🔥 Similarity Percentage

Displays recommendation match percentage.

## 📝 Movie Overview

Shows short descriptions of recommended movies.

---

# 📊 Recommendation Technique

This project uses a content-based filtering approach.

### Why Content-Based Filtering?

* Does not require user history
* Works well for metadata-rich datasets
* Easier to explain and implement
* Suitable for beginner and intermediate ML projects

---

# 🧪 Example Recommendation

### Input Movie:

```text
Batman Begins
```

### Recommended Movies:

* The Dark Knight
* Batman
* Batman Returns
* The Dark Knight Rises
* Man of Steel

---

# 🔐 Security Practices

The project uses:

* `.env` file for API keys
* `.gitignore` to prevent secret uploads

This follows standard development practices.

---

# 📈 Future Improvements

Potential future upgrades:

* User authentication system
* Watchlist functionality
* Search autocomplete
* Trailer integration
* Trending movies section
* Collaborative filtering
* Hybrid recommendation system
* Deployment on cloud platforms

---

# 🎯 Learning Outcomes

This project helped in understanding:

* NLP preprocessing
* Feature engineering
* TF-IDF vectorization
* Cosine similarity
* Recommendation systems
* API integration
* Streamlit frontend development
* End-to-end ML workflow

---

# 👨‍💻 Author

## Sahil Kelkar

B.Tech AIML Student

---

# 📜 License

This project is developed for educational and learning purposes.
