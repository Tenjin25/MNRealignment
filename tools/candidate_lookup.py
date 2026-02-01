"""
Candidate lookup table for Minnesota elections 1992-2010
Maps (year, office, party) to candidate names
"""

CANDIDATES = {
    # 1992
    (1992, 'President', 'R'): 'George H.W. Bush',
    (1992, 'President', 'DFL'): 'Bill Clinton',
    (1992, 'President', 'Other'): 'Ross Perot',
    (1992, 'U.S. Senate', 'R'): 'Rod Grams',
    (1992, 'U.S. Senate', 'DFL'): 'Paul Wellstone',
    
    # 1994
    (1994, 'Governor', 'R'): 'Arne Carlson',
    (1994, 'Governor', 'DFL'): 'John Marty',
    (1994, 'U.S. Senate', 'R'): 'Rod Grams',
    (1994, 'U.S. Senate', 'DFL'): 'Ann Wynia',
    (1994, 'Secretary of State', 'R'): 'Joanell Dyrstad',
    (1994, 'Secretary of State', 'DFL'): 'John Lindner',
    (1994, 'Attorney General', 'R'): 'Mike Hatch',
    (1994, 'Attorney General', 'DFL'): 'Hubert H. Humphrey III',
    (1994, 'State Auditor', 'R'): 'Judi Dutcher',
    (1994, 'State Auditor', 'DFL'): 'Mark Dayton',
    (1994, 'State Treasurer', 'R'): 'Mike McGrath',
    (1994, 'State Treasurer', 'DFL'): 'Michael McGrath',
    
    # 1996
    (1996, 'President', 'R'): 'Bob Dole',
    (1996, 'President', 'DFL'): 'Bill Clinton',
    (1996, 'President', 'RP'): 'Ross Perot',
    (1996, 'President', 'Other'): 'Other',
    (1996, 'U.S. Senate', 'R'): 'Rudy Boschwitz',
    (1996, 'U.S. Senate', 'DFL'): 'Paul Wellstone',
    
    # 1998
    (1998, 'Governor', 'R'): 'Norm Coleman',
    (1998, 'Governor', 'DFL'): 'Hubert H. Humphrey III',
    (1998, 'Governor', 'RP'): 'Jesse Ventura',
    (1998, 'Secretary of State', 'R'): 'Mary Kiffmeyer',
    (1998, 'Secretary of State', 'DFL'): 'Mark Ritchie',
    (1998, 'Attorney General', 'R'): 'Charlie Weaver',
    (1998, 'Attorney General', 'DFL'): 'Mike Hatch',
    (1998, 'State Auditor', 'R'): 'Mark Ourada',
    (1998, 'State Auditor', 'DFL'): 'Judi Dutcher',
    (1998, 'State Treasurer', 'R'): 'Mark Meierhenry',
    (1998, 'State Treasurer', 'DFL'): 'Carol Johnson',
    
    # 2000
    (2000, 'President', 'R'): 'George W. Bush',
    (2000, 'President', 'DFL'): 'Al Gore',
    (2000, 'President', 'GP'): 'Ralph Nader',
    (2000, 'President', 'LIB'): 'Harry Browne',
    (2000, 'President', 'RP'): 'Pat Buchanan',
    (2000, 'President', 'Other'): 'Other',
    (2000, 'U.S. Senate', 'R'): 'Rod Grams',
    (2000, 'U.S. Senate', 'DFL'): 'Mark Dayton',
    (2000, 'U.S. Senate', 'IND'): 'Jim Gibson',
    
    # 2002
    (2002, 'Governor', 'R'): 'Tim Pawlenty',
    (2002, 'Governor', 'DFL'): 'Roger Moe',
    (2002, 'Governor', 'IND'): 'Tim Penny',
    (2002, 'U.S. Senate', 'R'): 'Norm Coleman',
    (2002, 'U.S. Senate', 'DFL'): 'Walter Mondale',
    (2002, 'U.S. Senate', 'IND'): 'Jim Moore',
    (2002, 'Secretary of State', 'R'): 'Mary Kiffmeyer',
    (2002, 'Secretary of State', 'DFL'): 'Deborah L. Anderson',
    (2002, 'Attorney General', 'R'): 'Mike Hatch',
    (2002, 'Attorney General', 'DFL'): 'Mike Hatch',
    (2002, 'State Auditor', 'R'): 'Patricia Anderson Awada',
    (2002, 'State Auditor', 'DFL'): 'Judi Dutcher',
    
    # 2004
    (2004, 'President', 'R'): 'George W. Bush',
    (2004, 'President', 'DFL'): 'John Kerry',
    (2004, 'President', 'IND'): 'Ralph Nader',
    (2004, 'President', 'GP'): 'David Cobb',
    (2004, 'President', 'LIB'): 'Michael Badnarik',
    
    # 2006
    (2006, 'Governor', 'R'): 'Tim Pawlenty',
    (2006, 'Governor', 'DFL'): 'Mike Hatch',
    (2006, 'Governor', 'IND'): 'Peter Hutchinson',
    (2006, 'U.S. Senate', 'R'): 'Mark Kennedy',
    (2006, 'U.S. Senate', 'DFL'): 'Amy Klobuchar',
    (2006, 'U.S. Senate', 'IND'): 'Robert Fitzgerald',
    (2006, 'Secretary of State', 'R'): 'Mary Kiffmeyer',
    (2006, 'Secretary of State', 'DFL'): 'Mark Ritchie',
    (2006, 'Secretary of State', 'IND'): 'Independence Party',
    (2006, 'Attorney General', 'R'): 'Jeff Johnson',
    (2006, 'Attorney General', 'DFL'): 'Lori Swanson',
    (2006, 'Attorney General', 'IND'): 'Independence Party',
    (2006, 'State Auditor', 'R'): 'Patricia Anderson Awada',
    (2006, 'State Auditor', 'DFL'): 'Rebecca Otto',
    (2006, 'State Auditor', 'IND'): 'Lucy Gerold',
    
    # 2008
    (2008, 'President', 'R'): 'John McCain',
    (2008, 'President', 'DFL'): 'Barack Obama',
    (2008, 'President', 'IND'): 'Ralph Nader',
    (2008, 'President', 'GP'): 'Cynthia McKinney',
    (2008, 'President', 'LIB'): 'Bob Barr',
    (2008, 'U.S. Senate', 'R'): 'Norm Coleman',
    (2008, 'U.S. Senate', 'DFL'): 'Al Franken',
    (2008, 'U.S. Senate', 'IND'): 'Dean Barkley',
    
    # 2010
    (2010, 'Governor', 'R'): 'Tom Emmer',
    (2010, 'Governor', 'DFL'): 'Mark Dayton',
    (2010, 'Governor', 'IND'): 'Tom Horner',
    (2010, 'Attorney General', 'R'): 'Chris Barden',
    (2010, 'Attorney General', 'DFL'): 'Lori Swanson',
    (2010, 'Secretary of State', 'R'): 'Dan Severson',
    (2010, 'Secretary of State', 'DFL'): 'Mark Ritchie',
    (2010, 'State Auditor', 'R'): 'Pat Anderson',
    (2010, 'State Auditor', 'DFL'): 'Rebecca Otto',
    
    # 2024
    (2024, 'President', 'R'): 'Donald Trump',
    (2024, 'President', 'DFL'): 'Kamala Harris',
    (2024, 'President', 'LIB'): 'Chase Oliver',
    (2024, 'President', 'WTP'): 'Cornel West',
    (2024, 'President', 'G'): 'Jill Stein',
    (2024, 'President', 'SLP'): 'Claudia De la Cruz',
    (2024, 'President', 'SWP'): 'Rachele Fruit',
    (2024, 'President', 'JFA'): 'Robert F. Kennedy Jr.',
    (2024, 'President', 'IND'): 'Other Independent',
    (2024, 'U.S. Senate', 'R'): 'Royce White',
    (2024, 'U.S. Senate', 'DFL'): 'Amy Klobuchar',
    (2024, 'U.S. Senate', 'LIB'): 'Rebecca Whiting',
    (2024, 'U.S. Senate', 'IA'): 'Steve Carlson',
}

def get_candidate_name(year, office, party):
    """Get candidate name for a given year, office, and party"""
    # Normalize office names
    office_map = {
        'President': 'President',
        'U.S. Senate': 'U.S. Senate',
        'Governor': 'Governor',
        'Secretary of State': 'Secretary of State',
        'Attorney General': 'Attorney General',
        'State Auditor': 'State Auditor',
    }
    
    office = office_map.get(office, office)
    key = (year, office, party)
    
    return CANDIDATES.get(key, '')
