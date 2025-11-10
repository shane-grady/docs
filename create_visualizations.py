"""
Create visualizations for Polymarket Google Trends Analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Read the data
print("Loading data...")
all_data = pd.read_csv("polymarket_trends_detailed.csv")
summary = pd.read_csv("polymarket_trends_summary.csv", index_col=0)

# Convert date column
all_data['date'] = pd.to_datetime(all_data['date'])

# Sort by total interest
summary = summary.sort_values('total', ascending=False)

print(f"Creating visualizations...")

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
colors = plt.cm.tab20(np.linspace(0, 1, 20))

# Figure 1: Top 10 by Total Search Interest
fig, ax = plt.subplots(figsize=(14, 8))
top10 = summary.head(10)
bars = ax.barh(range(len(top10)), top10['total'], color=colors[:len(top10)])
ax.set_yticks(range(len(top10)))
ax.set_yticklabels(top10.index)
ax.invert_yaxis()
ax.set_xlabel('Total Search Interest (2025 YTD)', fontsize=12, fontweight='bold')
ax.set_title('Top 10 Most Searched People on Google (2025)\nPolymarket Candidates Ranked by Total Search Interest',
             fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)

# Add value labels
for i, (idx, row) in enumerate(top10.iterrows()):
    ax.text(row['total'], i, f"  {row['total']:,.0f}",
            va='center', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('polymarket_top10_total.png', dpi=300, bbox_inches='tight')
print("✓ Saved: polymarket_top10_total.png")
plt.close()

# Figure 2: Time series for Top 5
fig, ax = plt.subplots(figsize=(16, 9))
top5 = summary.head(5).index.tolist()

for i, person in enumerate(top5):
    person_data = all_data[all_data['person'] == person].sort_values('date')
    ax.plot(person_data['date'], person_data['interest'],
            marker='o', linewidth=2.5, markersize=4,
            label=person, color=colors[i], alpha=0.9)

ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Search Interest (0-100)', fontsize=12, fontweight='bold')
ax.set_title('Google Trends Over Time: Top 5 Candidates (2025)\n' +
             'Weekly Search Interest Throughout the Year',
             fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=11, framealpha=0.9)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('polymarket_top5_timeline.png', dpi=300, bbox_inches='tight')
print("✓ Saved: polymarket_top5_timeline.png")
plt.close()

# Figure 3: Market Share Pie Chart (Top 8 + Others)
fig, ax = plt.subplots(figsize=(12, 10))
top8 = summary.head(8)
others_share = summary.iloc[8:]['market_share'].sum() if len(summary) > 8 else 0

sizes = list(top8['market_share'])
labels = list(top8.index)

if others_share > 0:
    sizes.append(others_share)
    labels.append('Others')

wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                    startangle=90, colors=colors[:len(sizes)],
                                    textprops={'fontsize': 11, 'fontweight': 'bold'})

ax.set_title('Market Share by Search Interest (2025)\n' +
             'Distribution of Google Search Volume Across Candidates',
             fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('polymarket_market_share.png', dpi=300, bbox_inches='tight')
print("✓ Saved: polymarket_market_share.png")
plt.close()

# Figure 4: Average vs Peak Interest Scatter
fig, ax = plt.subplots(figsize=(14, 10))

for i, (person, row) in enumerate(summary.iterrows()):
    ax.scatter(row['average'], row['peak'], s=row['total']*2,
              alpha=0.6, color=colors[i % 20], edgecolors='black', linewidth=1.5)

    # Label top 8
    if i < 8:
        ax.annotate(person, (row['average'], row['peak']),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor=colors[i % 20], alpha=0.7))

ax.set_xlabel('Average Weekly Interest', fontsize=12, fontweight='bold')
ax.set_ylabel('Peak Interest', fontsize=12, fontweight='bold')
ax.set_title('Search Interest: Average vs Peak Performance (2025)\n' +
             'Bubble size represents total search volume',
             fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('polymarket_scatter_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: polymarket_scatter_analysis.png")
plt.close()

# Figure 5: Monthly trends heatmap for top 10
fig, ax = plt.subplots(figsize=(14, 10))

all_data['month'] = pd.to_datetime(all_data['date']).dt.to_period('M').astype(str)
top10_names = summary.head(10).index.tolist()
monthly_pivot = all_data[all_data['person'].isin(top10_names)].groupby(['person', 'month'])['interest'].mean().reset_index()
monthly_pivot = monthly_pivot.pivot(index='person', columns='month', values='interest')

# Reorder rows by total interest
monthly_pivot = monthly_pivot.reindex(top10_names)

im = ax.imshow(monthly_pivot.values, aspect='auto', cmap='YlOrRd', interpolation='nearest')

ax.set_xticks(range(len(monthly_pivot.columns)))
ax.set_xticklabels(monthly_pivot.columns, rotation=45, ha='right')
ax.set_yticks(range(len(monthly_pivot.index)))
ax.set_yticklabels(monthly_pivot.index)

ax.set_title('Monthly Search Interest Heatmap: Top 10 Candidates (2025)\n' +
             'Intensity shows average weekly search interest per month',
             fontsize=14, fontweight='bold', pad=20)

# Add colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Search Interest', rotation=270, labelpad=20, fontweight='bold')

# Add values in cells
for i in range(len(monthly_pivot.index)):
    for j in range(len(monthly_pivot.columns)):
        value = monthly_pivot.values[i, j]
        if not np.isnan(value):
            text = ax.text(j, i, f'{value:.0f}',
                          ha="center", va="center", color="black" if value < 50 else "white",
                          fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('polymarket_monthly_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ Saved: polymarket_monthly_heatmap.png")
plt.close()

# Figure 6: Comparison with Polymarket odds
polymarket_odds = {
    "Pope Leo XIV": 48,
    "Bianca Censori": 18,
    "Donald Trump": 9,
    "Kendrick Lamar": 4,
    "Elon Musk": 4,
    "Jimmy Kimmel": 5,
    "Taylor Swift": 1,
}

fig, ax = plt.subplots(figsize=(14, 10))

comparison_data = []
for person in summary.head(10).index:
    trends_pct = summary.loc[person, 'market_share']
    polymarket_pct = polymarket_odds.get(person, 0)
    comparison_data.append({
        'person': person,
        'Google Trends': trends_pct,
        'Polymarket': polymarket_pct
    })

comparison_df = pd.DataFrame(comparison_data)

x = np.arange(len(comparison_df))
width = 0.35

bars1 = ax.bar(x - width/2, comparison_df['Google Trends'], width,
               label='Google Trends Analysis', color='#FF6B6B', alpha=0.8)
bars2 = ax.bar(x + width/2, comparison_df['Polymarket'], width,
               label='Polymarket Odds', color='#4ECDC4', alpha=0.8)

ax.set_xlabel('Candidate', fontsize=12, fontweight='bold')
ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
ax.set_title('Google Trends vs Polymarket Odds (2025)\n' +
             'Comparison of Data-Driven Analysis vs Market Predictions',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(comparison_df['person'], rotation=45, ha='right')
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig('polymarket_odds_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: polymarket_odds_comparison.png")
plt.close()

print("\n" + "=" * 80)
print("All visualizations created successfully!")
print("=" * 80)
