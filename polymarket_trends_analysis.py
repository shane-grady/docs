"""
Polymarket Google Trends Analysis
Analyzes Google search trends to estimate the leader in the
"#1 Searched Person on Google This Year" market on Polymarket
"""

from pytrends.request import TrendReq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import time
import warnings
warnings.filterwarnings('ignore')

# List of candidates from Polymarket market (as of Nov 2025)
people = [
    "Pope Leo XIV",
    "Bianca Censori",
    "Donald Trump",
    "Jimmy Kimmel",
    "Kendrick Lamar",
    "Elon Musk",
    "Zohran Mamdani",
    "Luigi Mangione",
    "Andy Byron",
    "Kanye West",
    "Charlie Kirk",
    "Bad Bunny",
    "Taylor Swift",
    "Kate Middleton",
    "Joe Biden",
    "Travis Kelce",
    "Kim Kardashian"
]

print("=" * 80)
print("POLYMARKET GOOGLE TRENDS ANALYSIS")
print("Market: #1 Searched Person on Google This Year (2025)")
print("=" * 80)
print(f"\nAnalyzing {len(people)} candidates...")
print(f"Date range: 2025-01-01 to {date.today()}\n")

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2, backoff_factor=0.1)
timeframe = f"2025-01-01 {date.today()}"

# Collect data for all people
all_data = pd.DataFrame()
failed_queries = []

print("Fetching Google Trends data...\n")

for i, person in enumerate(people, 1):
    try:
        print(f"[{i}/{len(people)}] Fetching data for: {person}")
        pytrends.build_payload([person], timeframe=timeframe, geo='')
        df = pytrends.interest_over_time()

        if df.empty or person not in df.columns:
            print(f"  ⚠ No data available for {person}")
            failed_queries.append(person)
            continue

        df = df.reset_index()
        df = df.rename(columns={person: "interest"})
        df["person"] = person
        df = df[["date", "person", "interest"]]

        all_data = pd.concat([all_data, df], ignore_index=True)
        print(f"  ✓ Successfully fetched data")

        # Rate limiting
        time.sleep(1)

    except Exception as e:
        print(f"  ✗ Error fetching data for {person}: {str(e)}")
        failed_queries.append(person)
        time.sleep(2)

print("\n" + "=" * 80)
print("DATA COLLECTION COMPLETE")
print("=" * 80)

if failed_queries:
    print(f"\n⚠ Failed to fetch data for {len(failed_queries)} candidates:")
    for person in failed_queries:
        print(f"  - {person}")

# Calculate aggregate metrics
print("\n" + "=" * 80)
print("ANALYSIS RESULTS")
print("=" * 80)

summary = all_data.groupby("person")["interest"].agg([
    ('total', 'sum'),
    ('average', 'mean'),
    ('peak', 'max'),
    ('median', 'median')
]).round(2)

summary = summary.sort_values('total', ascending=False)

print("\n📊 RANKINGS BY TOTAL SEARCH INTEREST (2025 Year-to-Date)")
print("-" * 80)
print(f"{'Rank':<6} {'Person':<25} {'Total':<12} {'Average':<12} {'Peak':<10}")
print("-" * 80)

for rank, (person, row) in enumerate(summary.iterrows(), 1):
    print(f"{rank:<6} {person:<25} {row['total']:<12.0f} {row['average']:<12.2f} {row['peak']:<10.0f}")

# Calculate market share
print("\n📈 MARKET SHARE (% of Total Search Interest)")
print("-" * 80)
total_interest = summary['total'].sum()
summary['market_share'] = (summary['total'] / total_interest * 100).round(2)

for rank, (person, row) in enumerate(summary.iterrows(), 1):
    bar = "█" * int(row['market_share'] * 2)
    print(f"{rank:2}. {person:<25} {row['market_share']:>6.2f}% {bar}")

# Top 5 detailed analysis
print("\n🏆 TOP 5 CANDIDATES - DETAILED METRICS")
print("-" * 80)

top5 = summary.head(5)
for rank, (person, row) in enumerate(top5.iterrows(), 1):
    print(f"\n#{rank} {person}")
    print(f"  Total Interest: {row['total']:,.0f}")
    print(f"  Average Weekly Interest: {row['average']:.2f}")
    print(f"  Peak Interest: {row['peak']:.0f}")
    print(f"  Median Interest: {row['median']:.2f}")
    print(f"  Market Share: {row['market_share']:.2f}%")

# Monthly trends for top candidates
print("\n📅 MONTHLY TRENDS FOR TOP 5 CANDIDATES")
print("-" * 80)

all_data['month'] = pd.to_datetime(all_data['date']).dt.to_period('M')
top5_names = summary.head(5).index.tolist()
monthly_data = all_data[all_data['person'].isin(top5_names)].groupby(['month', 'person'])['interest'].mean().reset_index()

for person in top5_names:
    person_monthly = monthly_data[monthly_data['person'] == person]
    print(f"\n{person}:")
    for _, row in person_monthly.iterrows():
        print(f"  {row['month']}: {row['interest']:.2f}")

# Save detailed data
output_file = "polymarket_trends_detailed.csv"
all_data.to_csv(output_file, index=False)
print(f"\n💾 Detailed data saved to: {output_file}")

summary_file = "polymarket_trends_summary.csv"
summary.to_csv(summary_file)
print(f"💾 Summary statistics saved to: {summary_file}")

print("\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)

leader = summary.index[0]
leader_total = summary.iloc[0]['total']
leader_share = summary.iloc[0]['market_share']

print(f"\n🎯 ESTIMATED LEADER: {leader}")
print(f"   Total Search Interest: {leader_total:,.0f}")
print(f"   Market Share: {leader_share:.2f}%")

# Compare with current Polymarket odds
print("\n📊 COMPARISON WITH POLYMARKET ODDS:")
polymarket_odds = {
    "Pope Leo XIV": 48,
    "Bianca Censori": 18,
    "Donald Trump": 9,
    "Kendrick Lamar": 4,
    "Elon Musk": 4,
}

print(f"\n{'Person':<25} {'Google Trends %':<18} {'Polymarket %':<15} {'Difference'}")
print("-" * 80)

for person in summary.head(10).index:
    trends_pct = summary.loc[person, 'market_share']
    polymarket_pct = polymarket_odds.get(person, 0)
    diff = trends_pct - polymarket_pct
    arrow = "📈" if diff > 0 else "📉" if diff < 0 else "➡️"
    print(f"{person:<25} {trends_pct:>6.2f}%{'':<11} {polymarket_pct:>4}%{'':<10} {arrow} {diff:+.2f}%")

print("\n" + "=" * 80)
print("Note: Google Trends data may not perfectly correlate with official")
print("Google Year in Search results. This analysis is for estimation only.")
print("=" * 80)
