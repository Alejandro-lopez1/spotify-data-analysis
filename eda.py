import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# =========================
# Setup
# =========================

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

tracks_df = pd.read_csv("data/spotify/data.csv")

# =========================
# Canción más popular por año
# =========================

df_sorted = tracks_df.sort_values(
    ["year", "popularity"],
    ascending=[True, False]
)

top_song_by_year = (
    df_sorted
    .drop_duplicates(subset="year", keep="first")
    [["year", "name", "artists", "popularity"]]
)

print(top_song_by_year.head())
print(top_song_by_year.tail())

top_song_per_year = (
    tracks_df
    .loc[tracks_df.groupby("year")["popularity"].idxmax()]
    .sort_values("year")
)

print(top_song_per_year[["year", "name", "artists", "popularity"]].head(10))
print(top_song_per_year.tail(10))

# =========================
# Gráfico: popularidad top song por año
# =========================

plt.figure(figsize=(12, 6))
plt.plot(
    top_song_per_year["year"],
    top_song_per_year["popularity"]
)

plt.title("Top song popularity by year (Spotify metric)")
plt.xlabel("Year")
plt.ylabel("Popularity")

plt.tight_layout()
plt.savefig(output_dir / "top_song_popularity_by_year.png")
plt.close()

# =========================
# Normalización de artistas
# =========================

artists_df = tracks_df.copy()

artists_df["artists"] = (
    artists_df["artists"]
    .str.replace("[", "", regex=False)
    .str.replace("]", "", regex=False)
    .str.replace("'", "", regex=False)
    .str.split(", ")
)

artists_df = artists_df.explode("artists")

print(artists_df[["name", "artists", "popularity"]].head(10))

# =========================
# Popularidad por artista
# =========================

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

# =========================
# Relación catálogo vs popularidad
# =========================

artist_stats = (
    artist_popularity_df
    .copy()
)

print(artist_stats.head())
print(artist_stats.describe())

artist_stats = artist_stats[artist_stats["song_count"] >= 5]

plt.figure(figsize=(8, 6))
plt.scatter(
    artist_stats["song_count"],
    artist_stats["avg_popularity"],
    alpha=0.6
)

plt.xlabel("Cantidad de canciones")
plt.ylabel("Popularidad promedio")
plt.title("Relación entre tamaño del catálogo y popularidad promedio")

plt.tight_layout()
plt.savefig(output_dir / "catalog_size_vs_popularity.png")
plt.close()
