#!/usr/bin/env python3
"""
Polymarket Google Trends Analysis
Estimates who is leading the "#1 Searched Person on Google This Year" market
"""

from pytrends.request import TrendReq
import pandas as pd
import numpy as np
from datetime import date
import matplotlib.pyplot as plt
import time
import os

# Step 1: Define the list of candidates from the Polymarket market
people = [
    "Bianca Censori",
    "Taylor Swift",
    "Travis Kelce",
    "Donald Trump",
    "Elon Musk",
    "Kanye West",
    "Brittney Spears",
    "Kate Middleton",
    "Joe Biden",
    "Zendaya",
    "Tom Holland",
    "Kim Kardashian"
]

print("=" * 80)
print("POLYMARKET GOOGLE TRENDS ANALYSIS")
print("#1 Searched Person on Google This Year")
print("=" * 80)
print(f"\nAnalyzing {len(people)} candidates from Polymarket market")
print(f"Time period: 2024-01-01 to {date.today()}")
print("\nCandidates:", ", ".join(people))
print("\n" + "=" * 80)

# Step 2: Data Collection
print("\n[STEP 1] Collecting Google Trends data...\n")
print("NOTE: Using batch mode (5 people per request) to avoid rate limits\n")

pytrends = TrendReq(hl='en-US', tz=360)
timeframe = f"2024-01-01 {str(date.today())}"
all_data = pd.DataFrame()

# Process in batches of 5 (Google Trends limit for comparison)
batch_size = 5
for batch_num in range(0, len(people), batch_size):
    batch = people[batch_num:batch_num + batch_size]
    batch_label = f"Batch {batch_num//batch_size + 1}/{(len(people)-1)//batch_size + 1}"

    try:
        print(f"  [{batch_label}] Fetching data for: {', '.join(batch)}...")
        pytrends.build_payload(batch, timeframe=timeframe, geo='')
        df = pytrends.interest_over_time()

        if df is not None and not df.empty:
            # Remove the 'isPartial' column if it exists
            if 'isPartial' in df.columns:
                df = df.drop(columns=['isPartial'])

            # Reshape the data from wide to long format
            df = df.reset_index()
            df_melted = df.melt(id_vars=['date'], var_name='person', value_name='interest')
            all_data = pd.concat([all_data, df_melted], ignore_index=True)
            print(f"    ✓ Retrieved {len(df)} weeks of data for {len(batch)} people")
        else:
            print("    ✗ No data returned")

        # Add substantial delay between batches to avoid rate limiting
        if batch_num + batch_size < len(people):
            delay = 15
            print(f"    Waiting {delay} seconds before next batch...\n")
            time.sleep(delay)

    except Exception as e:
        print(f"    ✗ Error: {str(e)}")
        print(f"    Waiting 60 seconds before retrying...\n")
        time.sleep(60)

        # Retry once with longer delay
        try:
            print(f"  [{batch_label}] Retrying: {', '.join(batch)}...")
            pytrends = TrendReq(hl='en-US', tz=360)
            pytrends.build_payload(batch, timeframe=timeframe, geo='')
            df = pytrends.interest_over_time()

            if df is not None and not df.empty:
                if 'isPartial' in df.columns:
                    df = df.drop(columns=['isPartial'])
                df = df.reset_index()
                df_melted = df.melt(id_vars=['date'], var_name='person', value_name='interest')
                all_data = pd.concat([all_data, df_melted], ignore_index=True)
                print(f"    ✓ Retrieved {len(df)} weeks of data for {len(batch)} people")
            time.sleep(15)
        except Exception as e2:
            print(f"    ✗ Retry failed: {str(e2)}")
            time.sleep(30)

if all_data.empty:
    print("\n✗ ERROR: No data was collected due to rate limiting.")
    print("   This can happen when Google Trends detects too many requests.")
    print("   Please try again later or run with a smaller list of people.\n")
    exit(1)

print(f"\n✓ Data collection complete! Total records: {len(all_data)}\n")

# Step 3: Data Analysis
print("=" * 80)
print("[STEP 2] Analyzing search trends...\n")

# Calculate total search interest for each person
total_interest = all_data.groupby('person')['interest'].sum().sort_values(ascending=False)

# Calculate average weekly interest
avg_interest = all_data.groupby('person')['interest'].mean().sort_values(ascending=False)

# Calculate peak interest
peak_interest = all_data.groupby('person')['interest'].max().sort_values(ascending=False)

# Count weeks with significant interest (>= 10)
significant_weeks = all_data[all_data['interest'] >= 10].groupby('person').size().sort_values(ascending=False)

print("RANKING BY TOTAL SEARCH INTEREST (2024):")
print("-" * 80)
for rank, (person, score) in enumerate(total_interest.items(), 1):
    avg = avg_interest[person]
    peak = peak_interest[person]
    sig_weeks = significant_weeks.get(person, 0)

    print(f"{rank:2d}. {person:20s} | Total: {score:6.0f} | Avg: {avg:5.1f} | Peak: {peak:3.0f} | Active weeks: {sig_weeks}")

# Step 4: Determine the leader
leader = total_interest.index[0]
leader_score = total_interest.iloc[0]

print("\n" + "=" * 80)
print("RESULT:")
print("=" * 80)
print(f"🏆 CURRENT LEADER: {leader}")
print(f"   Total search interest score: {leader_score:.0f}")
print(f"   Average weekly interest: {avg_interest[leader]:.1f}")
print(f"   Peak interest: {peak_interest[leader]:.0f}")
print("=" * 80)

# Step 5: Create visualizations
print("\n[STEP 3] Generating visualizations...\n")

# Create output directory if it doesn't exist
os.makedirs('analysis_output', exist_ok=True)

# Visualization 1: Bar chart of total search interest
plt.figure(figsize=(14, 8))
total_interest.plot(kind='barh', color='steelblue')
plt.xlabel('Total Search Interest (2024)', fontsize=12, fontweight='bold')
plt.ylabel('Person', fontsize=12, fontweight='bold')
plt.title('Total Google Search Interest - 2024\nPolymarket: #1 Searched Person on Google This Year',
          fontsize=14, fontweight='bold', pad=20)
plt.gca().invert_yaxis()
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('analysis_output/total_interest_ranking.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: analysis_output/total_interest_ranking.png")

# Visualization 2: Time series comparison of top 5
plt.figure(figsize=(16, 8))
top_5 = total_interest.head(5).index

for person in top_5:
    person_data = all_data[all_data['person'] == person].sort_values('date')
    plt.plot(person_data['date'], person_data['interest'], marker='o',
             linewidth=2, markersize=3, label=person, alpha=0.8)

plt.xlabel('Date', fontsize=12, fontweight='bold')
plt.ylabel('Search Interest', fontsize=12, fontweight='bold')
plt.title('Google Trends Over Time - Top 5 Candidates (2024)\nPolymarket: #1 Searched Person on Google This Year',
          fontsize=14, fontweight='bold', pad=20)
plt.legend(loc='best', fontsize=10)
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('analysis_output/top5_trends_over_time.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: analysis_output/top5_trends_over_time.png")

# Visualization 3: Average weekly interest comparison
plt.figure(figsize=(14, 8))
avg_interest.plot(kind='barh', color='coral')
plt.xlabel('Average Weekly Search Interest', fontsize=12, fontweight='bold')
plt.ylabel('Person', fontsize=12, fontweight='bold')
plt.title('Average Weekly Google Search Interest - 2024\nPolymarket: #1 Searched Person on Google This Year',
          fontsize=14, fontweight='bold', pad=20)
plt.gca().invert_yaxis()
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('analysis_output/average_interest_ranking.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: analysis_output/average_interest_ranking.png")

# Save raw data to CSV
all_data.to_csv('analysis_output/raw_trends_data.csv', index=False)
print("  ✓ Saved: analysis_output/raw_trends_data.csv")

# Save summary statistics
summary = pd.DataFrame({
    'Total Interest': total_interest,
    'Average Interest': avg_interest,
    'Peak Interest': peak_interest,
    'Significant Weeks (>=10)': significant_weeks
}).fillna(0)
summary['Rank'] = range(1, len(summary) + 1)
summary = summary[['Rank', 'Total Interest', 'Average Interest', 'Peak Interest', 'Significant Weeks (>=10)']]
summary.to_csv('analysis_output/summary_statistics.csv')
print("  ✓ Saved: analysis_output/summary_statistics.csv")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print(f"\n📊 All results saved to: ./analysis_output/")
print("\nFiles generated:")
print("  - total_interest_ranking.png")
print("  - top5_trends_over_time.png")
print("  - average_interest_ranking.png")
print("  - raw_trends_data.csv")
print("  - summary_statistics.csv")
print("\n" + "=" * 80)
