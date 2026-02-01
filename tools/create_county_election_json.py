"""
Create comprehensive county election JSON with detailed results
"""

import csv
import json
import os
from collections import defaultdict

def get_competitiveness(margin_pct):
    """
    Determine competitiveness category based on margin percentage
    Matches the 15-category legend with Annihilation, Dominant, Stronghold, Safe, Likely, Lean, Tilt, and Tossup
    """
    abs_margin = abs(margin_pct)
    
    # Republican margins (positive)
    if margin_pct >= 40:
        return {
            "category": "Annihilation Republican",
            "party": "Republican",
            "code": "R_ANNIHILATION",
            "color": "#67000d"
        }
    elif margin_pct >= 30:
        return {
            "category": "Dominant Republican",
            "party": "Republican",
            "code": "R_DOMINANT",
            "color": "#a50f15"
        }
    elif margin_pct >= 20:
        return {
            "category": "Stronghold Republican",
            "party": "Republican",
            "code": "R_STRONGHOLD",
            "color": "#cb181d"
        }
    elif margin_pct >= 10:
        return {
            "category": "Safe Republican",
            "party": "Republican",
            "code": "R_SAFE",
            "color": "#ef3b2c"
        }
    elif margin_pct >= 5.5:
        return {
            "category": "Likely Republican",
            "party": "Republican",
            "code": "R_LIKELY",
            "color": "#fb6a4a"
        }
    elif margin_pct >= 1:
        return {
            "category": "Lean Republican",
            "party": "Republican",
            "code": "R_LEAN",
            "color": "#fcae91"
        }
    elif margin_pct >= 0.5:
        return {
            "category": "Tilt Republican",
            "party": "Republican",
            "code": "R_TILT",
            "color": "#fee8c8"
        }
    # Tossup
    elif abs_margin < 0.5:
        return {
            "category": "Tossup",
            "party": "Swing",
            "code": "TOSSUP",
            "color": "#f7f7f7"
        }
    # Democratic margins (negative)
    elif margin_pct >= -1:
        return {
            "category": "Tilt Democratic",
            "party": "Democratic",
            "code": "D_TILT",
            "color": "#e1f5fe"
        }
    elif margin_pct >= -5.5:
        return {
            "category": "Lean Democratic",
            "party": "Democratic",
            "code": "D_LEAN",
            "color": "#c6dbef"
        }
    elif margin_pct >= -10:
        return {
            "category": "Likely Democratic",
            "party": "Democratic",
            "code": "D_LIKELY",
            "color": "#9ecae1"
        }
    elif margin_pct >= -20:
        return {
            "category": "Safe Democratic",
            "party": "Democratic",
            "code": "D_SAFE",
            "color": "#6baed6"
        }
    elif margin_pct >= -30:
        return {
            "category": "Stronghold Democratic",
            "party": "Democratic",
            "code": "D_STRONGHOLD",
            "color": "#3182bd"
        }
    elif margin_pct >= -40:
        return {
            "category": "Dominant Democratic",
            "party": "Democratic",
            "code": "D_DOMINANT",
            "color": "#08519c"
        }
    else:
        return {
            "category": "Annihilation Democratic",
            "party": "Democratic",
            "code": "D_ANNIHILATION",
            "color": "#08306b"
        }

def normalize_office_name(office):
    """Normalize office names for consistent keys"""
    office_map = {
        'President': 'presidential',
        'U.S. Senate': 'us_senate',
        'Governor': 'governor',
        'Secretary of State': 'secretary_of_state',
        'Attorney General': 'attorney_general',
        'State Auditor': 'state_auditor',
        'State Treasurer': 'state_treasurer'
    }
    return office_map.get(office, office.lower().replace(' ', '_'))

def normalize_candidate_name(name):
    """Normalize candidate names to proper title case"""
    if not name or not name.strip():
        return name
    
    # Remove extra whitespace
    name = ' '.join(name.split())
    
    # List of words that should stay lowercase (unless at start)
    lowercase_words = {'de', 'van', 'von', 'der', 'el', 'la', 'le', 'du'}
    
    # Roman numerals that should stay uppercase
    roman_numerals = {'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'}
    
    # Split on spaces and handle each word
    words = name.split()
    result = []
    
    for i, word in enumerate(words):
        # Preserve roman numerals in uppercase
        if word.upper() in roman_numerals:
            word = word.upper()
        # Handle special cases with apostrophes (O'Brien, D'Angelo)
        elif "'" in word:
            parts = word.split("'")
            word = "'".join([p.capitalize() for p in parts])
        # Handle hyphenated names
        elif "-" in word:
            parts = word.split("-")
            word = "-".join([p.capitalize() for p in parts])
        # Handle Mc names (McDonald, McCarthy)
        elif word.lower().startswith('mc') and len(word) > 2:
            word = 'Mc' + word[2:].capitalize()
        # Handle Mac names (MacDonald)
        elif word.lower().startswith('mac') and len(word) > 3:
            word = 'Mac' + word[3:].capitalize()
        # Keep certain words lowercase unless they're first
        elif i > 0 and word.lower() in lowercase_words:
            word = word.lower()
        else:
            word = word.capitalize()
        
        result.append(word)
    
    return ' '.join(result)

def get_contest_name(office, year):
    """Get full contest name"""
    contest_map = {
        'President': f'PRESIDENT AND VICE PRESIDENT OF THE UNITED STATES',
        'U.S. Senate': f'UNITED STATES SENATOR',
        'Governor': f'GOVERNOR',
        'Secretary of State': f'SECRETARY OF STATE',
        'Attorney General': f'ATTORNEY GENERAL',
        'State Auditor': f'STATE AUDITOR',
        'State Treasurer': f'STATE TREASURER'
    }
    return contest_map.get(office, office.upper())

def process_election_files():
    """Process all election CSV files and create comprehensive JSON"""
    
    data_dir = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data"
    
    # Map file names to years
    files = {
        1990: '19901106__mn__general__county.csv',
        1992: '19921103__mn__general__county.csv',
        1994: '19941108__mn__general__county.csv',
        1996: '19961105__mn__general__county.csv',
        1998: '19981103__mn__general__county.csv',
        2000: '20001107__mn__general__county.csv',
        2002: '20021105__mn__general__county.csv',
        2004: '20041102__mn__general__county.csv',
        2006: '20061107__mn__general__county.csv',
        2008: '20081104__mn__general__county.csv',
        2010: '20101102__mn__general__county.csv',
        2012: '20121106__mn__general__county.csv',
        2014: '20141104__mn__general__county.csv',
        2016: '20161108__mn__general__county.csv',
        2018: '20181106__mn__general__county.csv',
        2020: '20201103__mn__general__county.csv',
        2022: '20221108__mn__general__county.csv',
        2024: '20241105__mn__general__county.csv',
    }
    
    results_by_year = {}
    
    for year, filename in sorted(files.items()):
        filepath = os.path.join(data_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠ Skipping {year}: File not found")
            continue
        
        print(f"Processing {year}...")
        
        # Read the CSV file
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Organize by office and county
            year_data = defaultdict(lambda: defaultdict(lambda: {
                'county': '',
                'votes_by_party': {},
                'candidates_by_party': {}
            }))
            
            for row in reader:
                county = row['county']
                office = row['office']
                party = row['party']
                candidate = row['candidate']
                votes = int(row['votes'])
                
                # Only include statewide executive offices, US Senate, and President
                allowed_offices = ['President', 'U.S. Senate', 'Governor', 'Secretary of State', 
                                 'Attorney General', 'State Auditor']
                if office not in allowed_offices:
                    continue
                
                # Normalize party names - IR (Independent-Republican) should be R
                if party == 'IR':
                    party = 'R'
                
                year_data[office][county]['county'] = county
                
                # Aggregate votes for the same party
                if party in year_data[office][county]['votes_by_party']:
                    year_data[office][county]['votes_by_party'][party] += votes
                else:
                    year_data[office][county]['votes_by_party'][party] = votes
                
                # Store candidate name (prefer non-empty names, normalize to title case)
                if party in year_data[office][county]['candidates_by_party']:
                    # If we already have a candidate name and this one is not empty, update
                    if candidate and candidate.strip():
                        year_data[office][county]['candidates_by_party'][party] = normalize_candidate_name(candidate)
                else:
                    year_data[office][county]['candidates_by_party'][party] = normalize_candidate_name(candidate) if candidate else candidate
        
        # Process each office for this year
        year_results = {}
        
        for office, counties in year_data.items():
            office_key = normalize_office_name(office)
            contest_id = f"{office_key}_{year}"
            contest_name = get_contest_name(office, year)
            
            if office_key not in year_results:
                year_results[office_key] = {}
            
            year_results[office_key][contest_id] = {
                'contest_name': contest_name,
                'results': {}
            }
            
            for county, data in counties.items():
                votes = data['votes_by_party']
                candidates = data['candidates_by_party']
                
                # Get DFL and Republican votes
                dem_votes = votes.get('DFL', 0)
                rep_votes = votes.get('R', 0)
                
                # Calculate other votes (everything except DFL and R)
                other_votes = sum(v for k, v in votes.items() if k not in ['DFL', 'R'])
                
                total_votes = sum(votes.values())
                two_party_total = dem_votes + rep_votes
                
                # Calculate margin (positive = Republican lead, negative = Democratic lead)
                margin = rep_votes - dem_votes
                margin_pct = round((margin / two_party_total * 100), 2) if two_party_total > 0 else 0
                
                # Determine winner
                if dem_votes > rep_votes:
                    winner = "DEM"
                elif rep_votes > dem_votes:
                    winner = "REP"
                else:
                    winner = "TIE"
                
                # Get competitiveness
                competitiveness = get_competitiveness(margin_pct)
                
                county_result = {
                    'county': county,
                    'contest': contest_name,
                    'year': str(year),
                    'dem_candidate': candidates.get('DFL', ''),
                    'rep_candidate': candidates.get('R', ''),
                    'dem_votes': dem_votes,
                    'rep_votes': rep_votes,
                    'other_votes': other_votes,
                    'total_votes': total_votes,
                    'two_party_total': two_party_total,
                    'margin': abs(margin),
                    'margin_pct': abs(margin_pct),
                    'winner': winner,
                    'competitiveness': competitiveness,
                    'all_parties': dict(votes)
                }
                
                year_results[office_key][contest_id]['results'][county] = county_result
        
        results_by_year[str(year)] = year_results
    
    # Create final JSON structure
    output = {
        'metadata': {
            'state': 'Minnesota',
            'state_code': 'MN',
            'total_counties': 87,
            'years_covered': sorted([int(y) for y in results_by_year.keys()]),
            'data_source': 'Minnesota Secretary of State',
            'generated_date': '2026-02-01'
        },
        'results_by_year': results_by_year
    }
    
    # Write to file
    output_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\mn_county_elections.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✓ Created: {output_file}")
    print(f"  Years: {len(results_by_year)}")
    total_contests = sum(len(year_data) for year_data in results_by_year.values())
    print(f"  Total contests: {total_contests}")

if __name__ == "__main__":
    print("="*60)
    print("Creating Minnesota County Election JSON")
    print("="*60)
    process_election_files()
    print("="*60)
    print("Complete!")
    print("="*60)
