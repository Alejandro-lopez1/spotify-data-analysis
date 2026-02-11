import pandas as pd
import matplotlib.pyplot as plt

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


#generamos un primer gráfico para tener una idea 
plt.figure(figsize=(12, 6))
plt.plot(
    top_song_per_year["year"],
    top_song_per_year["popularity"]
)
plt.title("Top song popularity by year (Spotify metric)")
plt.xlabel("Year")
plt.ylabel("Popularity")

plt.tight_layout()
plt.savefig("outputs/top_song_popularity_by_year.png")
plt.close()


# Convert artists from string to list
artists_df = tracks_df.copy()

artists_df["artists"] = (
    artists_df["artists"]
    .str.replace("[", "", regex=False)
    .str.replace("]", "", regex=False)
    .str.replace("'", "", regex=False)
    .str.split(", ")
)

artists_df = tracks_df.explode("artists")
print(artists_df[["name", "artists", "popularity"]].head(10))

artist_popularity_df = (
    artists_df
    .groupby("artists")
    .agg(
        avg_popularity=("popularity", "mean"),
        song_count=("name", "count")
    )
    .reset_index()
)
artist_popularity_df = artist_popularity_df[
    artist_popularity_df["song_count"] >= 10
]
top_artists_df = (
    artist_popularity_df
    .sort_values("avg_popularity", ascending=False)
    .head(10)
)
print(top_artists_df)
