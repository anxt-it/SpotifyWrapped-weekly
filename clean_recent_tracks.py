
import pandas as pd

# load file and return DataFrame
def load_df(data):
    return pd.DataFrame(data)


def clean_data_frame(df):
    str_columns = ['track_id', 'track_name', 'artist_id', 'artist_name', 'album_id', 'album_name']
    for col in str_columns:
        df[col] = df[col].astype(str)

    return df

# currently does nothing
