import csv

f=open(r'C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\19901106__mn__general__county.csv')
rows=[r for r in csv.DictReader(f)]

# Check for Lake of the Woods
lake_woods=[r for r in rows if 'Lake of the Woods' in r['county']]
print(f'Lake of the Woods entries: {len(lake_woods)}')
for r in lake_woods:
    print(f"  {r['office']}: {r['candidate']} - {r['votes']}")

# Check for Mahnomen  
mahnomen=[r for r in rows if 'Mahnomen' in r['county']]
print(f'\nMahnomen entries: {len(mahnomen)}')
for r in mahnomen:
    print(f"  {r['office']}: {r['candidate']} - {r['votes']}")

# List all unique counties
counties = sorted(set([r['county'] for r in rows]))
print(f'\nTotal unique counties: {len(counties)}')
print('Missing from 87:', 87 - len(counties))
