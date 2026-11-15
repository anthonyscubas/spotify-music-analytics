import pandas as pd
import pytest
from spotify_eda.analysis import load_tracks, summary, top_artists, genres

def _base(tmp_path):
    p=tmp_path/"d.csv"
    pd.DataFrame({"track_id":["a","a","b","c"],"track_name":["A","A","B","C"],"track_popularity":[60,60,90,250],"artist_name":["Alpha","Alpha","Beta","Beta"],"artist_popularity":[45,45,80,80],"artist_followers":[100,100,200,200],"artist_genres":["pop, dance","pop, dance",None,"rock"],"album_release_date":["2020-01-01"]*4,"track_duration_min":[3,3,4,-1],"explicit":[False,False,True,False]}).to_csv(p,index=False)
    return p

def test_deduplicates_ids(tmp_path):
    d=load_tracks(_base(tmp_path));assert len(d)==3

def test_invalid_popularity_and_duration(tmp_path):
    d=load_tracks(_base(tmp_path));assert pd.isna(d.loc[d.track_id=='c','track_popularity'].iloc[0]);assert pd.isna(d.loc[d.track_id=='c','track_duration_min'].iloc[0])

def test_genres_multivalue(tmp_path):
    d=load_tracks(_base(tmp_path));assert genres(d).loc['dance']==1

def test_minimum_tracks(tmp_path):
    d=load_tracks(_base(tmp_path));assert len(top_artists(d,min_tracks=2))==0
    assert len(top_artists(d,min_tracks=1))==2

def test_metrics(tmp_path):
    d=load_tracks(_base(tmp_path));assert summary(d)['tracks']==3

def test_missing_columns(tmp_path):
    p=tmp_path/'bad.csv';pd.DataFrame({'track_id':['a']}).to_csv(p,index=False)
    with pytest.raises(ValueError):load_tracks(p)
