import pandas as pd

tracks_df = pd.read_csv("data/spotify/data.csv")

#ordenamos por año y poularidad (de mayor a menor)
df_sorted = tracks_df.sort_values(["year", "popularity"], ascending=[True, False])

#mostramos la canción más popular por año
top_song_by_year = df_sorted.drop_duplicates(subset="year", keep="first")

#seleccionamos columnas relevantes
top_song_by_year = top_song_by_year[["year", "name", "artists", "popularity"]]

print(top_song_by_year.head())
print(top_song_by_year.tail())

# Canción más popular por año
top_song_per_year = (tracks_df.loc[tracks_df.groupby("year")["popularity"].idxmax()].sort_values("year"))

print(top_song_per_year[["year", "name", "artists", "popularity"]].head(10))
print(top_song_per_year.tail(10))
