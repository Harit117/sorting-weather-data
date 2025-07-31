import pandas as pd

df = pd.read_csv("4084341.csv", parse_dates=["DATE"])
required_columns = ["DATE", "STATION", "TAVG"]
if not all(col in df.columns for col in required_columns):
    raise ValueError("Missing columns: DATE, STATION, or TAVG")

df = df.dropna(subset=["STATION"])
df["TAVG"] = df["TAVG"].fillna(df["TAVG"].mean())

df["YEAR"] = df["DATE"].dt.year
df["MONTH"] = df["DATE"].dt.month
season_map = {
    12: "Winter", 1: "Winter", 2: "Winter",
    3: "Spring", 4: "Spring", 5: "Spring",
    6: "Summer", 7: "Summer", 8: "Summer",
    9: "Autumn", 10: "Autumn", 11: "Autumn"
}
df["SEASON"] = df["MONTH"].map(season_map)

tx_df = df[df["STATION"] == "USR0000TLAG"]
ma_df = df[df["STATION"] == "USR0000MCAP"]
if tx_df.empty or ma_df.empty:
    raise ValueError("Station data not found for USR0000TLAG or USR0000MCAP")

tx_seasonal = tx_df.groupby(["YEAR", "SEASON"])["TAVG"].mean().reset_index(name="TX_TAVG")
ma_seasonal = ma_df.groupby(["YEAR", "SEASON"])["TAVG"].mean().reset_index(name="MA_TAVG")

merged = pd.merge(ma_seasonal, tx_seasonal, on=["YEAR", "SEASON"])
if merged.empty:
    raise ValueError("No overlapping seasonal data between the stations.")

seasonal_corr = []
for season in ["Winter", "Spring", "Summer", "Autumn"]:
    season_data = merged[merged["SEASON"] == season]
    if len(season_data) >= 2:
        corr = season_data["MA_TAVG"].corr(season_data["TX_TAVG"])
        seasonal_corr.append({"SEASON": season, "CORRELATION": round(corr, 3)})
    else:
        seasonal_corr.append({"SEASON": season, "CORRELATION": None})

results = pd.DataFrame(seasonal_corr)
print(results)
