"""
Comprehensive verification script for all election years
Checks for missing data, incomplete counties, and data quality issues
"""

import json
import os

def verify_all_years():
    """Verify data completeness for all years"""
    data_dir = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data"
    json_file = os.path.join(data_dir, "mn_county_elections.json")
    
    print("=" * 80)
    print("MINNESOTA ELECTION DATA VERIFICATION")
    print("=" * 80)
    
    # Load JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results = data['results_by_year']
    
    # Expected contests by year (based on election cycle)
    expected_contests = {
        # Presidential years
        1992: ['presidential'],
        1996: ['presidential', 'us_senate'],
        2000: ['presidential', 'us_senate'],
        2004: ['presidential'],
        2008: ['presidential', 'us_senate'],
        2012: ['presidential', 'us_senate'],
        2016: ['presidential'],
        2020: ['presidential', 'us_senate'],
        2024: ['presidential', 'us_senate'],
        
        # Gubernatorial years
        1990: ['governor', 'us_senate', 'attorney_general', 'secretary_of_state', 'state_auditor'],
        1994: ['governor', 'us_senate', 'attorney_general', 'secretary_of_state', 'state_auditor'],
        1998: ['governor', 'attorney_general', 'secretary_of_state', 'state_auditor'],
        2002: ['governor', 'us_senate', 'attorney_general', 'secretary_of_state', 'state_auditor'],
        2006: ['governor', 'us_senate', 'attorney_general', 'secretary_of_state', 'state_auditor'],
        2010: ['governor', 'attorney_general', 'secretary_of_state', 'state_auditor'],
        2014: ['governor', 'us_senate', 'attorney_general', 'secretary_of_state', 'state_auditor'],
        2018: ['governor', 'us_senate', 'us_senate_special', 'attorney_general', 'secretary_of_state', 'state_auditor'],
        2022: ['governor', 'attorney_general', 'secretary_of_state', 'state_auditor'],
    }
    
    total_issues = 0
    
    for year in range(1990, 2026, 2):
        print(f"\n{'='*80}")
        print(f"YEAR: {year}")
        print(f"{'='*80}")
        
        if str(year) not in results:
            print(f"ERROR: No data found for {year}")
            total_issues += 1
            continue
        
        year_data = results[str(year)]
        actual_offices = sorted(year_data.keys())
        
        print(f"OK Offices found: {len(actual_offices)}")
        
        # Check each office
        for office in actual_offices:
            office_data = year_data[office]
            
            # Get the contest key (should be only one)
            contest_keys = [k for k in office_data.keys() if k != 'metadata']
            
            if not contest_keys:
                print(f"  ERROR {office}: No contests found")
                total_issues += 1
                continue
            
            for contest_key in contest_keys:
                contest = office_data[contest_key]
                
                if 'results' not in contest:
                    print(f"  ERROR {office} ({contest_key}): No results found")
                    total_issues += 1
                    continue
                
                county_count = len(contest['results'])
                
                if county_count == 0:
                    print(f"  ERROR {office} ({contest_key}): 0 counties (EMPTY)")
                    total_issues += 1
                elif county_count < 87:
                    print(f"  WARN {office} ({contest_key}): {county_count}/87 counties (INCOMPLETE)")
                    total_issues += 1
                else:
                    print(f"  OK {office} ({contest_key}): {county_count}/87 counties")
                
                # Sample one county to check data quality
                sample_county = list(contest['results'].values())[0]
                
                # Check for essential fields
                if 'dem_votes' not in sample_county and 'rep_votes' not in sample_county:
                    print(f"    WARN Missing vote data in sample county")
                    total_issues += 1
                elif sample_county.get('dem_votes', 0) == 0 and sample_county.get('rep_votes', 0) == 0:
                    print(f"    WARN Zero votes in sample county")
                    total_issues += 1
        
        # Check for expected vs actual offices
        if year in expected_contests:
            expected = set(expected_contests[year])
            actual = set(actual_offices)
            
            missing = expected - actual
            extra = actual - expected
            
            if missing:
                print(f"\n  WARN Missing expected offices: {', '.join(sorted(missing))}")
                total_issues += len(missing)
            
            if extra:
                print(f"  INFO Extra offices (not expected): {', '.join(sorted(extra))}")
    
    # Summary
    print(f"\n{'='*80}")
    print(f"VERIFICATION SUMMARY")
    print(f"{'='*80}")
    print(f"Total years checked: {len(range(1990, 2026, 2))}")
    print(f"Total issues found: {total_issues}")
    
    if total_issues == 0:
        print("\nALL DATA VERIFICATION PASSED!")
    else:
        print(f"\n{total_issues} issues need attention")
    
    print("=" * 80)
    
    return total_issues

if __name__ == "__main__":
    verify_all_years()
