import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class AgregadosPorGrupo(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass


    def fit(self, X, y):
        df_temp=pd.concat([X,y], axis=1)
        conteo = df_temp.groupby('main_artist')['popularity'].count()
        artistas_validos = conteo[conteo >= 5].index
        df_artistas = df_temp[df_temp['main_artist'].isin(artistas_validos)]
        self.artist_means_ =df_artistas.groupby('main_artist')['popularity'].mean()
        self.artist_stds_ =df_artistas.groupby('main_artist')['popularity'].std()
        self.artist_counts_ =df_artistas.groupby('main_artist')['popularity'].count()
        self.track_genre_means_ =df_temp.groupby('track_genre')['popularity'].mean()
        self.track_genre_stds_ =df_temp.groupby('track_genre')['popularity'].std()
        self.track_genre_counts_ =df_temp.groupby('track_genre')['popularity'].count()
        self.global_mean_ = y.mean()
        self.global_std_ = y.std()
        self.global_count_ = y.count()
        return self
    
    def transform(self, X):
        X = X.copy()
        X['artist_mean_popularity'] = X['main_artist'].map(self.artist_means_).fillna(self.global_mean_)
        X['artist_std_popularity'] = X['main_artist'].map(self.artist_stds_).fillna(self.global_std_)
        X['artist_count_popularity'] = X['main_artist'].map(self.artist_counts_).fillna(1)
        
        X['track_genre_mean_popularity'] = X['track_genre'].map(self.track_genre_means_).fillna(self.global_mean_)
        X['track_genre_std_popularity'] = X['track_genre'].map(self.track_genre_stds_).fillna(self.global_std_)
        X['track_genre_count_popularity'] = X['track_genre'].map(self.track_genre_counts_).fillna(1)
        X = X.drop(columns=['main_artist', 'album_name', 'track_genre'])
        return X