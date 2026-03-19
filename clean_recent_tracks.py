
import pandas as pd

# load file and return DataFrame
def load_df(data):
    return pd.DataFrame(data)


def clean_data_frame(df):
    # dtypes
    df['played_at'] = pd.to_datetime(df['played_at'])
    return df


# this is for test purposes only
from recent_tracks import test_data
# df = load_df(test_data)
