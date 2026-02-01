"""
Handle the outlier election files that need special parsing
- 2000: full_00results.csv (different column format)
- 2002: 2002_general_results - Results.csv (complex multi-header format)
- 2006: 2006_general_results - Results.csv (MCDName column)
- 2020-2024: Precinct files needing county aggregation
"""

import csv
import os
from collections import defaultdict
from candidate_lookup import get_candidate_name

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

def normalize_county(name):
    """Normalize county name variations"""
    name = name.strip().title()
    for suffix in [' Twp', ' Township', ' City', ' Unorganized']:
        if name.endswith(suffix):
            name = name[:-len(suffix)].strip()
    
    replacements = {
        'Saint Louis': 'St. Louis', 'St Louis': 'St. Louis',
        'Bigstone': 'Big Stone', 'Blueearth': 'Blue Earth',
        'Crowwing': 'Crow Wing', 'Lacquiparle': 'Lac Qui Parle',
        'Lac Qui Parle': 'Lac qui Parle',  # Fix capitalization
        'Lakeofthewoods': 'Lake Of The Woods', 'Lake Of The Woods': 'Lake of the Woods',  # Fix capitalization
        'Lesueur': 'Le Sueur',
        'Millelacs': 'Mille Lacs', 'Ottertail': 'Otter Tail',
        'Redlake': 'Red Lake', 'Yellowmedicine': 'Yellow Medicine',
        'Mcleod': 'McLeod'  # Fix capitalization
    }
    
    for old, new in replacements.items():
        if name.lower() == old.lower():
            return new
    return name

def convert_aligned_precinct_file(input_file, year, output_file):
    """Convert aligned precinct files (1992, 1994, 1996) to county level"""
    print(f"\nProcessing {year}: {os.path.basename(input_file)}")
    
    county_results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    # Increase CSV field size limit
    import csv, sys
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
        
        for row in reader:
            # Use CC or FIPS column
            county_code = row.get('CC', row.get('FIPS', '')).strip()
            if not county_code:
                continue
            
            # Handle 3-digit FIPS codes (Minnesota uses odd numbers: 001, 003, 005...)
            # Convert to sequential county code: FIPS = (CountyCode × 2) - 1
            if len(county_code) == 3:
                county_code = str((int(county_code) + 1) // 2).zfill(2)
            else:
                county_code = county_code.zfill(2)
            
            if county_code not in FIPS_TO_COUNTY:
                continue
            
            county = FIPS_TO_COUNTY[county_code]
            
            # Different years have different column names
            if year == 1992:
                # President: PresIR, PresDFL, PresOther
                for party, col in [('R', 'PresIR'), ('DFL', 'PresDFL'), ('Other', 'PresOther')]:
                    try:
                        votes = int(row.get(col, '0').strip() or '0')
                        if votes > 0:
                            county_results[county]['President'][party] += votes
                    except (ValueError, KeyError):
                        continue
            
            elif year == 1994:
                # Governor: GovIR, GovDFL, GovOther
                for party, col in [('R', 'GovIR'), ('DFL', 'GovDFL'), ('Other', 'GovOther')]:
                    try:
                        votes = int(row.get(col, '0').strip() or '0')
                        if votes > 0:
                            county_results[county]['Governor'][party] += votes
                    except (ValueError, KeyError):
                        continue
                
                # U.S. Senate: USSenIR, USSenDFL, USSenOther
                for party, col in [('R', 'USSenIR'), ('DFL', 'USSenDFL'), ('Other', 'USSenOther')]:
                    try:
                        votes = int(row.get(col, '0').strip() or '0')
                        if votes > 0:
                            county_results[county]['U.S. Senate'][party] += votes
                    except (ValueError, KeyError):
                        continue
                
                # All statewide offices
                for office, prefix in [
                    ('Secretary of State', 'SOS'),
                    ('Attorney General', 'AG'),
                    ('State Auditor', 'Aud'),
                    ('State Treasurer', 'Treas')
                ]:
                    for party, suffix in [('R', 'IR'), ('DFL', 'DFL'), ('Other', 'Other')]:
                        col = f'{prefix}{suffix}'
                        try:
                            votes = int(row.get(col, '0').strip() or '0')
                            if votes > 0:
                                county_results[county][office][party] += votes
                        except (ValueError, KeyError):
                            continue
            
            elif year == 1996:
                # President: PresRP, PresIR, PresDFL, PresOther
                for party, col in [('RP', 'PresRP'), ('R', 'PresIR'), ('DFL', 'PresDFL'), ('Other', 'PresOther')]:
                    try:
                        votes = int(row.get(col, '0').strip() or '0')
                        if votes > 0:
                            county_results[county]['President'][party] += votes
                    except (ValueError, KeyError):
                        continue
                
                # U.S. Senate: USSenIR, USSenDFL, USSenOther
                for party, col in [('R', 'USSenIR'), ('DFL', 'USSenDFL'), ('Other', 'USSenOther')]:
                    try:
                        votes = int(row.get(col, '0').strip() or '0')
                        if votes > 0:
                            county_results[county]['U.S. Senate'][party] += votes
                    except (ValueError, KeyError):
                        continue
            
            elif year == 1998:
                # Governor: GovIR, GovDFL, GovRP, GovOther
                for party, col in [('R', 'GovIR'), ('DFL', 'GovDFL'), ('RP', 'GovRP'), ('Other', 'GovOther')]:
                    try:
                        votes = int(row.get(col, '0').strip() or '0')
                        if votes > 0:
                            county_results[county]['Governor'][party] += votes
                    except (ValueError, KeyError):
                        continue
                
                # All statewide offices
                for office, prefix in [
                    ('Secretary of State', 'SOS'),
                    ('Attorney General', 'AG'),
                    ('State Auditor', 'Aud'),
                    ('State Treasurer', 'Treas')
                ]:
                    for party, suffix in [('R', 'IR'), ('DFL', 'DFL'), ('RP', 'RP'), ('MTP', 'MTP'), ('Other', 'Other')]:
                        col = f'{prefix}{suffix}'
                        try:
                            votes = int(row.get(col, '0').strip() or '0')
                            if votes > 0:
                                county_results[county][office][party] += votes
                        except (ValueError, KeyError):
                            continue
    
    write_results(county_results, year, output_file)
    print(f"  ✓ Created: {output_file}")

def convert_2000(input_file, output_file):
    """Convert 2000 election data from aligned precinct file"""
    print(f"\nProcessing 2000: {os.path.basename(input_file)}")
    
    county_results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # Strip column names to remove leading/trailing spaces
        reader.fieldnames = [name.strip() if name else name for name in reader.fieldnames]
        
        for row in reader:
            # Use CC (county code) column from aligned file
            county_code = row.get('CC', '').strip()
            if not county_code or county_code not in FIPS_TO_COUNTY:
                # Try zero-padding if needed
                if county_code:
                    county_code = county_code.zfill(2)
                if not county_code or county_code not in FIPS_TO_COUNTY:
                    continue
            
            county = FIPS_TO_COUNTY[county_code]
            
            # President
            for party, col in [('R', 'R_PREZ'), ('DFL', 'DFL_PREZ'), ('GP', 'GREEN_PREZ'), 
                              ('LIB', 'LIB_PREZ'), ('RP', 'RP_PREZ')]:
                try:
                    votes = int(row.get(col, '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['President'][party] += votes
                except ValueError:
                    continue
            
            # U.S. Senate
            for party, col in [('R', 'R_USSEN'), ('DFL', 'DFL_USSEN'), ('IND', 'IND_USSEN')]:
                try:
                    votes = int(row.get(col, '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['U.S. Senate'][party] += votes
                except ValueError:
                    continue
    
    write_results(county_results, 2000, output_file)
    print(f"  ✓ Created: {output_file}")

def convert_2002_aligned(input_file, output_file):
    """Convert 2002 aligned precinct file to county level"""
    print(f"\nProcessing 2002 aligned: {os.path.basename(input_file)}")
    
    county_results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    with open(input_file, 'r', encoding='utf-8') as f:
        # Skip first 2 rows, row 3 has headers
        next(f)
        next(f)
        reader = csv.DictReader(f)
        # Strip column names
        reader.fieldnames = [name.strip() if name else name for name in reader.fieldnames]
        
        for row in reader:
            county_code = (row.get('CC') or '').strip()
            if not county_code:
                continue
            
            county_code = county_code.zfill(2)
            if county_code not in FIPS_TO_COUNTY:
                continue
            
            county = FIPS_TO_COUNTY[county_code]
            
            # U.S. Senate
            for party, col in [('GP', 'USSenGP'), ('IND', 'USSenIP'), ('R', 'USSenR'), 
                              ('DFL', 'USSenDFL'), ('CP', 'USSenCP')]:
                try:
                    votes = int((row.get(col) or '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['U.S. Senate'][party] += votes
                except (ValueError, KeyError):
                    continue
            
            # Governor
            for party, col in [('GP', 'GovGP'), ('IND', 'GovIP'), ('R', 'GovR'), 
                              ('DFL', 'GovDFL'), ('CP', 'GovCP'), ('I', 'GovI')]:
                try:
                    votes = int((row.get(col) or '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['Governor'][party] += votes
                except (ValueError, KeyError):
                    continue
            
            # Secretary of State
            for party, col in [('GP', 'SOSGP'), ('IND', 'SOSIP'), ('R', 'SOSR'), ('DFL', 'SOSDFL')]:
                try:
                    votes = int((row.get(col) or '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['Secretary of State'][party] += votes
                except (ValueError, KeyError):
                    continue
            
            # Attorney General
            for party, col in [('IND', 'AGIP'), ('R', 'AGR'), ('DFL', 'AGDFL')]:
                try:
                    votes = int((row.get(col) or '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['Attorney General'][party] += votes
                except (ValueError, KeyError):
                    continue
            
            # State Auditor
            for party, col in [('GP', 'AudGP'), ('IND', 'AudIP'), ('R', 'AudR'), ('DFL', 'AudDFL')]:
                try:
                    votes = int((row.get(col) or '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['State Auditor'][party] += votes
                except (ValueError, KeyError):
                    continue
    
    write_results(county_results, 2002, output_file)
    print(f"  ✓ Created: {output_file}")

def convert_2002(input_file, output_file):
    """Convert 2002 election data using Fields.csv for column mapping"""
    print(f"\nProcessing 2002: {os.path.basename(input_file)}")
    
    county_results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    # Read using the actual data row (row 3) as headers
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # Row 3 (index 2) has the actual field names
        headers = [h.strip() for h in lines[2].split(',')]
        
        for line in lines[3:]:
            parts = [p.strip() for p in line.split(',')]
            if len(parts) < len(headers):
                parts.extend([''] * (len(headers) - len(parts)))
            
            row = dict(zip(headers, parts))
            mcd_name = row.get('MCD NAME', '').strip()
            county = normalize_county(mcd_name)
            
            if county not in COUNTY_CODES:
                continue
            
            # According to Fields.csv:
            # USSenGP, USSenIP, USSenR, Wellstone (DFL), USSenDFL, USSenCP, USSenWI
            # GovGP, GovIP, GovR, GovDFL, GovCP, GovI, GovSW, GovWI
            
            # U.S. Senate
            for party, col in [('GP', 'USSenGP'), ('IND', 'USSenIP'), ('R', 'USSenR'), 
                              ('DFL', 'USSenDFL'), ('CP', 'USSenCP')]:
                try:
                    votes = int(row.get(col, '0') or '0')
                    if votes > 0:
                        county_results[county]['U.S. Senate'][party] += votes
                except ValueError:
                    continue
            
            # Governor
            for party, col in [('GP', 'GovGP'), ('IND', 'GovIP'), ('R', 'GovR'), 
                              ('DFL', 'GovDFL'), ('CP', 'GovCP'), ('I', 'GovI')]:
                try:
                    votes = int(row.get(col, '0') or '0')
                    if votes > 0:
                        county_results[county]['Governor'][party] += votes
                except ValueError:
                    continue
            
            # Secretary of State
            for party, col in [('GP', 'SOSGP'), ('IND', 'SOSIP'), ('R', 'SOSR'), ('DFL', 'SOSDFL')]:
                try:
                    votes = int(row.get(col, '0') or '0')
                    if votes > 0:
                        county_results[county]['Secretary of State'][party] += votes
                except ValueError:
                    continue
            
            # Attorney General
            for party, col in [('IND', 'AGIP'), ('R', 'AGR'), ('DFL', 'AGDFL')]:
                try:
                    votes = int(row.get(col, '0') or '0')
                    if votes > 0:
                        county_results[county]['Attorney General'][party] += votes
                except ValueError:
                    continue
            
            # State Auditor
            for party, col in [('GP', 'AudGP'), ('IND', 'AudIP'), ('R', 'AudR'), ('DFL', 'AudDFL')]:
                try:
                    votes = int(row.get(col, '0') or '0')
                    if votes > 0:
                        county_results[county]['State Auditor'][party] += votes
                except ValueError:
                    continue
    
    write_results(county_results, 2002, output_file)
    print(f"  ✓ Created: {output_file}")

def convert_2004(input_file, output_file):
    """Convert 2004 election data from precinct-level Results.csv format"""
    print(f"\nProcessing 2004: {os.path.basename(input_file)}")
    
    county_results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Use CC (County Code) column - it's already in the right format (01, 02, etc.)
            county_code = row.get('CC', '').strip().zfill(2)
            if not county_code or county_code not in FIPS_TO_COUNTY:
                continue
            
            county = FIPS_TO_COUNTY[county_code]
            
            # President: USPresGP, USPresR, USPresDFL, USPresSE, USPresSW, USPresCF, USPresBL, USPresC, USPresL
            for party, col in [('R', 'USPresR'), ('DFL', 'USPresDFL'), ('GP', 'USPresGP'), 
                              ('SE', 'USPresSE'), ('SWP', 'USPresSW'), ('CF', 'USPresCF'), 
                              ('BL', 'USPresBL'), ('C', 'USPresC'), ('LIB', 'USPresL')]:
                try:
                    votes = int(row.get(col, '0') or '0')
                    if votes > 0:
                        county_results[county]['President'][party] += votes
                except (ValueError, TypeError):
                    continue
    
    write_results(county_results, 2004, output_file)
    print(f"  ✓ Created: {output_file}")

def convert_2008(input_file, output_file):
    """Convert 2008 election data from Results.csv format"""
    print(f"\nProcessing 2008: {os.path.basename(input_file)}")
    
    county_results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Get county ID and map to county name (needs zero-padding: "1" -> "01")
            county_id = row.get('CountyID', '').strip().zfill(2)
            if not county_id or county_id not in FIPS_TO_COUNTY:
                continue
            
            county = FIPS_TO_COUNTY[county_id]
            
            # President: USPRESR, USPRESDFL, USPRESGP, USPRESIND, etc.
            for party, col in [('R', 'USPRESR'), ('DFL', 'USPRESDFL'), ('GP', 'USPRESGP'), 
                              ('IND', 'USPRESIND'), ('SWP', 'USPRESSWP'), ('LIB', 'USPRESLIB'), 
                              ('CP', 'USPRESCP')]:
                try:
                    votes = int(row.get(col, '0') or '0')
                    if votes > 0:
                        county_results[county]['President'][party] += votes
                except (ValueError, TypeError):
                    continue
            
            # U.S. Senate: USSENR, USSENDFL, USSENIP (Dean Barkley), USSENLIB, USSENCP
            for party, col in [('R', 'USSENR'), ('DFL', 'USSENDFL'), ('IND', 'USSENIP'), 
                              ('LIB', 'USSENLIB'), ('CP', 'USSENCP')]:
                try:
                    votes = int(row.get(col, '0') or '0')
                    if votes > 0:
                        county_results[county]['U.S. Senate'][party] += votes
                except (ValueError, TypeError):
                    continue
    
    write_results(county_results, 2008, output_file)
    print(f"  ✓ Created: {output_file}")

def convert_2006(input_file, output_file):
    """Convert 2006 election data using Fields.csv for column mapping"""
    print(f"\nProcessing 2006: {os.path.basename(input_file)}")
    
    county_results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            mcd_name = row.get('MCDName', '').strip()
            county = normalize_county(mcd_name)
            
            if county not in COUNTY_CODES:
                continue
            
            # According to Fields.csv:
            # U.S. Senate: USSenR, USSenDFL, USSenIP, USSenWI
            for party, col in [('R', 'USSenR'), ('DFL', 'USSenDFL'), ('IND', 'USSenIP')]:
                try:
                    votes = int(row.get(col, '0') or '0')
                    if votes > 0:
                        county_results[county]['U.S. Senate'][party] += votes
                except ValueError:
                    continue
            
            # Governor: GovR, GovDFL, GovIP, GovWI
            for party, col in [('R', 'GovR'), ('DFL', 'GovDFL'), ('IND', 'GovIP')]:
                try:
                    votes = int(row.get(col, '0') or '0')
                    if votes > 0:
                        county_results[county]['Governor'][party] += votes
                except ValueError:
                    continue
            
            # Attorney General: AttGenR, AttGenDFL, AttGenIP, AttGenWI
            for party, col in [('R', 'AttGenR'), ('DFL', 'AttGenDFL'), ('IND', 'AttGenIP')]:
                try:
                    votes = int(row.get(col, '0') or '0')
                    if votes > 0:
                        county_results[county]['Attorney General'][party] += votes
                except ValueError:
                    continue
            
            # Secretary of State: SOSR, SOSDFL, SOSIP, SOSWI
            for party, col in [('R', 'SOSR'), ('DFL', 'SOSDFL'), ('IND', 'SOSIP')]:
                try:
                    votes = int(row.get(col, '0') or '0')
                    if votes > 0:
                        county_results[county]['Secretary of State'][party] += votes
                except ValueError:
                    continue
            
            # State Auditor: STAUDR, STAUDDFL, STAUDIP, STAUDWI
            for party, col in [('R', 'STAUDR'), ('DFL', 'STAUDDFL'), ('IND', 'STAUDIP')]:
                try:
                    votes = int(row.get(col, '0') or '0')
                    if votes > 0:
                        county_results[county]['State Auditor'][party] += votes
                except ValueError:
                    continue
    
    write_results(county_results, 2006, output_file)
    print(f"  ✓ Created: {output_file}")

def convert_2006_aligned(input_file, output_file):
    """Convert 2006 aligned precinct file to county level"""
    print(f"\nProcessing 2006 aligned: {os.path.basename(input_file)}")
    
    county_results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    # Custom headers for the messy 2006 file
    headers = ['PrecinctName','WD','CG','LEG','CM','SW','MCDName','JD','StateMCD','PRCT','County_ID','Fips',
               'Registered','EDR','Signature','RegMilAB','FEDAB','PresAB','TotVoters','VSCode','EquipmentModel',
               'USSenR','USSenDFL','USSenIP','USSenWI','USSenTOT',
               'GovR','GovDFL','GovIP','GovWI','GovTOT',
               'AttGenR','AttGenDFL','AttGenIP','AttGenWI','AttGenTOT',
               'SOSR','SOSDFL','SOSIP','SOSWI','SOSTOT',
               'STAUDR','STAUDDFL','STAUDIP','STAUDWI','STAUDTOT',
               'CongR','CongDFL','CongIP','CongWI','CongTOT',
               'StateSenR','StateSenDFL','StateSenIP','StateSenWI','StateSenTOT',
               'StateHouseR','StateHouseDFL','StateHouseIP','StateHouseWI','StateHouseTOT']
    
    with open(input_file, 'r', encoding='utf-8') as f:
        # Skip the messy header row and use custom fieldnames
        next(f)
        reader = csv.DictReader(f, fieldnames=headers)
        
        for row in reader:
            if row is None:
                continue
            
            county_code = (row.get('County_ID') or '').strip()
            if not county_code:
                continue
            
            # Handle 3-digit FIPS codes
            if len(county_code) == 3:
                county_code = str((int(county_code) + 1) // 2).zfill(2)
            else:
                county_code = county_code.zfill(2)
            
            if county_code not in FIPS_TO_COUNTY:
                continue
            
            county = FIPS_TO_COUNTY[county_code]
            
            # U.S. Senate
            for party, col in [('R', 'USSenR'), ('DFL', 'USSenDFL'), ('IND', 'USSenIP')]:
                try:
                    votes = int((row.get(col) or '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['U.S. Senate'][party] += votes
                except (ValueError, KeyError):
                    continue
            
            # Governor
            for party, col in [('R', 'GovR'), ('DFL', 'GovDFL'), ('IND', 'GovIP')]:
                try:
                    votes = int((row.get(col) or '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['Governor'][party] += votes
                except (ValueError, KeyError):
                    continue
            
            # Attorney General
            for party, col in [('R', 'AttGenR'), ('DFL', 'AttGenDFL'), ('IND', 'AttGenIP')]:
                try:
                    votes = int((row.get(col) or '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['Attorney General'][party] += votes
                except (ValueError, KeyError):
                    continue
            
            # Secretary of State
            for party, col in [('R', 'SOSR'), ('DFL', 'SOSDFL'), ('IND', 'SOSIP')]:
                try:
                    votes = int((row.get(col) or '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['Secretary of State'][party] += votes
                except (ValueError, KeyError):
                    continue
            
            # State Auditor
            for party, col in [('R', 'STAUDR'), ('DFL', 'STAUDDFL'), ('IND', 'STAUDIP')]:
                try:
                    votes = int((row.get(col) or '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['State Auditor'][party] += votes
                except (ValueError, KeyError):
                    continue
    
    write_results(county_results, 2006, output_file)
    print(f"  ✓ Created: {output_file}")

def convert_2010_aligned(input_file, output_file):
    """Convert 2010 aligned precinct file to county level"""
    print(f"\nProcessing 2010 aligned: {os.path.basename(input_file)}")
    
    county_results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # Strip column names
        reader.fieldnames = [name.strip() if name else name for name in reader.fieldnames]
        
        for row in reader:
            county_code = row.get('CountyID', '').strip()
            if not county_code:
                continue
            
            # Handle 3-digit FIPS codes
            if len(county_code) == 3:
                county_code = str((int(county_code) + 1) // 2).zfill(2)
            else:
                county_code = county_code.zfill(2)
            
            if county_code not in FIPS_TO_COUNTY:
                continue
            
            county = FIPS_TO_COUNTY[county_code]
            
            # Governor
            for party, col in [('R', 'GOVR'), ('DFL', 'GOVDFL'), ('IND', 'GOVIP'), ('GP', 'GOVGP'), ('TRP', 'GOVTRP'), ('GR', 'GOVGR'), ('EDP', 'GOVEDP')]:
                try:
                    votes = int(row.get(col, '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['Governor'][party] += votes
                except (ValueError, KeyError):
                    continue
            
            # MN State Senate
            for party, col in [('R', 'MNSENR'), ('DFL', 'MNSENDFL'), ('IND', 'MNSENIP')]:
                try:
                    votes = int(row.get(col, '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['State Senate'][party] += votes
                except (ValueError, KeyError):
                    continue
            
            # Attorney General
            for party, col in [('R', 'ATGENR'), ('DFL', 'ATGENDFL'), ('IND', 'ATGENIP'), ('TRP', 'ATGENTRP')]:
                try:
                    votes = int(row.get(col, '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['Attorney General'][party] += votes
                except (ValueError, KeyError):
                    continue
            
            # Secretary of State
            for party, col in [('R', 'SOSR'), ('DFL', 'SOSDFL'), ('IND', 'SOSIP')]:
                try:
                    votes = int(row.get(col, '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['Secretary of State'][party] += votes
                except (ValueError, KeyError):
                    continue
            
            # State Auditor
            for party, col in [('R', 'STAUDR'), ('DFL', 'STAUDDFL'), ('IND', 'STAUDIP')]:
                try:
                    votes = int(row.get(col, '0').strip() or '0')
                    if votes > 0:
                        county_results[county]['State Auditor'][party] += votes
                except (ValueError, KeyError):
                    continue
    
    write_results(county_results, 2010, output_file)
    print(f"  ✓ Created: {output_file}")

def convert_2024(input_file, output_file):
    """Convert 2024 which has a wide format with vote totals in columns"""
    print(f"\nProcessing 2024: {os.path.basename(input_file)}")
    
    county_results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            county_code = row['COUNTYCODE'].zfill(2)
            county_name = row['COUNTYNAME']
            
            # President columns: USPRSR, USPRSDFL, USPRSLIB, USPRSWTP, USPRSG, USPRSSLP, USPRSSWP, USPRSJFA, USPRSIND
            for party, col in [('R', 'USPRSR'), ('DFL', 'USPRSDFL'), ('LIB', 'USPRSLIB'),
                              ('WTP', 'USPRSWTP'), ('G', 'USPRSG'), ('SLP', 'USPRSSLP'),
                              ('SWP', 'USPRSSWP'), ('JFA', 'USPRSJFA'), ('IND', 'USPRSIND')]:
                try:
                    votes = int(row.get(col, '0') or '0')
                    if votes > 0:
                        county_results[county_name]['President'][party] += votes
                except ValueError:
                    continue
            
            # U.S. Senate columns: USSENR, USSENDFL, USSENLIB, USSENIA
            for party, col in [('R', 'USSENR'), ('DFL', 'USSENDFL'), ('LIB', 'USSENLIB'), ('IA', 'USSENIA')]:
                try:
                    votes = int(row.get(col, '0') or '0')
                    if votes > 0:
                        county_results[county_name]['U.S. Senate'][party] += votes
                except ValueError:
                    continue
    
    write_results(county_results, 2024, output_file)
    print(f"  ✓ Created: {output_file}")

def aggregate_precinct_to_county(input_file, output_file):
    """Aggregate precinct-level OpenElections format to county level"""
    print(f"\nAggregating precinct data: {os.path.basename(input_file)}")
    
    county_data = {}
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            county = row.get('county', '').strip()
            office = row.get('office', '').strip()
            district = row.get('district', '').strip()
            party = row.get('party', '').strip()
            candidate = row.get('candidate', '').strip()
            votes = int(row.get('votes', 0))
            
            key = (county, office, district, party, candidate)
            if key in county_data:
                county_data[key] += votes
            else:
                county_data[key] = votes
    
    # Write aggregated results
    results = []
    for (county, office, district, party, candidate), votes in sorted(county_data.items()):
        normalized_county = normalize_county(county)
        county_code = COUNTY_CODES.get(normalized_county, '')
        results.append([county_code, normalized_county, office, district, party, candidate, str(votes), ''])
    
    # Calculate percentages
    office_totals = {}
    for row in results:
        county_code, county, office, district = row[0], row[1], row[2], row[3]
        votes = int(row[6])
        key = (county_code, office, district)
        if key in office_totals:
            office_totals[key] += votes
        else:
            office_totals[key] = votes
    
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
    
    print(f"  ✓ Created: {output_file} ({len(results)} rows)")

def write_results(county_results, year, output_file):
    """Write county results to OpenElections format"""
    results = []
    
    for county in sorted(county_results.keys()):
        county_code = COUNTY_CODES[county]
        for office in sorted(county_results[county].keys()):
            party_votes = county_results[county][office]
            total = sum(party_votes.values())
            
            for party, votes in sorted(party_votes.items()):
                if votes > 0:
                    candidate = get_candidate_name(year, office, party)
                    pct = (votes / total * 100) if total > 0 else 0
                    results.append([
                        county_code, county, office, '',
                        party, candidate, str(votes), f'{pct:.2f}'
                    ])
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['county_code', 'county', 'office', 'district', 'party', 'candidate', 'votes', 'pct'])
        writer.writerows(results)

if __name__ == "__main__":
    data_dir = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data"
    
    print("="*60)
    print("Converting Outlier Election Files")
    print("="*60)
    
    # 1992, 1994, 1996, 1998 with aligned files
    for year, filename in [
        (1992, '1992_Vote_Stats.csv'),
        (1994, '1994_Vote_Stats.csv'),
        (1996, '1996_Vote_Stats-aligned.csv'),
        (1998, '1998_Vote_Stats-aligned.csv')
    ]:
        input_path = os.path.join(data_dir, filename)
        output_name = {
            1992: '19921103__mn__general__county.csv',
            1994: '19941108__mn__general__county.csv',
            1996: '19961105__mn__general__county.csv',
            1998: '19981103__mn__general__county.csv'
        }[year]
        output_path = os.path.join(data_dir, output_name)
        
        if os.path.exists(input_path):
            convert_aligned_precinct_file(input_path, year, output_path)
    
    # 2000
    if os.path.exists(os.path.join(data_dir, 'full_00results-aligned.csv')):
        convert_2000(
            os.path.join(data_dir, 'full_00results-aligned.csv'),
            os.path.join(data_dir, '20001107__mn__general__county.csv')
        )
    
    # 2002
    if os.path.exists(os.path.join(data_dir, '2002_general_results - Aligned Results.csv')):
        convert_2002_aligned(
            os.path.join(data_dir, '2002_general_results - Aligned Results.csv'),
            os.path.join(data_dir, '20021105__mn__general__county.csv')
        )
    
    # 2004
    if os.path.exists(os.path.join(data_dir, '2004_general_results.csv')):
        convert_2004(
            os.path.join(data_dir, '2004_general_results.csv'),
            os.path.join(data_dir, '20041102__mn__general__county.csv')
        )
    
    # 2006
    if os.path.exists(os.path.join(data_dir, '2006_general_results - Aligned Results.csv')):
        convert_2006_aligned(
            os.path.join(data_dir, '2006_general_results - Aligned Results.csv'),
            os.path.join(data_dir, '20061107__mn__general__county.csv')
        )
    
    # 2008
    if os.path.exists(os.path.join(data_dir, '2008_general_results - Results.csv')):
        convert_2008(
            os.path.join(data_dir, '2008_general_results - Results.csv'),
            os.path.join(data_dir, '20081104__mn__general__county.csv')
        )
    
    # 2010
    if os.path.exists(os.path.join(data_dir, '2010_general_results_final - Aligned Results.csv')):
        convert_2010_aligned(
            os.path.join(data_dir, '2010_general_results_final - Aligned Results.csv'),
            os.path.join(data_dir, '20101102__mn__general__county.csv')
        )
    
    # 2024 special format
    convert_2024(
        os.path.join(data_dir, '2024-general-federal-state-results-by-precinct-official - Precinct-Results.csv'),
        os.path.join(data_dir, '20241105__mn__general__county.csv')
    )
    
    # 2020-2022 precinct aggregation
    precinct_files = [
        ('20201103__mn__general__precinct.csv', '20201103__mn__general__county.csv'),
        ('20221108__mn__general__precinct.csv', '20221108__mn__general__county.csv'),
    ]
    
    for input_name, output_name in precinct_files:
        input_path = os.path.join(data_dir, input_name)
        output_path = os.path.join(data_dir, output_name)
        if os.path.exists(input_path):
            aggregate_precinct_to_county(input_path, output_path)
    
    print("\n" + "="*60)
    print("All outlier files converted!")
    print("="*60)
