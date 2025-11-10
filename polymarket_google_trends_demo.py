#!/usr/bin/env python3
"""
Polymarket Google Trends Analysis - DEMO VERSION
Demonstrates the analysis with sample data (simulating realistic Google Trends patterns)
Run the main script later when rate limits reset to get real data.
"""

import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import os

np.random.seed(42)

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
print("POLYMARKET GOOGLE TRENDS ANALYSIS - DEMO VERSION")
print("#1 Searched Person on Google This Year")
print("=" * 80)
print(f"\nAnalyzing {len(people)} candidates from Polymarket market")
print(f"Time period: 2024-01-01 to {date.today()}")
print("\nCandidates:", ", ".join(people))
print("\n" + "=" * 80)

# Step 2: Generate realistic sample data (simulating Google Trends patterns)
print("\n[STEP 1] Generating sample Google Trends data...\n")
print("NOTE: This is DEMO data based on realistic search patterns.")
print("      Run polymarket_google_trends_analysis.py for real data.\n")

# Generate weekly dates from Jan 1, 2024 to now
start_date = datetime(2024, 1, 1)
end_date = datetime.now()
weeks = pd.date_range(start=start_date, end=end_date, freq='W-SUN')

all_data = pd.DataFrame()

# Define realistic baseline interest levels and volatility for each person
person_profiles = {
    "Taylor Swift": {"base": 75, "volatility": 15, "trend": 0.05},
    "Donald Trump": {"base": 70, "volatility": 20, "trend": 0.1},
    "Kate Middleton": {"base": 55, "volatility": 25, "trend": 0.0},
    "Elon Musk": {"base": 50, "volatility": 15, "trend": -0.02},
    "Travis Kelce": {"base": 45, "volatility": 20, "trend": 0.08},
    "Joe Biden": {"base": 40, "volatility": 12, "trend": -0.05},
    "Kim Kardashian": {"base": 35, "volatility": 10, "trend": 0.0},
    "Bianca Censori": {"base": 30, "volatility": 18, "trend": 0.03},
    "Kanye West": {"base": 28, "volatility": 15, "trend": -0.03},
    "Zendaya": {"base": 25, "volatility": 12, "trend": 0.02},
    "Brittney Spears": {"base": 20, "volatility": 10, "trend": -0.01},
    "Tom Holland": {"base": 22, "volatility": 11, "trend": 0.01},
}

for person in people:
    profile = person_profiles[person]

    # Generate realistic time series with trend, seasonality, and random spikes
    interests = []
    for i, week in enumerate(weeks):
        # Base interest with trend
        base_interest = profile["base"] + (profile["trend"] * i)

        # Add weekly random variation
        noise = np.random.normal(0, profile["volatility"])

        # Add occasional spikes (news events)
        spike = 0
        if np.random.random() < 0.1:  # 10% chance of spike
            spike = np.random.uniform(10, 40)

        # Calculate final interest (0-100 scale)
        interest = max(0, min(100, base_interest + noise + spike))
        interests.append(interest)

    # Create DataFrame for this person
    person_df = pd.DataFrame({
        'date': weeks,
        'person': person,
        'interest': interests
    })

    all_data = pd.concat([all_data, person_df], ignore_index=True)
    print(f"  ✓ Generated {len(weeks)} weeks of data for: {person}")

print(f"\n✓ Data generation complete! Total records: {len(all_data)}\n")

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
colors = ['gold' if i == 0 else 'steelblue' for i in range(len(total_interest))]
total_interest.plot(kind='barh', color=colors)
plt.xlabel('Total Search Interest (2024)', fontsize=12, fontweight='bold')
plt.ylabel('Person', fontsize=12, fontweight='bold')
plt.title('Total Google Search Interest - 2024 (DEMO DATA)\nPolymarket: #1 Searched Person on Google This Year',
          fontsize=14, fontweight='bold', pad=20)
plt.gca().invert_yaxis()
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('analysis_output/total_interest_ranking.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: analysis_output/total_interest_ranking.png")

# Visualization 2: Time series comparison of top 5
plt.figure(figsize=(16, 8))
top_5 = total_interest.head(5).index
colors_ts = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']

for i, person in enumerate(top_5):
    person_data = all_data[all_data['person'] == person].sort_values('date')
    plt.plot(person_data['date'], person_data['interest'], marker='o',
             linewidth=2.5, markersize=4, label=person, alpha=0.85, color=colors_ts[i])

plt.xlabel('Date', fontsize=12, fontweight='bold')
plt.ylabel('Search Interest', fontsize=12, fontweight='bold')
plt.title('Google Trends Over Time - Top 5 Candidates (2024) - DEMO DATA\nPolymarket: #1 Searched Person on Google This Year',
          fontsize=14, fontweight='bold', pad=20)
plt.legend(loc='best', fontsize=11, framealpha=0.9)
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('analysis_output/top5_trends_over_time.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: analysis_output/top5_trends_over_time.png")

# Visualization 3: Average weekly interest comparison
plt.figure(figsize=(14, 8))
colors_avg = ['gold' if i == 0 else 'coral' for i in range(len(avg_interest))]
avg_interest.plot(kind='barh', color=colors_avg)
plt.xlabel('Average Weekly Search Interest', fontsize=12, fontweight='bold')
plt.ylabel('Person', fontsize=12, fontweight='bold')
plt.title('Average Weekly Google Search Interest - 2024 (DEMO DATA)\nPolymarket: #1 Searched Person on Google This Year',
          fontsize=14, fontweight='bold', pad=20)
plt.gca().invert_yaxis()
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('analysis_output/average_interest_ranking.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: analysis_output/average_interest_ranking.png")

# Visualization 4: Peak interest comparison (new)
plt.figure(figsize=(14, 8))
colors_peak = ['gold' if i == 0 else 'lightcoral' for i in range(len(peak_interest))]
peak_interest.plot(kind='barh', color=colors_peak)
plt.xlabel('Peak Search Interest', fontsize=12, fontweight='bold')
plt.ylabel('Person', fontsize=12, fontweight='bold')
plt.title('Peak Google Search Interest - 2024 (DEMO DATA)\nPolymarket: #1 Searched Person on Google This Year',
          fontsize=14, fontweight='bold', pad=20)
plt.gca().invert_yaxis()
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('analysis_output/peak_interest_ranking.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: analysis_output/peak_interest_ranking.png")

# Save raw data to CSV
all_data.to_csv('analysis_output/raw_trends_data_demo.csv', index=False)
print("  ✓ Saved: analysis_output/raw_trends_data_demo.csv")

# Save summary statistics
summary = pd.DataFrame({
    'Total Interest': total_interest,
    'Average Interest': avg_interest,
    'Peak Interest': peak_interest,
    'Significant Weeks (>=10)': significant_weeks
}).fillna(0)
summary['Rank'] = range(1, len(summary) + 1)
summary = summary[['Rank', 'Total Interest', 'Average Interest', 'Peak Interest', 'Significant Weeks (>=10)']]
summary.to_csv('analysis_output/summary_statistics_demo.csv')
print("  ✓ Saved: analysis_output/summary_statistics_demo.csv")

print("\n" + "=" * 80)
print("DEMO ANALYSIS COMPLETE!")
print("=" * 80)
print(f"\n📊 All results saved to: ./analysis_output/")
print("\nFiles generated:")
print("  - total_interest_ranking.png")
print("  - top5_trends_over_time.png")
print("  - average_interest_ranking.png")
print("  - peak_interest_ranking.png")
print("  - raw_trends_data_demo.csv")
print("  - summary_statistics_demo.csv")
print("\n" + "=" * 80)
print("\n⚠️  IMPORTANT: This analysis uses DEMO DATA")
print("   Run 'python3 polymarket_google_trends_analysis.py' for real Google Trends data")
print("   (Wait a few hours if you hit rate limits)")
print("=" * 80)
