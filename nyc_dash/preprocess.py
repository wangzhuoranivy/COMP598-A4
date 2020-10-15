import pandas as pd

def get_df():
    df = pd.read_csv('~/nyc_dash/nyc_311_trim.csv',usecols=[1,2,8],names=['open_date','close_date','zip_code'])

    # eliminate rows without close date and zip cod
    df.dropna(inplace=True)

    # extract months in month col
    df['month'] = df['close_date'].str.slice(0,2)

    # duration for each case
    df['close_date'] = pd.to_datetime(df['close_date'], format='%m/%d/%Y %I:%M:%S %p')
    df['open_date'] = pd.to_datetime(df['open_date'], format='%m/%d/%Y %I:%M:%S %p')
    df['duration'] = (df.close_date - df.open_date) / pd.Timedelta(hours=1)

    # remove negative duration rows
    df = df[df['duration']>=0]

    return(df)

