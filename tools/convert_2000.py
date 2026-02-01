"""
Targeted script to convert 2000 election data from aligned file
"""

import csv
import sys
from collections import defaultdict

# County codes mapping
COUNTY_CODES = {
    'Aitkin': '01', 'Anoka': '02', 'Becker': '03', 'Beltrami': '04',
    'Benton': '05', 'Big Stone': '06', 'Blue Earth': '07', 'Brown': '08',
    'Carlton': '09', 'Carver': '10', 'Cass': '11', 'Chippewa': '12',
    'Chisago': '13', 'Clay': '14', 'Clearwater': '15', 'Cook': '16',
    'Cottonwood': '17', 'Crow Wing': '18', 'Dakota': '19', 'Dodge': '20',
    'Douglas': '21', 'Faribault': '22', 'Fillmore': '23', 'Freeborn': '24',
    'Goodhue': '25', 'Grant': '26', 'Hennepin': '27', 'Houston': '28',
    'Hubbard': '29', 'Isanti': '30', 'Itasca': '31', 'Jackson': '32',
    'Kanabec': '33', 'Kandiyohi': '34', 'Kittson': '35', 'Koochiching': '36',
    'Lac qui Parle': '37', 'Lake': '38', 'Lake of the Woods': '39',
    'Le Sueur': '40', 'Lincoln': '41', 'Lyon': '42', 'McLeod': '43',
    'Mahnomen': '44', 'Marshall': '45', 'Martin': '46', 'Mille Lacs': '47',
    'Morrison': '48', 'Mower': '49', 'Murray': '50', 'Nicollet': '51',
    'Nobles': '52', 'Norman': '53', 'Olmsted': '54', 'Otter Tail': '55',
    'Pennington': '56', 'Pine': '57', 'Pipestone': '58', 'Polk': '59',
    'Pope': '60', 'Meeker': '61', 'Ramsey': '62', 'Red Lake': '63',
    'Redwood': '64', 'Renville': '65', 'Rice': '66', 'Rock': '67',
    'Roseau': '68', 'St. Louis': '69', 'Scott': '70', 'Sherburne': '71',
    'Sibley': '72', 'Stearns': '73', 'Steele': '74', 'Stevens': '75',
    'Swift': '76', 'Todd': '77', 'Traverse': '78', 'Wabasha': '79',
    'Wadena': '80', 'Waseca': '81', 'Washington': '82', 'Watonwan': '83',
    'Wilkin': '84', 'Winona': '85', 'Wright': '86', 'Yellow Medicine': '87'
}

FIPS_TO_COUNTY = {v: k for k, v in COUNTY_CODES.items()}

def convert_2000():
    """Convert 2000 election data from aligned file"""
    input_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\full_00results-aligned.csv"
    output_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\20001107__mn__general__county.csv"
    
    print(f"Processing: {input_file}")
    
    county_results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    # Increase CSV field size limit
    maxInt = sys.maxsize
    while True:
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # Strip leading/trailing spaces from column names
        reader.fieldnames = [name.strip() if name else name for name in reader.fieldnames]
        
        print(f"Columns: {reader.fieldnames[:10]}")  # Debug: show first 10 columns
        
        for row in reader:
            # Use CC or FIPS column
            county_code = row.get('CC', row.get('FIPS', '')).strip()
            if not county_code:
                continue
            
            # Handle 3-digit FIPS codes - take last 2 digits
            if len(county_code) == 3:
                county_code = county_code[1:]
            county_code = county_code.zfill(2)
            
            if county_code not in FIPS_TO_COUNTY:
                continue
            
            county = FIPS_TO_COUNTY[county_code]
            
            # President: R_PREZ, DFL_PREZ, GREEN_PREZ, LIB_PREZ, RP_PREZ, etc.
            for party, col in [('R', 'R_PREZ'), ('DFL', 'DFL_PREZ'), ('GP', 'GREEN_PREZ'), 
                              ('LIB', 'LIB_PREZ'), ('RP', 'RP_PREZ')]:
                try:
                    votes = int(row.get(col, '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['President'][party] += votes
                except (ValueError, KeyError):
                    continue
            
            # U.S. Senate: R_USSEN, DFL_USSEN, IND_USSEN
            for party, col in [('R', 'R_USSEN'), ('DFL', 'DFL_USSEN'), ('IND', 'IND_USSEN')]:
                try:
                    votes = int(row.get(col, '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['U.S. Senate'][party] += votes
                except (ValueError, KeyError):
                    continue
    
    # Write results
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['county_code', 'county', 'office', 'district', 'party', 'candidate', 'votes', 'pct'])
        writer.writeheader()
        
        for county in sorted(county_results.keys()):
            county_code = COUNTY_CODES[county]
            
            for office in sorted(county_results[county].keys()):
                total_votes = sum(county_results[county][office].values())
                
                for party in sorted(county_results[county][office].keys()):
                    votes = county_results[county][office][party]
                    pct = round((votes / total_votes * 100), 2) if total_votes > 0 else 0
                    
                    writer.writerow({
                        'county_code': county_code,
                        'county': county,
                        'office': office,
                        'district': '',
                        'party': party,
                        'candidate': '',
                        'votes': votes,
                        'pct': pct
                    })
    
    total_rows = sum(len(county_results[county][office]) for county in county_results for office in county_results[county])
    print(f"✓ Created: {output_file}")
    print(f"  Counties: {len(county_results)}")
    print(f"  Total rows: {total_rows}")

if __name__ == "__main__":
    convert_2000()
