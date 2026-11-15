"""Uso: python scripts/run_analysis.py --data data/spotify_data.csv --output reports"""
import argparse
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from spotify_eda.analysis import load_tracks
from spotify_eda.reporting import create_report

if __name__ == "__main__":
    p=argparse.ArgumentParser(description="EDA de Spotify")
    p.add_argument("--data",default="data/spotify_demo.csv",help="Ruta del archivo CSV de canciones")
    p.add_argument("--output",default="reports",help="Carpeta de salida")
    args=p.parse_args()
    metrics=create_report(load_tracks(args.data),args.output)
    print("Reporte creado:",metrics)
