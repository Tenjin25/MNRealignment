import csv

csv_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\19901106__mn__general__county.csv"

offices = {}
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        office = row['office']
        county = row['county']
        
        if office not in offices:
            offices[office] = {}
        if county not in offices[office]:
            offices[office][county] = []
        offices[office][county].append(row['candidate'])

print("County counts per office:")
for office in sorted(offices.keys()):
    print(f"{office}: {len(offices[office])} counties")

print("\nChecking for duplicate counties in Secretary of State:")
sec_state = offices.get('Secretary of State', {})
for county, candidates in sorted(sec_state.items()):
    if len(candidates) > 3:
        print(f"  {county}: {len(candidates)} entries - {candidates}")

print("\nChecking for duplicate counties in State Treasurer:")
treasurer = offices.get('State Treasurer', {})
for county, candidates in sorted(treasurer.items()):
    if len(candidates) > 3:
        print(f"  {county}: {len(candidates)} entries - {candidates}")
