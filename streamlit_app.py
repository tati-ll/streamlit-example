from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import pandas as pd
import streamlit as st
import webbrowser
import json
from spotyfyAPI import get_token

from funciones import playlist_popularity

#Spotify API
# Obtener el client ID y el client secret
client_id = st.secrets['SPOTIFY_CLIENT_ID']
client_secret = st.secrets['SPOTIFY_CLIENT_SECRET']

sp = Spotify(auth_manager=SpotifyClientCredentials())
token  = get_token(client_id,client_secret)


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
    resultados_playlist = playlist_popularity(libro, books, songs)

    uri= resultados_playlist['URI'].tolist()

    # Mostrar resultados en Streamlit
    st.write(resultados_playlist[['track_name','track_artist','URI']])
