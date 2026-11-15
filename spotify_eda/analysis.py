"""Carga, control de calidad, métricas y agregaciones del catálogo."""
from pathlib import Path
import pandas as pd

REQUIRED = {"track_id", "track_name", "track_popularity", "artist_name", "artist_popularity", "artist_followers", "artist_genres", "album_release_date", "track_duration_min", "explicit"}

def load_tracks(path):
    df = pd.read_csv(Path(path))
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Columnas requeridas ausentes: {', '.join(sorted(missing))}")
    df = df.copy()
    df["track_id"] = df["track_id"].astype("string").str.strip()
    df["artist_name"] = df["artist_name"].astype("string").str.strip()
    df["track_name"] = df["track_name"].astype("string").str.strip()
    df = df.dropna(subset=["track_id", "artist_name", "track_name"])
    df = df.loc[(df["track_id"] != "") & (df["artist_name"] != "") & (df["track_name"] != "")]
    df = df.drop_duplicates(subset="track_id", keep="first").copy()
    for c in ["track_popularity", "artist_popularity", "artist_followers", "track_duration_min"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["album_release_date"] = pd.to_datetime(df["album_release_date"], errors="coerce")
    df["release_year"] = df["album_release_date"].dt.year
    df["artist_genres"] = df["artist_genres"].fillna("Sin clasificar")
    df["explicit"] = df["explicit"].astype("string").str.lower().map({"true":True,"false":False,"1":True,"0":False})
    df.loc[~df["track_popularity"].between(0,100), "track_popularity"] = float('nan')
    df.loc[~df["artist_popularity"].between(0,100), "artist_popularity"] = float('nan')
    df.loc[df["artist_followers"] < 0, "artist_followers"] = float('nan')
    df.loc[df["track_duration_min"] <= 0, "track_duration_min"] = float('nan')
    return df

def summary(df):
    return {
        "tracks": int(len(df)),
        "artists": int(df.artist_name.nunique()),
        "average_track_popularity": round(float(df.track_popularity.mean()),2),
        "median_track_popularity": round(float(df.track_popularity.median()),2),
        "average_duration_minutes": round(float(df.track_duration_min.mean()),2),
        "explicit_percent": round(float(df.explicit.mean()*100),2),
        "unclassified_genres_percent": round(float((df.artist_genres == "Sin clasificar").mean()*100),2),
        "missing_release_dates": int(df.album_release_date.isna().sum()),
    }

def top_artists(df, min_tracks=5, n=10):
    d = df.dropna(subset=["track_popularity"])
    a = (d.groupby("artist_name", as_index=False).agg(
        avg_popularity=("track_popularity", "mean"),
        tracks=("track_id", "nunique")))
    return a[a.tracks>=min_tracks].sort_values(["avg_popularity","tracks"],ascending=[False,False]).head(n)

def top_tracks(df, n=10):
    return df.dropna(subset=["track_popularity"]).sort_values("track_popularity",ascending=False).head(n)

def genres(df, n=12):
    # Los géneros están asignados al artista y pueden contener múltiples etiquetas.
    s = df.loc[df.artist_genres != "Sin clasificar", "artist_genres"]
    return s.str.split(",").explode().str.strip().replace("",pd.NA).dropna().value_counts().head(n)

def correlations(df):
    d = df[["track_popularity","artist_popularity","artist_followers","track_duration_min"]].copy()
    d["log10_followers_plus_one"] = __import__("numpy").log10(d["artist_followers"].clip(lower=0)+1)
    return d[["track_popularity","artist_popularity","log10_followers_plus_one","track_duration_min"]].corr()
