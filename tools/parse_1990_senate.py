"""
Parse 1990 Minnesota election text data and convert to OpenElections CSV format
"""

import csv
import re

def parse_1990_text_file(text_file, output_csv):
    """Parse the extracted text file and create proper CSV"""
    
    # Minnesota county codes
    county_codes = {
        'Aitkin': '01', 'Anoka': '02', 'Becker': '03', 'Beltrami': '04',
        'Benton': '05', 'BigStone': '06', 'Big Stone': '06', 'BlueEarth': '07', 'Blue Earth': '07', 
        'Brown': '08', 'Carlton': '09', 'Carver': '10', 'Cass': '11', 'Chippewa': '12',
        'Chisago': '13', 'Clay': '14', 'Clearwater': '15', 'Cook': '16',
        'Cottonwood': '17', 'CrowWing': '18', 'Crow Wing': '18', 'Dakota': '19', 'Dodge': '20',
        'Douglas': '21', 'Faribault': '22', 'Fillmore': '23', 'Freeborn': '24',
        'Goodhue': '25', 'Grant': '26', 'Hennepin': '27', 'Houston': '28',
        'Hubbard': '29', 'Isanti': '30', 'Itasca': '31', 'Jackson': '32',
        'Kanabec': '33', 'Kandiyohi': '34', 'Kittson': '35', 'Koochiching': '36',
        'LacquiParle': '37', 'Lac qui Parle': '37', 'Lake': '38', 'LakeoftheWoods': '39', 
        'Lakeof theWoods': '39', 'Lake of the Woods': '39', 'LeSueur': '40', 'Le Sueur': '40',
        'Lincoln': '41', 'Lyon': '42', 'McLeod': '43', 'Mahnomen': '44',
        'Marshall': '45', 'Martin': '46', 'Meeker': '61', 'MilleLacs': '47', 'Mille Lacs': '47', 
        'Morrison': '48', 'Mower': '49', 'Murray': '50', 'Nicollet': '51', 'Nobles': '52',
        'Norman': '53', 'Olmsted': '54', 'OtterTail': '55', 'Otter Tail': '55', 
        'Pennington': '56', 'Pine': '57', 'Pipestone': '58', 'Polk': '59', 'Pope': '60',
        'Ramsey': '62', 'RedLake': '63', 'Red Lake': '63', 'Redwood': '64', 'Renville': '65',
        'Rice': '66', 'Rock': '67', 'Roseau': '68', 'St.Louis': '69', 'St. Louis': '69', 'S1.Louis': '69',
        'Scott': '70', 'Sherburne': '71', 'Sibley': '72', 'Stearns': '73',
        'Steele': '74', 'Stevens': '75', 'Swift': '76', 'Todd': '77',
        'Traverse': '78', 'Wabasha': '79', 'Wadena': '80', 'Waseca': '81',
        'Washington': '82', 'Watonwan': '83', 'Wilkin': '84', 'Winona': '85',
        'Wright': '86', 'YellowMedicine': '87', 'Yellow Medicine': '87'
    }
    
    results = []
    
    with open(text_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find U.S. Senate section - get everything between "UNITED STATES SENATOR" and "GOVERNOR"
    senate_match = re.search(r'VOTE FOR UNITED STATES ?SENATOR.*?(?=VOTE FOR ?GOVERNOR)', content, re.DOTALL)
    
    if senate_match:
        senate_text = senate_match.group(0)
        lines = senate_text.split('\n')
        
        for line in lines:
            # Skip header lines
            if not line.strip() or 'COUNTY' in line or 'PAGE' in line or 'REGISTRATION' in line:
                continue
            
            # Try to match county name at the beginning - IMPORTANT: Check longest names first
            matched = False
            for county in sorted(county_codes.keys(), key=len, reverse=True):
                if line.startswith(county):
                    matched = True
                    code = county_codes[county]
                    matched = True
                    code = county_codes[county]
                    # Extract numbers from the line
                    # Format: CountyName ... Wellstone Boschwitz Bentley
                    parts = line.split()
                    
                    # Find numeric values (should be last 3 values for candidates)
                    numbers = [p.replace(',', '') for p in parts if p.replace(',', '').isdigit()]
                    
                    if len(numbers) >= 3:
                        # Last 3 numbers are candidate vote totals
                        wellstone = numbers[-3]  # DFL
                        boschwitz = numbers[-2]  # IR (Republican)
                        bentley = numbers[-1]    # GRP
                        
                        # Clean county name
                        clean_county = county
                        if clean_county == 'BigStone':
                            clean_county = 'Big Stone'
                        elif clean_county == 'BlueEarth':
                            clean_county = 'Blue Earth'
                        elif clean_county == 'CrowWing':
                            clean_county = 'Crow Wing'
                        elif clean_county == 'LacquiParle':
                            clean_county = 'Lac qui Parle'
                        elif clean_county == 'LakeoftheWoods':
                            clean_county = 'Lake of the Woods'
                        elif clean_county == 'LeSueur':
                            clean_county = 'Le Sueur'
                        elif clean_county == 'MilleLacs':
                            clean_county = 'Mille Lacs'
                        elif clean_county == 'OtterTail':
                            clean_county = 'Otter Tail'
                        elif clean_county == 'RedLake':
                            clean_county = 'Red Lake'
                        elif clean_county == 'St.Louis' or clean_county == 'S1.Louis':
                            clean_county = 'St. Louis'
                        elif clean_county == 'YellowMedicine':
                            clean_county = 'Yellow Medicine'
                        
                        # Calculate total and percentages
                        total = int(wellstone) + int(boschwitz) + int(bentley)
                        if total > 0:
                            pct_wellstone = (int(wellstone) / total * 100)
                            pct_boschwitz = (int(boschwitz) / total * 100)
                            pct_bentley = (int(bentley) / total * 100)
                            
                            results.append([code, clean_county, 'U.S. Senate', '', 'DFL', 'Paul David Wellstone', wellstone, f'{pct_wellstone:.2f}'])
                            results.append([code, clean_county, 'U.S. Senate', '', 'IR', 'Rudy Boschwitz', boschwitz, f'{pct_boschwitz:.2f}'])
                            results.append([code, clean_county, 'U.S. Senate', '', 'GRP', 'Russell B. Bentley', bentley, f'{pct_bentley:.2f}'])
                        
                        break
            
            if matched:
                continue
    
    # Find Governor section - get everything from "GOVERNOR" until TOTAL or next major section
    gov_match = re.search(r'VOTE FOR ?GOVERNOR.*?(?=VOTE FOR ?STATE AUDITOR|PAGE 7)', content, re.DOTALL)
    
    if gov_match:
        gov_text = gov_match.group(0)
        lines = gov_text.split('\n')
        
        for line in lines:
            # Skip header lines
            if not line.strip() or 'COUNTY' in line or 'PAGE' in line or 'GOVERNOR' in line or 'RUDY' in line:
                continue
            
            # Try to match county name at the beginning - IMPORTANT: Check longest names first
            matched = False
            for county in sorted(county_codes.keys(), key=len, reverse=True):
                if line.startswith(county):
                    matched = True
                    matched = True
                    code = county_codes[county]
                    # Extract numbers from the line
                    # Format: CountyName Perpich Carlson ...others...
                    parts = line.split()
                    
                    # Find numeric values (Governor candidates are first set)
                    numbers = [p.replace(',', '') for p in parts if p.replace(',', '').isdigit()]
                    
                    if len(numbers) >= 2:
                        # First 2 numbers are main candidates
                        perpich = numbers[0]  # DFL
                        carlson = numbers[1]  # IR (Republican)
                        
                        # Clean county name
                        clean_county = county
                        if clean_county == 'BigStone':
                            clean_county = 'Big Stone'
                        elif clean_county == 'BlueEarth':
                            clean_county = 'Blue Earth'
                        elif clean_county == 'CrowWing':
                            clean_county = 'Crow Wing'
                        elif clean_county == 'LacquiParle':
                            clean_county = 'Lac qui Parle'
                        elif clean_county == 'LakeoftheWoods':
                            clean_county = 'Lake of the Woods'
                        elif clean_county == 'LeSueur':
                            clean_county = 'Le Sueur'
                        elif clean_county == 'MilleLacs':
                            clean_county = 'Mille Lacs'
                        elif clean_county == 'OtterTail':
                            clean_county = 'Otter Tail'
                        elif clean_county == 'RedLake':
                            clean_county = 'Red Lake'
                        elif clean_county == 'St.Louis' or clean_county == 'S1.Louis':
                            clean_county = 'St. Louis'
                        elif clean_county == 'YellowMedicine':
                            clean_county = 'Yellow Medicine'
                        
                        # Calculate total and percentages
                        total = int(perpich) + int(carlson)
                        if total > 0:
                            pct_perpich = (int(perpich) / total * 100)
                            pct_carlson = (int(carlson) / total * 100)
                            
                            results.append([code, clean_county, 'Governor', '', 'DFL', 'Rudy Perpich', perpich, f'{pct_perpich:.2f}'])
                            results.append([code, clean_county, 'Governor', '', 'IR', 'Arne Carlson', carlson, f'{pct_carlson:.2f}'])
                        
                        break
            
            if matched:
                continue
    
    # Write to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['county_code', 'county', 'office', 'district', 'party', 'candidate', 'votes', 'pct'])
        writer.writerows(results)
    
    senate_count = len([r for r in results if r[2] == 'U.S. Senate']) // 3
    gov_count = len([r for r in results if r[2] == 'Governor']) // 2
    
    print(f"\n✓ Created CSV: {output_csv}")
    print(f"  Total rows: {len(results)}")
    print(f"  U.S. Senate: {senate_count} counties")
    print(f"  Governor: {gov_count} counties")
    print(f"\n1990 Results:")
    print(f"  U.S. Senate: Paul Wellstone (DFL) defeated Rudy Boschwitz (IR)")
    print(f"  Governor: Arne Carlson (IR) defeated Rudy Perpich (DFL)")
    
    return len(results)

if __name__ == "__main__":
    text_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\19901106__mn__general__county_text.txt"
    output_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\19901106__mn__general__county.csv"
    
    print("="*60)
    print("Parsing 1990 Minnesota Election Results")
    print("U.S. Senate: Wellstone (DFL) vs Boschwitz (IR)")
    print("Governor: Carlson (IR) vs Perpich (DFL)")  
    print("="*60)
    
    parse_1990_text_file(text_file, output_file)
