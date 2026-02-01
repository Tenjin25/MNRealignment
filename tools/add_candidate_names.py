"""
Add candidate names to OpenElections CSV files that are missing them
"""

import csv
import sys
import os

sys.path.append(os.path.dirname(__file__))
from candidate_lookup import get_candidate_name

def add_candidate_names(input_file, year):
    """Add candidate names to a CSV file based on year, office, and party"""
    
    print(f"\nProcessing {year}: {os.path.basename(input_file)}")
    
    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            office = row['office']
            party = row['party']
            candidate = row.get('candidate', '').strip()
            
            # Look up the candidate name
            new_candidate = get_candidate_name(year, office, party)
            
            # Always update if we found a name (force update)
            if new_candidate:
                row['candidate'] = new_candidate
            elif not candidate:
                # Keep it empty if no lookup found and it was already empty
                row['candidate'] = ''
            
            rows.append(row)
    
    # Write back
    with open(input_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['county_code', 'county', 'office', 'district', 'party', 'candidate', 'votes', 'pct'])
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"  ✓ Updated {len(rows)} rows with candidate names")

if __name__ == "__main__":
    data_dir = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data"
    
    files_to_update = [
        ('19921103__mn__general__county.csv', 1992),
        ('19941108__mn__general__county.csv', 1994),
        ('19961105__mn__general__county.csv', 1996),
        ('19981103__mn__general__county.csv', 1998),
        ('20001107__mn__general__county.csv', 2000),
        ('20021105__mn__general__county.csv', 2002),
        ('20041102__mn__general__county.csv', 2004),
        ('20081104__mn__general__county.csv', 2008),
        ('20101102__mn__general__county.csv', 2010),
    ]
    
    print("="*60)
    print("Adding Candidate Names to OpenElections Files")
    print("="*60)
    
    for filename, year in files_to_update:
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            add_candidate_names(filepath, year)
        else:
            print(f"\n⚠ File not found: {filename}")
    
    print("\n" + "="*60)
    print("Complete!")
    print("="*60)
