"""
Extract ALL statewide races from 1990 Minnesota PDF for OpenElections
Includes: U.S. Senate, Governor, Secretary of State, State Auditor, State Treasurer, Attorney General
"""

import csv
import re

def parse_1990_complete(text_file, output_csv):
    """Parse all statewide races from 1990 PDF"""
    
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
    
    def clean_county_name(county):
        """Standardize county names"""
        if county == 'BigStone':
            return 'Big Stone'
        elif county == 'BlueEarth':
            return 'Blue Earth'
        elif county == 'CrowWing':
            return 'Crow Wing'
        elif county == 'LacquiParle':
            return 'Lac qui Parle'
        elif county == 'LakeoftheWoods' or county == 'Lakeof theWoods':
            return 'Lake of the Woods'
        elif county == 'LeSueur':
            return 'Le Sueur'
        elif county == 'MilleLacs':
            return 'Mille Lacs'
        elif county == 'OtterTail':
            return 'Otter Tail'
        elif county == 'RedLake':
            return 'Red Lake'
        elif county == 'St.Louis' or county == 'S1.Louis':
            return 'St. Louis'
        elif county == 'YellowMedicine':
            return 'Yellow Medicine'
        return county
    
    results = []
    
    with open(text_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. U.S. SENATE
    senate_match = re.search(r'VOTE FOR UNITED STATES ?SENATOR.*?(?=VOTE FOR ?GOVERNOR)', content, re.DOTALL)
    if senate_match:
        print("Extracting U.S. Senate...")
        lines = senate_match.group(0).split('\n')
        for line in lines:
            if not line.strip() or 'COUNTY' in line or 'PAGE' in line or 'REGISTRATION' in line:
                continue
            for county in sorted(county_codes.keys(), key=len, reverse=True):
                if line.startswith(county):
                    code = county_codes[county]
                    parts = line.split()
                    numbers = [p.replace(',', '') for p in parts if p.replace(',', '').isdigit()]
                    if len(numbers) >= 3:
                        wellstone, boschwitz, bentley = numbers[-3], numbers[-2], numbers[-1]
                        clean_county = clean_county_name(county)
                        total = int(wellstone) + int(boschwitz) + int(bentley)
                        if total > 0:
                            results.append([code, clean_county, 'U.S. Senate', '', 'DFL', 'Paul David Wellstone', wellstone, f'{int(wellstone)/total*100:.2f}'])
                            results.append([code, clean_county, 'U.S. Senate', '', 'IR', 'Rudy Boschwitz', boschwitz, f'{int(boschwitz)/total*100:.2f}'])
                            results.append([code, clean_county, 'U.S. Senate', '', 'GRP', 'Russell B. Bentley', bentley, f'{int(bentley)/total*100:.2f}'])
                    break
    
    # 2. GOVERNOR
    gov_match = re.search(r'GOVERNORANDLIEUTENANTGOVERNOR.*?(?=VOTE FOR ?STATE AUDITOR|PAGE 7)', content, re.DOTALL)
    if gov_match:
        print("Extracting Governor...")
        lines = gov_match.group(0).split('\n')
        for line in lines:
            if not line.strip() or 'COUNTY' in line or 'PAGE' in line or 'GOVERNOR' in line or 'RUDY' in line:
                continue
            for county in sorted(county_codes.keys(), key=len, reverse=True):
                if line.startswith(county):
                    code = county_codes[county]
                    parts = line.split()
                    numbers = [p.replace(',', '') for p in parts if p.replace(',', '').isdigit()]
                    if len(numbers) >= 2:
                        perpich, carlson = numbers[0], numbers[1]
                        clean_county = clean_county_name(county)
                        total = int(perpich) + int(carlson)
                        if total > 0:
                            results.append([code, clean_county, 'Governor', '', 'DFL', 'Rudy Perpich', perpich, f'{int(perpich)/total*100:.2f}'])
                            results.append([code, clean_county, 'Governor', '', 'IR', 'Arne Carlson', carlson, f'{int(carlson)/total*100:.2f}'])
                    break
    
    # 3. SECRETARY OF STATE (on same page as Governor - columns after Governor)
    if gov_match:
        print("Extracting Secretary of State...")
        lines = gov_match.group(0).split('\n')
        for line in lines:
            if not line.strip() or 'COUNTY' in line or 'PAGE' in line or 'GOVERNOR' in line or 'JOAN' in line:
                continue
            for county in sorted(county_codes.keys(), key=len, reverse=True):
                if line.startswith(county):
                    code = county_codes[county]
                    parts = line.split()
                    numbers = [p.replace(',', '') for p in parts if p.replace(',', '').isdigit()]
                    # Secretary of State is after Governor: positions vary, typically last 3 numbers
                    # Order in data: JOAN ANDERSON GROWE (DFL), DAVID JENNINGS (IR), CANDICE SJOSTROM (GRP)
                    if len(numbers) >= 8:
                        growe, jennings, sjostrom = numbers[-3], numbers[-2], numbers[-1]
                        clean_county = clean_county_name(county)
                        total = int(growe) + int(jennings) + int(sjostrom)
                        if total > 0:
                            results.append([code, clean_county, 'Secretary of State', '', 'DFL', 'Joan Anderson Growe', growe, f'{int(growe)/total*100:.2f}'])
                            results.append([code, clean_county, 'Secretary of State', '', 'IR', 'David Jennings', jennings, f'{int(jennings)/total*100:.2f}'])
                            results.append([code, clean_county, 'Secretary of State', '', 'GRP', 'Candice Sjostrom', sjostrom, f'{int(sjostrom)/total*100:.2f}'])
                    break
    
    # 4. STATE AUDITOR, TREASURER, ATTORNEY GENERAL
    auditor_match = re.search(r'STATEAUDITOR.*?(?=PAGE 9)', content, re.DOTALL)
    if auditor_match:
        print("Extracting State Auditor, Treasurer, Attorney General...")
        lines = auditor_match.group(0).split('\n')
        for line in lines:
            if not line.strip() or 'COUNTY' in line or 'PAGE' in line or 'AUDITOR' in line or 'MARK' in line or 'TOTAL' in line:
                continue
            for county in sorted(county_codes.keys(), key=len, reverse=True):
                if line.startswith(county):
                    code = county_codes[county]
                    parts = line.split()
                    numbers = [p.replace(',', '') for p in parts if p.replace(',', '').isdigit()]
                    
                    if len(numbers) >= 7:
                        # State Auditor: positions 0-1 (DFL MARK DAYTON, IR BOB HEINRICH)
                        dayton, heinrich = numbers[0], numbers[1]
                        # State Treasurer: positions 2-4 (DFL MICHAEL MCGRATH, IR JOHN BONNIWELL, GRP COLLEEN BURGER)
                        mcgrath, bonniwell, burger = numbers[2], numbers[3], numbers[4]
                        # Attorney General: positions 5-6 (DFL HUMPHREY III, IR KEVIN JOHNSON)
                        humphrey, johnson = numbers[5], numbers[6]
                        
                        clean_county = clean_county_name(county)
                        
                        # State Auditor
                        total = int(dayton) + int(heinrich)
                        if total > 0:
                            results.append([code, clean_county, 'State Auditor', '', 'DFL', 'Mark Dayton', dayton, f'{int(dayton)/total*100:.2f}'])
                            results.append([code, clean_county, 'State Auditor', '', 'IR', 'Bob Heinrich', heinrich, f'{int(heinrich)/total*100:.2f}'])
                        
                        # State Treasurer
                        total = int(mcgrath) + int(bonniwell) + int(burger)
                        if total > 0:
                            results.append([code, clean_county, 'State Treasurer', '', 'DFL', 'Michael A. McGrath', mcgrath, f'{int(mcgrath)/total*100:.2f}'])
                            results.append([code, clean_county, 'State Treasurer', '', 'IR', 'John Bonniwell', bonniwell, f'{int(bonniwell)/total*100:.2f}'])
                            results.append([code, clean_county, 'State Treasurer', '', 'GRP', 'Colleen Burger', burger, f'{int(burger)/total*100:.2f}'])
                        
                        # Attorney General
                        total = int(humphrey) + int(johnson)
                        if total > 0:
                            results.append([code, clean_county, 'Attorney General', '', 'DFL', 'Hubert H. Humphrey III', humphrey, f'{int(humphrey)/total*100:.2f}'])
                            results.append([code, clean_county, 'Attorney General', '', 'IR', 'Kevin E. Johnson', johnson, f'{int(johnson)/total*100:.2f}'])
                    break
    
    # Write to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['county_code', 'county', 'office', 'district', 'party', 'candidate', 'votes', 'pct'])
        writer.writerows(results)
    
    # Count results by office
    offices = {}
    for row in results:
        office = row[2]
        offices[office] = offices.get(office, 0) + 1
    
    print(f"\n✓ Created CSV: {output_csv}")
    print(f"  Total rows: {len(results)}")
    print(f"\nOffices extracted:")
    for office, count in sorted(offices.items()):
        counties = count // 2 if 'Senate' not in office else count // 3
        print(f"  {office}: {counties} counties")
    
    return len(results)

if __name__ == "__main__":
    text_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\19901106__mn__general__county_text.txt"
    output_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\19901106__mn__general__county.csv"
    
    print("="*60)
    print("1990 Minnesota Complete Election Data Extraction")
    print("All Statewide Offices for OpenElections")
    print("="*60 + "\n")
    
    parse_1990_complete(text_file, output_file)
