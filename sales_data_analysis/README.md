# Sales Data Analysis
A small project that looks at sales time series data. Touches on some key areas of data analysis:
  
## Pandas Functions
- `pd.read_csv()` + `pd.concat` to staple together a bunch of csv data and get it indexed appropriately for easy time series manipulations.
- `.resample()` To downsample data to daily and also 6-hour dayparts, and aggregate across columns with custom lambda functions.
- `.groupby()` Ever useful function, used here to find which part of the day over the timeframe represented accounts for greatest sales.
- `.diff()` + `nlargest()` to see the greatest daily change.

## Hypotheis Testing
- `stats.ttest_inf()` To compare means of time series data between different periods.
- `stats.ttest_1samp()` To determine the statistical significance of a pronounced difference.
- p-value interpretation. Scipy makes things almost too easy--hours of youtube stats videos reduced down to a single line of code. Use these tools carefully.

## Data Visualization
- Rocked some subplots, and plenty of different cosmetic functions to make the plots look like how I wanted them to.
- `ax.twinx()` to create a second, right side y-axis to overlay two trends of different numeric ranges over the same x-axis time period to see how the trends relate.
