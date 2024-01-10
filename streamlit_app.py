from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import streamlit as st
import webbrowser
import json

from funciones import playlist_popularity

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
    resultados_playlist = playlist_popularity(libro, books, songs)

    uri= resultados_playlist['URI'].tolist()

    # Mostrar resultados en Streamlit
    st.write(resultados_playlist[['track_name','track_artist','URI']])
