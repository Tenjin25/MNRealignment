"""
Extract 1990 Minnesota Governor and U.S. Senate results from PDF
Focused extraction for key races showing Republican strength
"""

import sys
import os
import csv
import re

def extract_1990_races(pdf_path, output_csv):
    """Extract specific races from 1990 PDF"""
    try:
        import pdfplumber
    except ImportError:
        print("Installing pdfplumber...")
        os.system(f'"{sys.executable}" -m pip install pdfplumber')
        import pdfplumber
    
    # Minnesota county codes
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
    
    all_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Extracting from {len(pdf.pages)} pages PDF...\n")
        
        # Extract all text and tables from county summary pages
        for page_num in range(2, 28):  # Pages 3-28 contain county summaries
            page = pdf.pages[page_num]
            text = page.extract_text()
            
            if not text:
                continue
            
            # Look for race headers in text
            if 'UNITED STATES SENATOR' in text or 'SENATOR' in text:
                print(f"Page {page_num + 1}: Found U.S. Senate data")
            if 'GOVERNOR' in text:
                print(f"Page {page_num + 1}: Found Governor data")
            
            # Extract tables
            tables = page.extract_tables()
            for table in tables:
                if table and len(table) > 0:
                    # Add raw table data for analysis
                    all_data.extend(table)
    
    # Save raw extracted data for review
    raw_output = output_csv.replace('.csv', '_raw.csv')
    with open(raw_output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(all_data)
    
    print(f"\n✓ Raw data extracted to: {raw_output}")
    print(f"  Total rows: {len(all_data)}")
    print("\nNext steps:")
    print("  1. Review the raw CSV to identify data patterns")
    print("  2. Look for columns with county names and vote totals")
    print("  3. We can then write a parser based on the actual structure")
    
    # Also save the text content for reference
    text_output = output_csv.replace('.csv', '_text.txt')
    with pdfplumber.open(pdf_path) as pdf:
        with open(text_output, 'w', encoding='utf-8') as f:
            for page_num in range(2, 28):
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text:
                    f.write(f"\n\n{'='*60}\nPAGE {page_num + 1}\n{'='*60}\n\n")
                    f.write(text)
    
    print(f"✓ Text content saved to: {text_output}")

if __name__ == "__main__":
    pdf_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\1990-11-06-g-sec.pdf"
    output_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\19901106__mn__general__county.csv"
    
    if not os.path.exists(pdf_file):
        print(f"Error: PDF file not found at {pdf_file}")
        sys.exit(1)
    
    print("="*60)
    print("1990 Minnesota Election Data Extraction")
    print("Target: Governor and U.S. Senate races")
    print("="*60 + "\n")
    
    extract_1990_races(pdf_file, output_file)
