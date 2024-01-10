def playlist_popularity(title, books_df, songs_df):
    """Función que busca el 'sentiment compound' del título dado y lo compara con el 'sentiment compound' de las
    canciones en el dataset, y genera una playlist de 20 canciones más similares en sentimiento, además tomando en
    cuenta la popularidad de las canciones"""
    book_sentiment = books_df.loc[books_df["Book"] == title, "sentiment"].values[0]

    # Calcular la diferencia absoluta en el sentimiento
    songs_df['abs_dif'] = abs(songs_df['sentiment'] - book_sentiment)

    # Seleccionar las 20 canciones más similares en sentimiento
    similar_songs = songs_df.nsmallest(70, 'abs_dif')

    # Ordenar las canciones en base a 'track_popularity'
    sorted_playlist = similar_songs.sort_values(by=['track_popularity', 'abs_dif'], ascending=[False, True]).head(20)

    return sorted_playlist
