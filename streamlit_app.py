import pandas as pd
import streamlit as st
# import spotipy
from funciones import playlist_popularity
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
import webbrowser
import json
# import requests

# Agregar CSS personalizado para imitar el estilo de Spotify
st.markdown("""
    <style>
        body {
            background-color: #191414;
            color: #fff;
            font-family: 'Helvetica Neue', sans-serif;
        }
        h1, h2, h3 {
            color: #1DB954;
        }
        select {
            background-color: #282828;
            color: #fff;
        }
        .stButton>button {
            background-color: #1DB954;
            color: #fff;
        }
        .stButton>button:hover {
            background-color: #25d366;
        }
        /* Puedes agregar más estilos según sea necesario */
    </style>
""", unsafe_allow_html=True)

# Crear un objeto de la API de Spotify
sp = Spotify()

#Spotify API
# Obtener el client ID y el client secret
client_id = "2c6e83abacec42e5b9dd16073017a179"
client_secret = "c21f09ef530643ca9055aa35dd081819"

# Obtener el token de acceso
auth_manager = SpotifyOAuth(client_id, client_secret, redirect_uri="http://localhost:8501")
auth_url = auth_manager.get_authorize_url()

# Abrir un navegador web con la URL de autorización
webbrowser.open(auth_url)

# Obtener el código de autorización
code = input("Ingrese el código de autorización: ")

# Intercambiar el código de autorización por un token de acceso
token = auth_manager.get_access_token(code)

# Almacenar el token de acceso
with open("token.json", "w") as f:
    f.write(json.dumps(token))

col1, col2 = st.columns(2)

with col1:
   st.title(":blue[BOOKBEAT]")
   st.markdown(''':blue[***¡Disfruta de tus libros favoritos con la banda sonora perfecta!***]''')

with col2:
   st.image("bookbeat.png")

@st.cache_data
def carga_dataset():
    # Ruta al archivo CSV
    ruta_books = "books_sentiment.csv"
    ruta_songs = "songs_sentiment.csv"

    # Cargar datos desde el archivo CSV
    books = pd.read_csv(ruta_books)
    songs = pd.read_csv(ruta_songs)

    return books, songs

books, songs = carga_dataset()

def obtener_coincidencias(titulo_ingresado):
    return books[books["Book"].str.contains(titulo_ingresado, case=False)]

# Configuración de la página
st.title("Búsqueda de Libro:")

# Obtener coincidencias del DataFrame
coincidencias = obtener_coincidencias("")

# Mostrar las primeras 5 coincidencias en un cuadro desplegable (dropdown)
libro_seleccionado = st.selectbox("Seleccione el libro:", coincidencias["Book"].tolist(), index=0)

def obtener_coincidencias(libro_seleccionado):
    return books[books["Book"].str.contains(libro_seleccionado, case=False)]

# Botón para generar la playlist
if st.button("Generar Playlist"):
    # Resultados de la función basada en el título del libro
    libro = libro_seleccionado
    resultados_playlist = playlist_popularity(libro_seleccionado, books, songs)

    uri= resultados_playlist['URI'].tolist()

    # Mostrar resultados en Streamlit
    st.write(resultados_playlist[['track_name','track_artist','URI']])







# """
# # Welcome to Streamlit!

# Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
# If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
# forums](https://discuss.streamlit.io).
