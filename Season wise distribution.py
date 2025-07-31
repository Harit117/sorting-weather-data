import pandas as pd

df = pd.read_csv('4084341.csv', parse_dates=['DATE'])
df['MONTH'] = df['DATE'].dt.month
df['YEAR'] = df['DATE'].dt.year

season_map = {
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Spring', 4: 'Spring', 5: 'Spring',
    6: 'Summer', 7: 'Summer', 8: 'Summer',
    9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
}
df['SEASON'] = df['MONTH'].map(season_map)

def map_state(station_code):
    try:
        letter = station_code[-4]
        return {
            'T': 'Texas',
            'W': 'Washington',
            'M': 'Massachusetts'
        }.get(letter, 'Unknown')
    except Exception as e:
        return 'Unknown'

df['STATE'] = df['STATION'].apply(map_state)

seasonal_summary = df.groupby(['STATION', 'STATE', 'SEASON'])['TAVG'].agg([
    ('TEMP_MEDIAN_C', 'median'),
    ('TMAX', 'max'),
    ('TMIN', 'min')
]).reset_index()

print("📍 Seasonal Stats per Station & State:")
print(seasonal_summary)
