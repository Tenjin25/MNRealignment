import csv
from collections import Counter

rows=list(csv.DictReader(open(r'C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\19901106__mn__general__county.csv')))

counties=[r['county'] for r in rows]
county_counts=Counter(counties)

# Find any duplicates
duplicates = [c for c, count in county_counts.items() if c in county_counts and list(county_counts.values()).count(count) > 1]

# Better approach - check each county has exactly 5 entries (3 Senate + 2 Governor)
print("Counties with incorrect entry counts:\n")
for county, count in sorted(county_counts.items()):
    if count != 5:
        senate_count = len([r for r in rows if r['county']==county and r['office']=='U.S. Senate'])
        gov_count = len([r for r in rows if r['county']==county and r['office']=='Governor'])
        print(f"{county}: {count} total ({senate_count} Senate, {gov_count} Governor)")

unique = len(set(counties))
print(f"\nUnique counties: {unique}/87")
print(f"Total rows: {len(rows)} (should be 435 for 87 counties * 5 entries)")
