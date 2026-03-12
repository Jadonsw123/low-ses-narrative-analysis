"""
Complete Analysis & Visualization of All 387 Narratives
Merges checkpoint_51.json + gpt4_raw_results.json
Generates publication-quality diagrams
"""
import json
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configure style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 14
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

print("\n" + "="*80)
print("LOADING DATA FROM CHECKPOINT & RESULTS")
print("="*80 + "\n")

# Load checkpoint_51 (narratives 0-51)
with open('results/gpt4_checkpoint_51.json', 'r') as f:
    checkpoint = json.load(f)
checkpoint_results = checkpoint['results']
print(f"✓ Loaded checkpoint_51: {len(checkpoint_results)} narratives (indices 0-51)")

# Load gpt4_raw_results (narratives 52+)
with open('results/gpt4_raw_results.json', 'r') as f:
    raw_data = json.load(f)
raw_results = raw_data['results']
print(f"✓ Loaded gpt4_raw_results: {len(raw_results)} narratives (indices 52+)")

# Merge all results
all_results = checkpoint_results + raw_results
print(f"✓ TOTAL MERGED: {len(all_results)} narratives\n")

# Verify indices and check for duplicates
indices = [r['narrative_idx'] for r in all_results]
unique_indices = set(indices)
print(f"Index range: {min(indices)} to {max(indices)}")
print(f"Total narratives: {len(all_results)}")
print(f"Unique indices: {len(unique_indices)}")
if len(unique_indices) != len(all_results):
    print(f"⚠️  WARNING: {len(all_results) - len(unique_indices)} duplicate(s) found!")
    # Find duplicates
    from collections import Counter
    idx_counts = Counter(indices)
    duplicates = [idx for idx, count in idx_counts.items() if count > 1]
    print(f"   Duplicate indices: {duplicates}")
print(f"Expected range: 0-{len(unique_indices)-1}")
print()

# ===== ANALYSIS STATISTICS =====
print("="*80)
print("ANALYSIS OF ALL {} NARRATIVES".format(len(all_results)))
print("="*80 + "\n")

# Critical Pedagogy
agencies = [r['critical_pedagogy']['student_agency'] for r in all_results]
print("CRITICAL PEDAGOGY - Student Agency Distribution:")
for agency, count in Counter(agencies).most_common():
    pct = (count / len(all_results)) * 100
    print(f"  {agency.capitalize()}: {count} ({pct:.1f}%)")

barriers_count = sum(1 for r in all_results if r['critical_pedagogy']['structural_barriers_evident'])
print(f"\n  Narratives with structural barriers: {barriers_count}/{len(all_results)} ({(barriers_count/len(all_results))*100:.1f}%)")

consciousness_vals = [r['critical_pedagogy']['consciousness_of_barriers'] for r in all_results]
print("\nConsciousness of Barriers:")
for cons, count in Counter(consciousness_vals).most_common():
    pct = (count / len(all_results)) * 100
    print(f"  {cons.capitalize()}: {count} ({pct:.1f}%)")

# Ecological Systems
dominant_levels = [r['ecological_systems']['dominant_level'] for r in all_results]
print(f"\n{'='*80}")
print("ECOLOGICAL SYSTEMS - Dominant Levels:")
for level, count in Counter(dominant_levels).most_common():
    pct = (count / len(all_results)) * 100
    print(f"  {level.capitalize()}: {count} ({pct:.1f}%)")

# Bourdieu's Capital
print(f"\n{'='*80}")
print("BOURDIEU'S CAPITAL - Distributions:\n")

for capital in ['economic', 'social', 'cultural', 'symbolic']:
    values = [r['bourdieu_capital'][capital] for r in all_results]
    print(f"{capital.capitalize()}:")
    for val, count in Counter(values).most_common():
        pct = (count / len(all_results)) * 100
        val_label = val.capitalize() if val else 'None'
        print(f"  {val_label}: {count} ({pct:.1f}%)")
    print()

# Capital combinations
capital_profiles = []
for r in all_results:
    caps = r['bourdieu_capital']
    assets = sum(1 for cap in ['economic', 'social', 'cultural', 'symbolic'] if caps[cap] == 'asset')
    deficits = sum(1 for cap in ['economic', 'social', 'cultural', 'symbolic'] if caps[cap] == 'deficit')
    absents = sum(1 for cap in ['economic', 'social', 'cultural', 'symbolic'] if caps[cap] == 'absent')
    capital_profiles.append({'assets': assets, 'deficits': deficits, 'absents': absents})

profiles_df = pd.DataFrame(capital_profiles)
print(f"{'='*80}")
print("CAPITAL PROFILE PATTERNS:\n")
print("Asset Distribution (# of asset capitals per narrative):")
for assets, count in Counter(profiles_df['assets']).most_common():
    pct = (count / len(all_results)) * 100
    print(f"  {assets} assets: {count} narratives ({pct:.1f}%)")

print("\n" + "="*80 + "\n")

# ===== VISUALIZATION 1: AGENCY × CONSCIOUSNESS SCATTER =====
print("Creating Visualization 1: Agency × Consciousness Scatter...")
fig, ax = plt.subplots(figsize=(12, 8))

agency_order = {'high': 3, 'moderate': 2, 'low': 1}
consciousness_order = {'high': 3, 'moderate': 2, 'low': 1}

x_data = [consciousness_order.get(r['critical_pedagogy']['consciousness_of_barriers'], 0) for r in all_results]
y_data = [agency_order.get(r['critical_pedagogy']['student_agency'], 0) for r in all_results]

# Add jitter
x_jitter = np.array(x_data) + np.random.normal(0, 0.05, len(x_data))
y_jitter = np.array(y_data) + np.random.normal(0, 0.05, len(y_data))

scatter = ax.scatter(x_jitter, y_jitter, alpha=0.6, s=100, c=y_data, cmap='RdYlGn', edgecolors='black', linewidth=0.5)
ax.set_xlabel('Consciousness of Barriers', fontsize=14, fontweight='bold')
ax.set_ylabel('Student Agency', fontsize=14, fontweight='bold')
ax.set_title('The Awareness-Action Gap: Consciousness vs. Agency in Low-SES Narratives\n(n=387)', fontsize=16, fontweight='bold')
ax.set_xticks([1, 2, 3])
ax.set_xticklabels(['Low', 'Moderate', 'High'])
ax.set_yticks([1, 2, 3])
ax.set_yticklabels(['Low', 'Moderate', 'High'])
ax.grid(True, alpha=0.3)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Agency Level', fontsize=12)
plt.tight_layout()
plt.savefig('results/01_agency_consciousness_scatter.png')
print("✓ Saved: 01_agency_consciousness_scatter.png")
plt.close()

# ===== VISUALIZATION 2: BOURDIEU CAPITAL HEATMAP =====
print("Creating Visualization 2: Bourdieu Capital Heatmap...")
fig, ax = plt.subplots(figsize=(10, 6))

capital_types = ['Economic', 'Social', 'Cultural', 'Symbolic']
status_types = ['Deficit', 'Asset', 'Absent']

# Create matrix
capital_matrix = []
for capital in ['economic', 'social', 'cultural', 'symbolic']:
    row = []
    values = [r['bourdieu_capital'][capital] for r in all_results]
    for status in ['deficit', 'asset', 'absent']:
        count = sum(1 for v in values if v == status)
        pct = (count / len(all_results)) * 100
        row.append(pct)
    capital_matrix.append(row)

capital_matrix = np.array(capital_matrix)
sns.heatmap(capital_matrix, annot=True, fmt='.1f', cmap='RdYlGn', 
            xticklabels=status_types, yticklabels=capital_types,
            cbar_kws={'label': 'Percentage of Students (%)'}, ax=ax, annot_kws={'fontsize': 12})
ax.set_title('Bourdieu\'s Capital Distribution Across Low-SES Students\n(n=387)', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('results/02_bourdieu_capital_heatmap.png')
print("✓ Saved: 02_bourdieu_capital_heatmap.png")
plt.close()

# ===== VISUALIZATION 3: ECOLOGICAL SYSTEMS BAR CHART =====
print("Creating Visualization 3: Ecological Systems Bar Chart...")
fig, ax = plt.subplots(figsize=(12, 6))

levels = ['Microsystem', 'Exosystem', 'Macrosystem', 'Chronosystem', 'Mesosystem']
dominant_counts = Counter(dominant_levels)
counts = [dominant_counts.get(level.lower(), 0) for level in levels]
colors = ['#2ecc71', '#e74c3c', '#f39c12', '#3498db', '#9b59b6']

bars = ax.bar(levels, counts, color=colors, edgecolor='black', linewidth=1.5)
ax.set_ylabel('Number of Students', fontsize=14, fontweight='bold')
ax.set_title('Dominant Ecological System Levels in Low-SES Student Narratives\n(n=387)', fontsize=16, fontweight='bold')
ax.set_ylim(0, max(counts) * 1.1)

# Add count labels on bars
for bar, count in zip(bars, counts):
    height = bar.get_height()
    pct = (count / len(all_results)) * 100
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(count)}\n({pct:.1f}%)',
            ha='center', va='bottom', fontweight='bold', fontsize=12)

plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('results/03_ecological_systems_bar.png')
print("✓ Saved: 03_ecological_systems_bar.png")
plt.close()

# ===== VISUALIZATION 4: CAPITAL PROFILE DISTRIBUTION =====
print("Creating Visualization 4: Capital Profile Distribution...")
fig, axes = plt.subplots(1, 3, figsize=(16, 7))

# Assets distribution
ax = axes[0]
asset_counts = Counter(profiles_df['assets'])
assets_sorted = sorted(asset_counts.keys())
assets_vals = [asset_counts[k] for k in assets_sorted]
colors_assets = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#27ae60']
ax.bar([str(i) for i in assets_sorted], assets_vals, color=colors_assets[:len(assets_sorted)], edgecolor='black', linewidth=1.5)
ax.set_xlabel('Number of Asset Capitals', fontsize=13, fontweight='bold')
ax.set_ylabel('Count', fontsize=13, fontweight='bold')
ax.set_title('Asset Capital Distribution', fontsize=14, fontweight='bold')
for i, (k, v) in enumerate(zip(assets_sorted, assets_vals)):
    pct = (v / len(all_results)) * 100
    ax.text(i, v, f'{v}\n({pct:.1f}%)', ha='center', va='bottom', fontweight='bold', fontsize=11)

# Deficits distribution
ax = axes[1]
deficit_counts = Counter(profiles_df['deficits'])
deficits_sorted = sorted(deficit_counts.keys())
deficits_vals = [deficit_counts[k] for k in deficits_sorted]
ax.bar([str(i) for i in deficits_sorted], deficits_vals, color='#e74c3c', edgecolor='black', linewidth=1.5)
ax.set_xlabel('Number of Deficit Capitals', fontsize=13, fontweight='bold')
ax.set_ylabel('Count', fontsize=13, fontweight='bold')
ax.set_title('Deficit Capital Distribution', fontsize=14, fontweight='bold')
for i, (k, v) in enumerate(zip(deficits_sorted, deficits_vals)):
    pct = (v / len(all_results)) * 100
    ax.text(i, v, f'{v}\n({pct:.1f}%)', ha='center', va='bottom', fontweight='bold', fontsize=11)

# Absent distribution
ax = axes[2]
absent_counts = Counter(profiles_df['absents'])
absents_sorted = sorted(absent_counts.keys())
absents_vals = [absent_counts[k] for k in absents_sorted]
ax.bar([str(i) for i in absents_sorted], absents_vals, color='#95a5a6', edgecolor='black', linewidth=1.5)
ax.set_xlabel('Number of Absent Capitals', fontsize=13, fontweight='bold')
ax.set_ylabel('Count', fontsize=13, fontweight='bold')
ax.set_title('Absent Capital Distribution', fontsize=14, fontweight='bold')
for i, (k, v) in enumerate(zip(absents_sorted, absents_vals)):
    pct = (v / len(all_results)) * 100
    ax.text(i, v, f'{v}\n({pct:.1f}%)', ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.suptitle('Capital Profiles: Assets, Deficits, and Absences (n=387)', fontsize=16, fontweight='bold')
plt.subplots_adjust(top=0.88, hspace=0.4)
plt.savefig('results/04_capital_profile_distribution.png')
print("✓ Saved: 04_capital_profile_distribution.png")
plt.close()

# ===== VISUALIZATION 5: AGENCY DISTRIBUTION =====
print("Creating Visualization 5: Agency Distribution...")
fig, ax = plt.subplots(figsize=(10, 6))

agency_counts = Counter(agencies)
agency_order_list = ['high', 'moderate', 'low']
colors_agency = ['#2ecc71', '#f39c12', '#e74c3c']
counts_ordered = [agency_counts.get(a, 0) for a in agency_order_list]
labels_ordered = [a.capitalize() for a in agency_order_list]

bars = ax.bar(labels_ordered, counts_ordered, color=colors_agency, edgecolor='black', linewidth=1.5, width=0.6)
ax.set_ylabel('Number of Students', fontsize=14, fontweight='bold')
ax.set_title('Student Agency in Low-SES Narratives\n(Critical Pedagogy Framework, n=387)', fontsize=16, fontweight='bold')
ax.set_ylim(0, max(counts_ordered) * 1.15)

for bar, count in zip(bars, counts_ordered):
    height = bar.get_height()
    pct = (count / len(all_results)) * 100
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(count)}\n({pct:.1f}%)',
            ha='center', va='bottom', fontweight='bold', fontsize=13)

plt.tight_layout()
plt.savefig('results/05_agency_distribution.png')
print("✓ Saved: 05_agency_distribution.png")
plt.close()

# ===== VISUALIZATION 6: CONSCIOUSNESS DISTRIBUTION =====
print("Creating Visualization 6: Consciousness Distribution...")
fig, ax = plt.subplots(figsize=(10, 6))

consciousness_counts = Counter(consciousness_vals)
consciousness_order_list = ['high', 'moderate', 'low']
colors_cons = ['#2ecc71', '#f39c12', '#e74c3c']
counts_cons = [consciousness_counts.get(c, 0) for c in consciousness_order_list]
labels_cons = [c.capitalize() for c in consciousness_order_list]

bars = ax.bar(labels_cons, counts_cons, color=colors_cons, edgecolor='black', linewidth=1.5, width=0.6)
ax.set_ylabel('Number of Students', fontsize=14, fontweight='bold')
ax.set_title('Consciousness of Barriers in Low-SES Students\n(Critical Pedagogy Framework, n=387)', fontsize=16, fontweight='bold')
ax.set_ylim(0, max(counts_cons) * 1.15)

for bar, count in zip(bars, counts_cons):
    height = bar.get_height()
    pct = (count / len(all_results)) * 100
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(count)}\n({pct:.1f}%)',
            ha='center', va='bottom', fontweight='bold', fontsize=13)

plt.tight_layout()
plt.savefig('results/06_consciousness_distribution.png')
print("✓ Saved: 06_consciousness_distribution.png")
plt.close()

print("\n" + "="*80)
print("ALL VISUALIZATIONS COMPLETE!")
print("="*80)
print("\nGenerated files:")
print("  ✓ 01_agency_consciousness_scatter.png")
print("  ✓ 02_bourdieu_capital_heatmap.png")
print("  ✓ 03_ecological_systems_bar.png")
print("  ✓ 04_capital_profile_distribution.png")
print("  ✓ 05_agency_distribution.png")
print("  ✓ 06_consciousness_distribution.png")
print("\nAll files saved to: results/")
print("="*80 + "\n")
