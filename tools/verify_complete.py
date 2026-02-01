import csv

csv_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\19901106__mn__general__county.csv"

offices = {}
total_rows = 0

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_rows += 1
        office = row['office']
        if office not in offices:
            offices[office] = {'counties': set(), 'entries': 0}
        offices[office]['counties'].add(row['county'])
        offices[office]['entries'] += 1

print("="*60)
print("1990 Minnesota Election Data Summary")
print("="*60)
print(f"\nTotal rows: {total_rows}")
print(f"\nOffices extracted:")
for office in sorted(offices.keys()):
    counties = len(offices[office]['counties'])
    entries = offices[office]['entries']
    candidates = entries // counties
    print(f"  {office}:")
    print(f"    - {counties} counties")
    print(f"    - {candidates} candidates per county")
    print(f"    - {entries} total entries")

# Expected total calculation
print(f"\n Expected: 87 counties × (3 + 2 + 3 + 2 + 3 + 2) = 87 × 15 = 1,305 rows")
print(f"   Actual: {total_rows} rows")
print(f"   Status: {'✓ MATCH' if total_rows == 1305 else '✗ MISMATCH'}")

# Check a sample county
print(f"\nSample county (Hennepin):")
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    hennepin = [row for row in reader if row['county'] == 'Hennepin']
    for office in sorted(set(r['office'] for r in hennepin)):
        office_rows = [r for r in hennepin if r['office'] == office]
        print(f"  {office}: {len(office_rows)} entries")
        for r in office_rows:
            print(f"    - {r['party']:3s} {r['candidate']:30s} {r['votes']:>7s} votes ({r['pct']:>6s}%)")
