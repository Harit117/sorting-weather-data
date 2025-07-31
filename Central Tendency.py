import pandas as pd

df = pd.read_csv(r'C:/Users/Harit/OneDrive/Desktop/Internship project/Assignment 1/4084341.csv')
df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
df['YEAR'] = df['DATE'].dt.year
df['TAVG'] = pd.to_numeric(df['TAVG'], errors='coerce')
df['TAVG_C'] = (df['TAVG'] - 32) * 5 / 9

station_to_state = {
    'USR0000WCEC': 'Washington',
    'USR0000MCAP': 'Massachusetts',
    'USR0000TLAG': 'Texas'
}

df['STATION_DISPLAY'] = df['STATION'].map(station_to_state).fillna(df['STATION'])

summary = df.groupby(['STATION_DISPLAY', 'YEAR'])['TAVG_C'].agg([
    ('TEMP_MEAN_C', 'mean'),
    ('TEMP_MEDIAN_C', 'median'),
    ('TEMP_MAX_C', 'max'),
    ('TEMP_MIN_C', 'min')
])

pd.set_option('display.max_rows', None)
print(summary)
