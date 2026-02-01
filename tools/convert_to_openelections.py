"""
Convert Minnesota election data files to OpenElections format
Handles various input formats from 1992-2024
OpenElections format: county_code,county,office,district,party,candidate,votes,pct
"""

import csv
import os
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

# FIPS to County mapping
FIPS_TO_COUNTY = {v: k for k, v in COUNTY_CODES.items()}

def get_county_from_fips(fips):
    """Convert FIPS code to county name"""
    fips_str = str(fips).zfill(3)[-2:]  # Get last 2 digits
    return FIPS_TO_COUNTY.get(fips_str, None)

def normalize_county_name(county):
    """Normalize county name variations"""
    county = county.strip().title()
    
    # Remove "Twp", "Township", "City" suffixes
    for suffix in [' Twp', ' Township', ' City']:
        if county.endswith(suffix):
            county = county[:-len(suffix)].strip()
    
    # Handle specific variations
    replacements = {
        'Saint Louis': 'St. Louis',
        'St Louis': 'St. Louis',
        'Bigstone': 'Big Stone',
        'Blueearth': 'Blue Earth',
        'Crowwing': 'Crow Wing',
        'Lacquiparle': 'Lac Qui Parle',
        'Lakeofthewoods': 'Lake Of The Woods',
        'Lesueur': 'Le Sueur',
        'Millelacs': 'Mille Lacs',
        'Ottertail': 'Otter Tail',
        'Redlake': 'Red Lake',
        'Yellowmedicine': 'Yellow Medicine'
    }
    
    for old, new in replacements.items():
        if county.lower() == old.lower():
            county = new
    
    return county

def aggregate_precinct_to_county(input_file, output_file):
    """Aggregate precinct-level OpenElections format to county level"""
    print(f"\nAggregating precinct data: {os.path.basename(input_file)}")
    
    county_results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            county = row.get('county', '').strip()
            office = row.get('office', '').strip()
            district = row.get('district', '').strip()
            party = row.get('party', '').strip()
            candidate = row.get('candidate', '').strip()
            votes = int(row.get('votes', 0))
            
            key = (office, district, party, candidate)
            county_results[county][key] += votes
    
    # Write aggregated results
    results = []
    for county in sorted(county_results.keys()):
        county_code = COUNTY_CODES.get(county, '')
        for (office, district, party, candidate), votes in sorted(county_results[county].items()):
            results.append([county_code, county, office, district, party, candidate, str(votes), ''])
    
    # Calculate percentages
    office_totals = defaultdict(lambda: defaultdict(int))
    for row in results:
        county_code, county, office, district = row[0], row[1], row[2], row[3]
        votes = int(row[6])
        key = (county_code, office, district)
        office_totals[key] += votes
    
    for row in results:
        county_code, county, office, district = row[0], row[1], row[2], row[3]
        votes = int(row[6])
        key = (county_code, office, district)
        total = office_totals[key]
        pct = (votes / total * 100) if total > 0 else 0
        row[7] = f'{pct:.2f}'
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['county_code', 'county', 'office', 'district', 'party', 'candidate', 'votes', 'pct'])
        writer.writerows(results)
    
    print(f"  ✓ Created: {output_file}")
    print(f"    {len(results)} rows from precinct data")
    return len(results)

def aggregate_to_county(input_file, year, output_file):
    """Aggregate precinct-level data to county level"""
    
    print(f"\nProcessing {year}: {os.path.basename(input_file)}")
    
    county_results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        
        print(f"  Headers: {', '.join(headers[:10])}...")
        
        # Detect format and county column
        county_col = None
        fips_col = None
        
        for col in headers:
            col_stripped = col.strip()  # Handle columns with leading/trailing spaces
            col_lower = col_stripped.lower()
            if 'county' in col_lower and 'id' not in col_lower:
                county_col = col
                break
            elif col_stripped == 'CC':
                fips_col = col
            elif col_stripped == 'FIPS':
                fips_col = col
            elif col_stripped == 'MCD NAME':
                county_col = col
        
        if not county_col and not fips_col:
            print(f"  ⚠ Warning: No county column found. Skipping.")
            return None
        
        # Process each row
        for row in reader:
            # Get county
            if county_col and row.get(county_col):
                county = normalize_county_name(row[county_col])
            elif fips_col and row.get(fips_col):
                county = get_county_from_fips(row[fips_col])
            else:
                continue
            
            # Skip if not a valid county
            if county not in COUNTY_CODES:
                continue
            
            # Define race mapping for statewide offices
            race_mapping = [
                # President
                (['PresRP', 'PresIR', 'PresR'], 'President', 'R'),
                (['PresDFL'], 'President', 'DFL'),
                (['PresOther', 'PresG', 'PresGP'], 'President', 'Other'),
                
                # U.S. Senate
                (['USSenIR', 'USSenR'], 'U.S. Senate', 'R'),
                (['USSenDFL'], 'U.S. Senate', 'DFL'),
                (['USSenOther', 'USSenGP', 'USSenG'], 'U.S. Senate', 'Other'),
                
                # Governor
                (['GovIR', 'GovR'], 'Governor', 'R'),
                (['GovDFL'], 'Governor', 'DFL'),
                (['GovRP', 'GovGP', 'GovOther'], 'Governor', 'Other'),
                
                # Secretary of State
                (['SOSIR', 'SOSR'], 'Secretary of State', 'R'),
                (['SOSDFL'], 'Secretary of State', 'DFL'),
                (['SOSRP', 'SOSGP', 'SOSOther'], 'Secretary of State', 'Other'),
                
                # Attorney General
                (['AGIR', 'AGR'], 'Attorney General', 'R'),
                (['AGDFL'], 'Attorney General', 'DFL'),
                (['AGRP', 'AGGP', 'AGOther'], 'Attorney General', 'Other'),
                
                # State Auditor
                (['AudIR', 'AudR'], 'State Auditor', 'R'),
                (['AudDFL'], 'State Auditor', 'DFL'),
                (['AudRP', 'AudMTP', 'AudGP', 'AudOther'], 'State Auditor', 'Other'),
                
                # State Treasurer (where applicable)
                (['TreasIR', 'TreasR'], 'State Treasurer', 'R'),
                (['TreasDFL'], 'State Treasurer', 'DFL'),
                (['TreasRP', 'TreasGP', 'TreasOther'], 'State Treasurer', 'Other'),
            ]
            
            # Extract votes for each race mapping
            for col_names, office, party in race_mapping:
                for col in col_names:
                    if col in headers:
                        votes_str = row.get(col, '0')
                        try:
                            votes = int(votes_str) if votes_str else 0
                            if votes > 0:
                                county_results[county][office][party] += votes
                        except ValueError:
                            continue
                        break  # Found the column, no need to check other variants
    
    # Write results
    if not county_results:
        print(f"  ⚠ No valid data extracted")
        return None
    
    results = []
    for county in sorted(county_results.keys()):
        county_code = COUNTY_CODES[county]
        for office in sorted(county_results[county].keys()):
            party_votes = county_results[county][office]
            total = sum(party_votes.values())
            
            for party, votes in sorted(party_votes.items()):
                if votes > 0:
                    pct = (votes / total * 100) if total > 0 else 0
                    results.append([
                        county_code,
                        county,
                        office,
                        '',  # district
                        party,
                        '',  # candidate - would need lookup
                        str(votes),
                        f'{pct:.2f}'
                    ])
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['county_code', 'county', 'office', 'district', 'party', 'candidate', 'votes', 'pct'])
        writer.writerows(results)
    
    print(f"  ✓ Created: {output_file}")
    print(f"    {len(results)} rows, {len(county_results)} counties")
    
    return len(results)

if __name__ == "__main__":
    data_dir = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data"
    
    # Files to convert from raw MN format
    conversions = [
        ('1992_Vote_Stats-aligned.csv', '1992', '19921103__mn__general__county.csv'),
        ('1994_Vote_Stats-aligned.csv', '1994', '19941108__mn__general__county.csv'),
        ('1996_Vote_Stats-aligned.csv', '1996', '19961105__mn__general__county.csv'),
        ('1998_Vote_Stats.csv', '1998', '19981103__mn__general__county.csv'),
        ('full_00results-aligned.csv', '2000', '20001107__mn__general__county.csv'),
        ('2002_general_results - Results.csv', '2002', '20021105__mn__general__county.csv'),
        ('2004_general_results.csv', '2004', '20041102__mn__general__county.csv'),
        ('2006_general_results - Results.csv', '2006', '20061107__mn__general__county.csv'),
        ('2008_general_results - Results.csv', '2008', '20081104__mn__general__county.csv'),
        ('2010_general_results_final - Results.csv', '2010', '20101102__mn__general__county.csv'),
    ]
    
    # Precinct files to aggregate to county
    precinct_conversions = [
        ('20201103__mn__general__precinct.csv', '20201103__mn__general__county.csv'),
        ('20221108__mn__general__precinct.csv', '20221108__mn__general__county.csv'),
        ('2024-general-federal-state-results-by-precinct-official - Precinct-Results.csv', '20241105__mn__general__county.csv'),
    ]
    
    print("="*60)
    print("Converting Minnesota Election Data to OpenElections Format")
    print("="*60)
    
    for input_name, year, output_name in conversions:
        input_file = os.path.join(data_dir, input_name)
        output_file = os.path.join(data_dir, output_name)
        
        if os.path.exists(input_file):
            if not os.path.exists(output_file):
                aggregate_to_county(input_file, year, output_file)
            else:
                print(f"\n✓ Already converted: {output_name}")
        else:
            print(f"\n⚠ File not found: {input_name}")
    
    print("\n" + "-"*60)
    print("Aggregating precinct data to county level")
    print("-"*60)
    
    for input_name, output_name in precinct_conversions:
        input_file = os.path.join(data_dir, input_name)
        output_file = os.path.join(data_dir, output_name)
        
        if os.path.exists(input_file):
            if not os.path.exists(output_file):
                aggregate_precinct_to_county(input_file, output_file)
            else:
                print(f"\n✓ Already aggregated: {output_name}")
        else:
            print(f"\n⚠ File not found: {input_name}")
    
    print("\n" + "="*60)
    print("Conversion complete!")
    print("All files now in OpenElections county format")
    print("="*60)
