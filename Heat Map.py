import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('4084341.csv', parse_dates=['DATE'])

season_map = {
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Spring', 4: 'Spring', 5: 'Spring',
    6: 'Summer', 7: 'Summer', 8: 'Summer',
    9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
}
df['MONTH'] = df['DATE'].dt.month
df['SEASON'] = df['MONTH'].map(season_map)

seasonal_summary = df.groupby(['STATION', 'SEASON'])['TAVG'].agg([
    ('TEMP_MEDIAN_C', 'median'),
    ('TMAX', 'max'),
    ('TMIN', 'min')
]).reset_index()

heatmap_data = seasonal_summary.pivot(index='STATION', columns='SEASON', values='TEMP_MEDIAN_C')

plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="coolwarm", linewidths=0.5)
plt.title("🌡️ Median Seasonal Temperatures per Station")
plt.xlabel("Season")
plt.ylabel("Station")
plt.tight_layout()
plt.show()
