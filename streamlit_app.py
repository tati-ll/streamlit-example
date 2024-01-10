import pandas as pd
import streamlit as st
from funciones import playlist_popularity

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
# libro_seleccionado = st.selectbox("Seleccione el libro:", coincidencias["Book"].tolist(), index=0)
# Mostrar las primeras 5 coincidencias en un cuadro de opciones (radio)
libro_seleccionado = st.radio("Seleccione el libro:", coincidencias["Book"].tolist(), index=0)

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
