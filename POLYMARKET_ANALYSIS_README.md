# Polymarket Google Trends Analysis

## Overview

This project analyzes Google search trends to estimate who is leading the **"#1 Searched Person on Google This Year"** market on Polymarket.

The analysis uses the `pytrends` library to collect weekly Google search interest data for all candidates since January 1, 2024, and determines the leader based on total search volume.

## Files

### Analysis Scripts

1. **`polymarket_google_trends_analysis.py`** - Main script for real Google Trends data
   - Fetches actual search data from Google Trends API
   - Processes data in batches to avoid rate limiting
   - Includes retry logic and error handling

2. **`polymarket_google_trends_demo.py`** - Demo script with sample data
   - Uses realistic simulated data
   - Perfect for testing and understanding the analysis methodology
   - No API calls, runs immediately

### Output Files (in `analysis_output/` directory)

- **`total_interest_ranking.png`** - Bar chart showing total search interest for all candidates
- **`average_interest_ranking.png`** - Bar chart showing average weekly search interest
- **`peak_interest_ranking.png`** - Bar chart showing peak search interest moments
- **`top5_trends_over_time.png`** - Line chart showing how the top 5 candidates' search interest evolved over time
- **`raw_trends_data_demo.csv`** - Complete raw data with weekly interest scores
- **`summary_statistics_demo.csv`** - Summary table with all key metrics

## Candidates Analyzed

The current list includes 12 candidates from the Polymarket market:

1. Bianca Censori
2. Taylor Swift
3. Travis Kelce
4. Donald Trump
5. Elon Musk
6. Kanye West
7. Brittney Spears
8. Kate Middleton
9. Joe Biden
10. Zendaya
11. Tom Holland
12. Kim Kardashian

## Installation

### Prerequisites

- Python 3.7+
- pip

### Install Required Packages

```bash
pip install pytrends pandas numpy matplotlib
```

## Usage

### Option 1: Demo Version (Recommended First)

Run the demo version to see the complete analysis with sample data:

```bash
python3 polymarket_google_trends_demo.py
```

This will:
- Generate realistic sample data for all candidates
- Perform complete analysis
- Create all visualizations
- Save results to `analysis_output/` directory

### Option 2: Real Data Version

Run the main script to fetch actual Google Trends data:

```bash
python3 polymarket_google_trends_analysis.py
```

**Important Notes:**
- This script makes actual API calls to Google Trends
- Google may rate limit requests (HTTP 429 errors)
- If you encounter rate limiting, wait a few hours and try again
- The script includes automatic retry logic with delays
- Processing takes several minutes due to rate limiting delays

## Analysis Methodology

### 1. Data Collection

The script collects weekly Google search interest data for each candidate from January 1, 2024 to the present day.

**Batching Strategy:**
- Candidates are processed in batches of 5 (Google Trends API limit)
- 15-second delays between batches to avoid rate limiting
- Automatic retry logic with 60-second delays on failures

### 2. Metrics Calculated

For each candidate, the analysis computes:

- **Total Search Interest**: Sum of all weekly interest scores (primary ranking metric)
- **Average Weekly Interest**: Mean interest score across all weeks
- **Peak Interest**: Highest weekly interest score achieved
- **Significant Weeks**: Number of weeks with interest ≥ 10

### 3. Determining the Leader

The leader is determined by **total search interest** - the candidate with the highest cumulative search volume throughout 2024.

This metric is most appropriate because:
- It reflects sustained interest over time, not just viral moments
- It accounts for both consistency and peak popularity
- It aligns with "searched person of the year" - cumulative annual impact

### 4. Visualizations

Four comprehensive visualizations are generated:

1. **Total Interest Ranking** - Shows overall leader (winner highlighted in gold)
2. **Trends Over Time** - Compares top 5 candidates' weekly performance
3. **Average Interest** - Shows consistency of search interest
4. **Peak Interest** - Highlights biggest viral moments

## Demo Results (Sample Data)

Based on the demo run with realistic sample data:

```
RANKING BY TOTAL SEARCH INTEREST (2024):
--------------------------------------------------------------------------------
 1. Taylor Swift         | Total:   8060 | Avg:  83.1 | Peak: 100 | Active weeks: 97
 2. Donald Trump         | Total:   7102 | Avg:  73.2 | Peak: 100 | Active weeks: 97
 3. Kate Middleton       | Total:   5586 | Avg:  57.6 | Peak: 100 | Active weeks: 94
 4. Elon Musk            | Total:   5160 | Avg:  53.2 | Peak:  99 | Active weeks: 96
 5. Travis Kelce         | Total:   4741 | Avg:  48.9 | Peak:  92 | Active weeks: 94
```

🏆 **Current Leader (Demo Data): Taylor Swift** with a total search interest score of 8,060

## Customization

### Adding/Removing Candidates

Edit the `people` list at the top of either script:

```python
people = [
    "Person 1",
    "Person 2",
    # Add more names here
]
```

### Adjusting Time Period

Modify the `timeframe` variable:

```python
timeframe = "2024-01-01 2024-12-31"  # Custom date range
```

### Changing Analysis Parameters

- **Batch size**: Modify `batch_size` (max 5 due to Google Trends API limit)
- **Delays**: Adjust `time.sleep()` values (increase if hitting rate limits)
- **Significant interest threshold**: Change the `>= 10` filter in significant weeks calculation

## Troubleshooting

### Issue: "The request failed: Google returned a response with code 429"

**Solution**: You've hit Google Trends rate limiting.
- Wait 2-4 hours before trying again
- Run the demo version in the meantime
- Consider analyzing fewer candidates at once

### Issue: "No data was collected"

**Solution**:
- Check your internet connection
- Verify candidate names are spelled correctly
- Increase delays between batches
- Try running at a different time of day

### Issue: Missing visualizations

**Solution**:
- Ensure matplotlib is installed: `pip install matplotlib`
- Check that the `analysis_output/` directory was created
- Verify Python has write permissions in the current directory

## Technical Details

### API Rate Limiting Strategy

The script implements several strategies to handle Google Trends rate limiting:

1. **Batch Processing**: Groups 5 candidates per request (API maximum)
2. **Progressive Delays**: 15-second delays between successful batches
3. **Exponential Backoff**: 60-second delay after failures, with one retry attempt
4. **Clean Error Handling**: Gracefully handles 429 errors with informative messages

### Data Format

Google Trends returns interest scores on a 0-100 scale:
- **100**: Peak search interest for the given time period
- **50**: Half the peak interest
- **0**: Less than 1% of peak interest

**Important**: Scores are relative to each query's own peak, not absolute search volumes. The analysis compares cumulative scores within the same time frame, making them comparable.

## Output Interpretation

### Understanding the Rankings

- **Total Interest**: Best indicator for "person of the year" (cumulative impact)
- **Average Interest**: Shows consistency and sustained relevance
- **Peak Interest**: Identifies biggest viral moments or news events
- **Active Weeks**: Shows longevity of public interest

### Reading the Visualizations

1. **Bar Charts**: Longer bars = higher interest (winner in gold)
2. **Time Series**: Spikes indicate major news events or viral moments
3. **Relative Comparison**: All metrics are relative to the analysis time period

## Further Analysis

### Possible Extensions

1. **Regional Analysis**: Add `geo='US'` parameter for country-specific trends
2. **Category Filtering**: Use `cat=` parameter to focus on specific search categories
3. **Related Queries**: Use `pytrends.related_queries()` to understand search context
4. **Sentiment Analysis**: Combine with news API to analyze why interest peaked
5. **Prediction Model**: Use time series forecasting to predict year-end leader

### Export Options

All data is exported to CSV for further analysis in:
- Excel/Google Sheets
- Tableau/Power BI
- R or other statistical software
- Custom Python analysis scripts

## References

- [Polymarket](https://polymarket.com/) - Prediction market platform
- [pytrends Documentation](https://pypi.org/project/pytrends/) - Google Trends API
- [Google Trends](https://trends.google.com/) - Official Google Trends site

## License

This analysis script is provided for educational and research purposes.

## Disclaimer

This analysis is based on Google search data and is for informational purposes only. It does not constitute financial advice. Google Trends data is subject to Google's terms of service.

---

**Last Updated**: November 10, 2025
**Author**: Polymarket Analysis Project
**Version**: 1.0
