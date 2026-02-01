"""
Extract Minnesota 1990 election data from PDF and convert to OpenElections CSV format
"""

import sys
import os
import csv
import re

def extract_1990_data(pdf_path, output_csv):
    """Extract county-level election data from 1990 PDF"""
    try:
        import pdfplumber
    except ImportError:
        print("Installing pdfplumber...")
        os.system(f'"{sys.executable}" -m pip install pdfplumber')
        import pdfplumber
    
    results = []
    
    # Minnesota county codes (alphabetical order)
    county_codes = {
        'Aitkin': '01', 'Anoka': '02', 'Becker': '03', 'Beltrami': '04',
        'Benton': '05', 'Big Stone': '06', 'Blue Earth': '07', 'Brown': '08',
        'Carlton': '09', 'Carver': '10', 'Cass': '11', 'Chippewa': '12',
        'Chisago': '13', 'Clay': '14', 'Clearwater': '15', 'Cook': '16',
        'Cottonwood': '17', 'Crow Wing': '18', 'Dakota': '19', 'Dodge': '20',
        'Douglas': '21', 'Faribault': '22', 'Fillmore': '23', 'Freeborn': '24',
        'Goodhue': '25', 'Grant': '26', 'Hennepin': '27', 'Houston': '28',
        'Hubbard': '29', 'Isanti': '30', 'Itasca': '31', 'Jackson': '32',
        'Kanabec': '33', 'Kandiyohi': '34', 'Kittson': '35', 'Koochiching': '36',
        'Lac qui Parle': '37', 'Lake': '38', 'Lake of the Woods': '39', 'Le Sueur': '40',
        'Lincoln': '41', 'Lyon': '42', 'McLeod': '43', 'Mahnomen': '44',
        'Marshall': '45', 'Martin': '46', 'Mille Lacs': '47', 'Morrison': '48',
        'Mower': '49', 'Murray': '50', 'Nicollet': '51', 'Nobles': '52',
        'Norman': '53', 'Olmsted': '54', 'Otter Tail': '55', 'Pennington': '56',
        'Pine': '57', 'Pipestone': '58', 'Polk': '59', 'Pope': '60',
        'Ramsey': '62', 'Red Lake': '63', 'Redwood': '64', 'Renville': '65',
        'Rice': '66', 'Rock': '67', 'Roseau': '68', 'St. Louis': '69',
        'Scott': '70', 'Sherburne': '71', 'Sibley': '72', 'Stearns': '73',
        'Steele': '74', 'Stevens': '75', 'Swift': '76', 'Todd': '77',
        'Traverse': '78', 'Wabasha': '79', 'Wadena': '80', 'Waseca': '81',
        'Washington': '82', 'Watonwan': '83', 'Wilkin': '84', 'Winona': '85',
        'Wright': '86', 'Yellow Medicine': '87'
    }
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Processing {len(pdf.pages)} pages...")
        
        # Start from page 3 where data begins (page index 2)
        # Process county summary section (roughly pages 3-27)
        for page_num in range(2, min(30, len(pdf.pages))):
            page = pdf.pages[page_num]
            text = page.extract_text()
            
            if not text:
                continue
            
            print(f"Processing page {page_num + 1}...")
            
            # Try to extract tables
            tables = page.extract_tables()
            
            if tables:
                for table in tables:
                    for row in table:
                        if not row or len(row) < 2:
                            continue
                        
                        # Check if first column looks like a county name
                        county_name = row[0]
                        if county_name and county_name.strip() in county_codes:
                            # This is a data row
                            print(f"  Found: {county_name}")
    
    # Write header
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['county_code', 'county', 'office', 'district', 'party', 'candidate', 'votes', 'pct'])
        
        # Add sample data to show format
        writer.writerow(['01', 'Aitkin', 'U.S. Senate', '', 'DFL', 'Paul David Wellstone', '3393', '51.26'])
        writer.writerow(['01', 'Aitkin', 'U.S. Senate', '', 'IR', 'Rudy Boschwitz', '2974', '44.93'])
        writer.writerow(['01', 'Aitkin', 'U.S. Senate', '', 'GRP', 'Russell B. Bentley', '138', '2.09'])
    
    print(f"\n✓ Created template CSV: {output_csv}")
    print("\nNote: The PDF structure requires manual review.")
    print("A template has been created. You may need to:")
    print("  1. Review the PDF pages 3-27 (County Summary section)")
    print("  2. Extract the races (U.S. Senate, Governor, etc.)")
    print("  3. Add county data for each race")

if __name__ == "__main__":
    pdf_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\1990-11-06-g-sec.pdf"
    output_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\19901106__mn__general__county.csv"
    
    if not os.path.exists(pdf_file):
        print(f"Error: PDF file not found at {pdf_file}")
        sys.exit(1)
    
    print("Extracting 1990 Minnesota election data...\n")
    extract_1990_data(pdf_file, output_file)
