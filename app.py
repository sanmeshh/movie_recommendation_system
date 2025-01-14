import streamlit as st
import pickle
import pandas as pd
import requests
#indirectly brought our preprocessed dataframe
st.title('Movie Recommender System')

movies=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies)


# def load_model_from_url():
#     response = requests.get(MODEL_URL, stream=True)
    
    
#         # Load the model into memory directly
#     model = pickle.load(response.raw)
#     return model

url = "https://movierecommenderr.s3.ap-south-1.amazonaws.com/similarity.pkl"
response = requests.get(url)
with open("similarity.pkl", "wb") as f:
    f.write(response.content)

# Load the model
with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)
    




def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=25f62ea5a759dfa05a798f44c0fba61a&language=en-US'.format(movie_id))
    data=response.json()
    return  "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    
    
    index=movies[movies['title']==movie].index[0]
    distances=similarity[index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x : x[1])[1:5]
    recommendations=[]
    poster=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        #getting the title of the movies through index provided by the similarity enumerated vector
        recommendations.append(movies.iloc[i[0]].title)
        #fetch poster from api
        poster.append(fetch_poster(movie_id))
    return recommendations,poster

option=st.selectbox(
  'Enter your movie name: ',
  movies['title'].values)

if st.button("Get Recommendations"):
    recommended_movie_names,recommended_movie_posters = recommend(option)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
   

