"""
Check which Minnesota counties are missing from the 1990 extraction
"""

# All 87 Minnesota counties
all_counties = [
    'Aitkin', 'Anoka', 'Becker', 'Beltrami', 'Benton', 'Big Stone', 'Blue Earth', 'Brown',
    'Carlton', 'Carver', 'Cass', 'Chippewa', 'Chisago', 'Clay', 'Clearwater', 'Cook',
    'Cottonwood', 'Crow Wing', 'Dakota', 'Dodge', 'Douglas', 'Faribault', 'Fillmore', 'Freeborn',
    'Goodhue', 'Grant', 'Hennepin', 'Houston', 'Hubbard', 'Isanti', 'Itasca', 'Jackson',
    'Kanabec', 'Kandiyohi', 'Kittson', 'Koochiching', 'Lac qui Parle', 'Lake', 'Lake of the Woods', 'Le Sueur',
    'Lincoln', 'Lyon', 'McLeod', 'Mahnomen', 'Marshall', 'Martin', 'Meeker', 'Mille Lacs',
    'Morrison', 'Mower', 'Murray', 'Nicollet', 'Nobles', 'Norman', 'Olmsted', 'Otter Tail',
    'Pennington', 'Pine', 'Pipestone', 'Polk', 'Pope', 'Ramsey', 'Red Lake', 'Redwood',
    'Renville', 'Rice', 'Rock', 'Roseau', 'St. Louis', 'Scott', 'Sherburne', 'Sibley',
    'Stearns', 'Steele', 'Stevens', 'Swift', 'Todd', 'Traverse', 'Wabasha', 'Wadena',
    'Waseca', 'Washington', 'Watonwan', 'Wilkin', 'Winona', 'Wright', 'Yellow Medicine'
]

# Read the extracted CSV
import csv

csv_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\19901106__mn__general__county.csv"

extracted_counties = set()

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        extracted_counties.add(row['county'])

print(f"Total Minnesota counties: {len(all_counties)}")
print(f"Extracted counties: {len(extracted_counties)}")
print(f"Missing: {len(all_counties) - len(extracted_counties)}\n")

missing = sorted([c for c in all_counties if c not in extracted_counties])

if missing:
    print("Missing counties:")
    for county in missing:
        print(f"  - {county}")
else:
    print("✓ All counties extracted!")

# Check the text file to see why they're missing
print("\n" + "="*60)
print("Checking text file for missing counties...")
print("="*60)

text_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\19901106__mn__general__county_text.txt"

with open(text_file, 'r', encoding='utf-8') as f:
    text = f.read()
    
    for county in missing[:5]:  # Check first 5 missing
        # Try different name variations
        variations = [
            county,
            county.replace(' ', ''),
            county.replace('. ', '.'),
        ]
        
        found = False
        for var in variations:
            if var in text:
                print(f"\n{county}: Found as '{var}' in text")
                # Find a sample line
                lines = text.split('\n')
                for line in lines:
                    if line.startswith(var):
                        print(f"  Sample: {line[:100]}")
                        found = True
                        break
                if found:
                    break
        
        if not found:
            print(f"\n{county}: NOT FOUND in text")
