
import pandas as pd
from numpy import integer, int64


# load file and return DataFrame
def load_df(data):
    return pd.DataFrame(data)


def clean_data_frame(df):
    # duplicates
    df = df.drop_duplicates(subset=['played_at']).reset_index(drop=True)


    # data types
    str_columns = ['track_id', 'track_name', 'artist_id', 'artist_name', 'album_id', 'album_name']
    for col in str_columns:
        df[col] = df[col].astype(str)

    rows_to_insert = [tuple(map(lambda x: int(x) if isinstance(x, (integer, int64)) else x, row))
               for row in df.to_records(index=False)]

    return rows_to_insert

