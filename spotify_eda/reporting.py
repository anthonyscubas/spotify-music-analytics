"""Gráficos y resumen publicable, sin dependencia de rutas del autor."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from .analysis import summary, top_artists, top_tracks, genres, correlations

BLUE="#1DB954"; DARK="#14211A"

def _style():
    plt.rcParams.update({"figure.figsize":(10,5.8),"font.size":10,"axes.spines.top":False,"axes.spines.right":False,"axes.titleweight":"bold","axes.labelcolor":DARK,"text.color":DARK,"savefig.facecolor":"white"})

def _save(out,name):
    plt.tight_layout(pad=1.8)
    plt.savefig(out/name, dpi=175, bbox_inches="tight")
    plt.close()

def create_report(df, dest):
    dest=Path(dest); figs=dest/"figures";figs.mkdir(parents=True,exist_ok=True)
    _style(); metrics=summary(df)
    s=df.track_popularity.dropna()
    fig, ax=plt.subplots(); ax.hist(s,bins=20,color=BLUE,edgecolor="white");ax.set(title="Distribución de popularidad de canciones",xlabel="Popularidad de la canción (0–100)",ylabel="Cantidad de canciones"); _save(figs,"01_popularidad.png")
    a=top_artists(df)
    fig, ax=plt.subplots(figsize=(11,6)); ax.barh(a.artist_name.astype(str).iloc[::-1],a.avg_popularity.iloc[::-1],color=BLUE);ax.set(title="Artistas con mayor popularidad media (mín. 5 canciones)",xlabel="Popularidad media de canciones (0–100)");_save(figs,"02_artistas.png")
    t=top_tracks(df)
    fig,ax=plt.subplots(figsize=(11,6));labels=(t.track_name.astype(str)+" — "+t.artist_name.astype(str)).str.slice(0,63);ax.barh(labels.iloc[::-1],t.track_popularity.iloc[::-1],color=BLUE);ax.set(title="10 canciones con mayor popularidad registrada",xlabel="Popularidad (0–100)");_save(figs,"03_canciones.png")
    g=genres(df)
    fig,ax=plt.subplots(figsize=(11,6));ax.barh(g.index[::-1],g.values[::-1],color=BLUE);ax.set(title="Géneros más frecuentes (etiquetas multivalor)",xlabel="Apariciones en registros de canciones");_save(figs,"04_generos.png")
    years=df.release_year.value_counts().sort_index();years=years[(years.index>=1980)&(years.index<=2030)]
    fig,ax=plt.subplots(figsize=(11,5));ax.plot(years.index,years.values,marker="o",markersize=3,color=BLUE);ax.set(title="Canciones por año de lanzamiento de álbum",xlabel="Año",ylabel="Registros de canciones");_save(figs,"05_anios.png")
    corr=correlations(df)
    fig,ax=plt.subplots(figsize=(8,6));im=ax.imshow(corr,vmin=-1,vmax=1,cmap="BrBG");ax.set_xticks(range(len(corr)),["Popularidad canción","Popularidad artista","log10 seguidores","Duración"],rotation=28,ha="right");ax.set_yticks(range(len(corr)),["Popularidad canción","Popularidad artista","log10 seguidores","Duración"])
    for i in range(len(corr)):
      for j in range(len(corr)):
        val=corr.iloc[i,j];ax.text(j,i,f"{val:.2f}" if np.isfinite(val) else "—",ha="center",va="center",color="black")
    fig.colorbar(im,ax=ax,shrink=.7);ax.set(title="Correlaciones de Pearson (descriptivas)");_save(figs,"06_correlaciones.png")
    fig,ax=plt.subplots(figsize=(11,5)); x=df.artist_followers; y=df.track_popularity; mask=x.notna()&y.notna();ax.scatter(np.log10(x[mask]+1),y[mask],s=7,alpha=.18,color=BLUE);ax.set(title="Seguidores del artista vs. popularidad de canciones",xlabel="log10(seguidores + 1)",ylabel="Popularidad de canciones (0–100)");_save(figs,"07_seguidores.png")
    fig,ax=plt.subplots(figsize=(9,5));p=df.groupby("explicit").track_popularity.agg(["mean","count"]);p=p.reindex([False,True]).dropna();ax.bar(["No explícita" if x is False or x==False else "Explícita" for x in p.index],p["mean"],color=["#7BBE9E",BLUE][:len(p)]);ax.set(title="Popularidad media por contenido explícito",ylabel="Popularidad media de canciones (0–100)");_save(figs,"08_explicit.png")
    (dest/"metrics.json").write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding="utf-8")
    a.to_csv(dest/"top_artists.csv",index=False);t[["track_name","artist_name","track_popularity"]].to_csv(dest/"top_tracks.csv",index=False)
    return metrics
