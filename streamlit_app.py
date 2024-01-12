from spotipy import Spotify
import pandas as pd
import streamlit as st
from spotifyAPI import authenticate_spotify_user

from funciones import playlist_popularity

#Spotify API
# Obtener el client ID y el client secret
SPOTIFY_CLIENT_ID = st.secrets['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = st.secrets['SPOTIFY_CLIENT_SECRET']
REDIRECT_URI = "https://tati-ll-streamlit-example-streamlit-app-5rmuke.streamlit.app/"

st.set_page_config(
    page_title="BookBeat",
    page_icon="book",
    layout="wide",
)

# Title and gif
config = {
    "authorization_endpoint": "https://accounts.spotify.com/authorize",
    "token_endpoint": "https://accounts.spotify.com/api/token",
    "redirect_uri": REDIRECT_URI,
    "client_id": SPOTIFY_CLIENT_ID,
    "client_secret": SPOTIFY_CLIENT_SECRET,
    "scope": "playlist-modify-private",
}

st.title(":blue[BOOKBEAT]")
but, img = st.columns([0.5, 0.5])

img.image("bookbeat.png")

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
button = st.button("Generar Playlist")

try:
    st.write('Prueba')
    spotify = authenticate_spotify_user(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope='playlist-modify-private')
    but.write(f"Authenticated successfully as **{spotify.me()['display_name']}")
except:
    spotify = None
    st.error("Unable to authenticate with Spotify.")

playlist_name = f'Playlist to read "{libro_seleccionado}"'

if spotify:
    button = st.button("Generar Playlist")
    if button:
        # Resultados de la función basada en el título del libro
        libro = libro_seleccionado
        resultados_playlist = playlist_popularity(libro, books, songs)
        uris= resultados_playlist['URI'].tolist()
        try:
            book_playlist = spotify.user_playlist_create(
                        user=spotify.current_user()["id"],
                        name=playlist_name,
                        public=False,
                        collaborative=False,
                        description=f'Playlist to read "{libro_seleccionado}", generated with BookBeat.',
                    )
        except Exception as e:
            st.error(f"Error creating playlist: {e}")

        if book_playlist:
            st.success("Successfully created playlist!")
            try:
                spotify.user_playlist_add_tracks(
                    user=spotify.current_user()["id"],
                    playlist_id=book_playlist["id"],
                    tracks=uris)
            except Exception as e:
                st.error(f"Error adding tracks to playlist: {e}")

            st.success("Successfully added tracks to playlist!")
            st.write(
                        f"Check out your playlist [here]({book_playlist['external_urls']['spotify']})."
                    )
        else:
            st.error("Unable to authenticate with Spotify.")
