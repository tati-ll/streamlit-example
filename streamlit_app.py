import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from funciones import playlist_popularity


ruta_books = 'books_sentiment.csv'
ruta_songs = 'songs_sentiment.csv'

books = pd.read_csv(ruta_books)
songs = pd.read_csv(ruta_songs)


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

# Utilizar la función para obtener la playlist
playlist1 = playlist_popularity(libro_seleccionado, books, songs)
"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

indices = np.linspace(0, 1, num_points)
theta = 2 * np.pi * num_turns * indices
radius = indices

x = radius * np.cos(theta)
y = radius * np.sin(theta)

df = pd.DataFrame({
    "x": x,
    "y": y,
    "idx": indices,
    "rand": np.random.randn(num_points),
})

st.altair_chart(alt.Chart(df, height=700, width=700)
    .mark_point(filled=True)
    .encode(
        x=alt.X("x", axis=None),
        y=alt.Y("y", axis=None),
        color=alt.Color("idx", legend=None, scale=alt.Scale()),
        size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
    ))
