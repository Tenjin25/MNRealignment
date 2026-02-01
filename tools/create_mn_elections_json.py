"""
Create nested JSON file for Minnesota elections following the rating format
Includes: President, U.S. Senate, Governor, and all statewide executive offices
"""

import csv
import json
import os
from collections import defaultdict

def load_election_data(year, filename):
    """Load election data from CSV file"""
    filepath = os.path.join('data', filename)
    
    if not os.path.exists(filepath):
        print(f"  ⚠ File not found: {filename}")
        return {}
    
    results = defaultdict(lambda: defaultdict(dict))
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            county_code = row['county_code'].zfill(2)
            office = row['office']
            party = row['party']
            votes = int(row['votes'])
            
            # Only include statewide offices
            statewide_offices = [
                'President', 
                'U.S. Senate', 
                'Governor', 
                'Secretary of State', 
                'Attorney General', 
                'State Auditor',
                'State Treasurer'
            ]
            
            if office not in statewide_offices:
                continue
            
            # Store votes by party for each office
            results[county_code][office][party] = votes
    
    return results

def calculate_rating(dem_votes, rep_votes, other_votes=0):
    """
    Calculate the rating based on Democratic margin
    For Jesse Ventura (Reform/RP), treat as "other" with special handling
    """
    total = dem_votes + rep_votes + other_votes
    
    if total == 0:
        return 0
    
    # Calculate Democratic margin (D% - R%)
    dem_pct = (dem_votes / total) * 100
    rep_pct = (rep_votes / total) * 100
    margin = dem_pct - rep_pct
    
    # For races with significant third party (like Ventura 1998)
    # We'll still use D vs R margin, but note the third party presence
    
    # Rating scale based on margin
    if margin >= 40:
        return 15  # Annihilation Democratic (40%+)
    elif margin >= 30:
        return 14  # Dominant Democratic (30.00-39.99%)
    elif margin >= 20:
        return 13  # Stronghold Democratic (20.00-29.99%)
    elif margin >= 10:
        return 12  # Safe Democratic (10.00-19.99%)
    elif margin >= 5.5:
        return 11  # Likely Democratic (5.50-9.99%)
    elif margin >= 1:
        return 10  # Lean Democratic (1.00-5.49%)
    elif margin >= 0.5:
        return 9   # Tilt Democratic (0.50-0.99%)
    elif margin > -0.5:
        return 8   # Tossup (<0.50%)
    elif margin > -1:
        return 7   # Tilt Republican (0.50-0.99%)
    elif margin > -5.5:
        return 6   # Lean Republican (1.00-5.49%)
    elif margin > -10:
        return 5   # Likely Republican (5.50-9.99%)
    elif margin > -20:
        return 4   # Safe Republican (10.00-19.99%)
    elif margin > -30:
        return 3   # Stronghold Republican (20.00-29.99%)
    elif margin > -40:
        return 2   # Dominant Republican (30.00-39.99%)
    else:
        return 1   # Annihilation Republican (40%+)

def create_election_json():
    """Create the nested JSON structure for all Minnesota elections"""
    
    # Election files to process (year, filename)
    elections = [
        (1990, '19901106__mn__general__county.csv'),
        (1992, '19921103__mn__general__county.csv'),
        (1994, '19941108__mn__general__county.csv'),
        (1996, '19961105__mn__general__county.csv'),
        (1998, '19981103__mn__general__county.csv'),
        (2000, '20001107__mn__general__county.csv'),
        (2002, '20021105__mn__general__county.csv'),
        (2004, '20041102__mn__general__county.csv'),
        (2006, '20061107__mn__general__county.csv'),
        (2008, '20081104__mn__general__county.csv'),
        (2010, '20101102__mn__general__county.csv'),
        (2012, '20121106__mn__general__county.csv'),
        (2014, '20141104__mn__general__county.csv'),
        (2016, '20161108__mn__general__county.csv'),
        (2018, '20181106__mn__general__county.csv'),
        (2020, '20201103__mn__general__county.csv'),
        (2022, '20221108__mn__general__county.csv'),
        (2024, '20241105__mn__general__county.csv'),
    ]
    
    result = {}
    
    print("="*60)
    print("Creating Minnesota Elections Aggregated JSON")
    print("="*60)
    
    for year, filename in elections:
        print(f"\nProcessing {year}...")
        
        data = load_election_data(year, filename)
        
        if not data:
            continue
        
        year_key = str(year)
        result[year_key] = {}
        
        # Determine which offices exist in this year
        all_offices = set()
        for county_data in data.values():
            all_offices.update(county_data.keys())
        
        print(f"  Offices found: {', '.join(sorted(all_offices))}")
        
        # Process each office
        for office in sorted(all_offices):
            office_key = office.replace(' ', '_').replace('.', '').lower()
            result[year_key][office_key] = {}
            
            # Process each county
            for county_code, county_data in data.items():
                if office not in county_data:
                    continue
                
                party_votes = county_data[office]
                
                # Get votes by party
                dem_votes = party_votes.get('DFL', 0)
                rep_votes = party_votes.get('R', 0)
                
                # Sum all other parties
                other_votes = sum(
                    votes for party, votes in party_votes.items()
                    if party not in ['DFL', 'R']
                )
                
                # Calculate rating
                rating = calculate_rating(dem_votes, rep_votes, other_votes)
                
                result[year_key][office_key][county_code] = rating
        
        print(f"  ✓ Processed {len(data)} counties")
    
    # Save to JSON file
    output_path = 'data/mn_elections_aggregated.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✓ JSON saved to: {output_path}")
    print(f"  Years: {len(result)}")
    print(f"{'='*60}")
    
    return output_path

if __name__ == "__main__":
    create_election_json()
