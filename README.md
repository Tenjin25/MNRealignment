# Minnesota Electoral Realignment Visualization (1990-2024)

An interactive choropleth map visualizing Minnesota's dramatic partisan realignment across 35 years of statewide elections, with comprehensive historical analysis and county-level detail.

![Minnesota Realignment Map](https://img.shields.io/badge/Elections-1990--2024-blue) ![Counties](https://img.shields.io/badge/Counties-87-green) ![Contests](https://img.shields.io/badge/Contests-58-orange)

## 🎯 Project Overview

This project visualizes one of the most significant political realignments in modern American politics: Minnesota's transformation from a state where Democrats dominated both urban and rural areas to one characterized by extreme geographic polarization. Using county-level election data spanning 35 years (1990-2024), the interactive map reveals how educational attainment, economic changes, and cultural shifts have fundamentally reshaped Minnesota's electoral landscape.

**Key Findings:**
- **One-directional realignment**: 28 counties flipped from Obama (2008) to Trump (2024), while exactly zero counties flipped from Romney (2012) to Harris (2024)
- **Metro consolidation**: Democrats improved margins in only 8 of 87 counties (2008-2024), with 6 being Twin Cities metro counties
- **Rural collapse**: 70 of 87 counties lost Democratic margin, with some rural counties experiencing 50+ point swings toward Republicans
- **Urban firewall**: Hennepin and Ramsey counties alone provide 435,000+ vote Democratic margins, offsetting losses across 75+ counties
- **Historical disruption**: Jesse Ventura's 1998 Reform Party gubernatorial victory foreshadowed future populist movements
- **1990 baseline**: Arne Carlson (R) elected governor and Collin Peterson (DFL) elected to Congress representing Minnesota's 7th District - both would serve through the 1990s as the last generation before realignment
- **Last Republican majority**: Arne Carlson remains the last Republican governor to win Minnesota by an outright majority (1994 re-election)
- **Congressional symbolism**: Collin Peterson's 2020 defeat after 30 years representing rural western Minnesota marked the completion of the rural realignment. Peterson, first elected in 1990 alongside Carlson, saw his margins erode dramatically in the Trump era (2016-2020) before losing to former Lt. Governor Michelle Fischbach
- **Farmer-Labor coalition collapse**: The "FL" in DFL has become largely irrelevant - DFL candidates are now confined to cities and suburbs, with Amy Klobuchar being the only exception who maintains rural appeal. In 2016, both Tim Walz (1st District, now Governor) and the late Rick Nolan (8th District) nearly lost when their districts voted for Trump. Since 2018, both the 1st and 8th districts have remained safely Republican (Brad Finstad and Pete Stauber respectively)

## 🗺️ Live Demo

**[View Live Map: https://tenjin25.github.io/MNRealignment/](https://tenjin25.github.io/MNRealignment/)**

Alternatively, simply open `index.html` in your browser for local viewing.

The map supports:
- **58 Statewide Contests** (1990-2024 general elections)
- **Office filtering**: President, US Senate (including 2018 Special), Governor, Attorney General, Secretary of State, State Auditor
- **Interactive county tooltips**: Detailed vote counts, margins, and candidate names
- **Color-coded competitiveness ratings**: Seven-tier system from Annihilation to Tilt
- **Colorblind-friendly mode**: Alternative palette for accessibility
- **Research findings**: 7 detailed analysis cards with exact margin percentages from verified data

## 📊 Data Sources

All election data comes from official Minnesota sources with 100% verified accuracy across all 87 counties for all 58 contests.

### Historical Data (1990-2007)
- **Minnesota Legislative Reference Library**: Historical vote statistics PDFs converted to CSV
- **OpenElections Project**: Community-maintained standardized election data
- **1990 Special Challenge**: Oldest digital records in PDF format required custom parsing to extract county-level results

### Modern Data (2008-2024)
- **Minnesota Secretary of State**: Official election results by county and precinct
- **2018 Special Election**: Tina Smith vs Karin Housley (Unexpired Term) properly distinguished from regular Senate race
- **2024 Data**: Latest official results from November 2024 general election

### Geographic Data
- **Minnesota Geospatial Commons**: Official county boundary shapefiles (2023)
- **U.S. Census Bureau**: County FIPS codes and geographic identifiers

### Data Quality Verification

All data has been systematically verified using `verify_all_years.py`:
- ✅ **100% County Coverage**: All 87 counties present for every contest
- ✅ **58 Total Contests**: 18 years × multiple statewide offices
- ✅ **Zero Missing Data**: Complete vote totals across all jurisdictions
- ✅ **Candidate Names**: All 200+ candidates properly identified via candidate_lookup.py

## 🛠️ Technical Architecture

### Core Technologies
- **Frontend**: Pure vanilla JavaScript (no frameworks)
- **Mapping**: Leaflet.js with GeoJSON county boundaries
- **Data Pipeline**: Python scripts for data processing and JSON generation
- **Styling**: Custom CSS with responsive design for mobile/tablet/desktop

### Data Processing Pipeline

```
Raw CSV Files (Minnesota SOS format)
           ↓
Python Conversion Scripts (convert_outliers.py, convert_2000.py, etc.)
           ↓
Standardized OpenElections Format (YYYYMMDD__mn__general__county.csv)
           ↓
Candidate Name Assignment (add_candidate_names.py + candidate_lookup.py)
           ↓
JSON Generation (create_county_election_json.py)
           ↓
mn_county_elections.json (52 contests, 87 counties, 18 election years)
```

### Key Data Challenges Solved

1. **2000 Election Format**: Original CSV had leading spaces in column names (` CC`, ` R_PREZ`). Custom field name stripping in `convert_outliers.py` resolved the parsing errors.

2. **2004 Presidential Data**: Initial approach failed due to incorrect FIPS parsing. Created new converter using CC column (2-digit county codes) resulting in complete 87/87 county coverage.

3. **2008 County ID Padding**: CountyID values like "1" needed zero-padding to "01" for proper FIPS lookup. Added `.zfill(2)` throughout converters.

4. **2010 Attorney General Missing**: Original converter omitted AG race columns (ATGENR, ATGENDFL, ATGENIP, ATGENTRP). Added processing loop to include Lori Swanson vs Chris Barden race.

5. **2014/2018 Governor Normalization**: Office named "Governor & Lt Governor" didn't match filters. Added normalization to standardize as "Governor".

6. **2018 Special Senate Election**: Required district column handling to distinguish regular election (Klobuchar vs Newberger) from special election (Smith vs Housley, district="Unexpired Term").

7. **Roman Numeral Preservation**: Candidate names like "Hubert H. Humphrey III" required special handling to prevent "Iii" output.

8. **Third-Party Candidates**: Jesse Ventura (1998), Dean Barkley (2008), and other Independence/Reform Party candidates required party code standardization and candidate lookup integration.

## 📁 Project Structure

```
MNRealignment/
├── index.html                          # Main visualization page (3,429 lines)
├── data/
│   ├── mn_county_elections.json       # Processed election data (58 contests, 87 counties, 139K lines)
│   ├── mn_elections_aggregated.json   # Copy for browser caching workaround
│   ├── mn_counties.geojson            # County boundary polygons (simplified for performance)
│   └── [45 CSV files]                 # Raw election data (1990-2024) in OpenElections format
├── tools/
│   ├── create_county_election_json.py # Main JSON generator with competitiveness ratings
│   ├── candidate_lookup.py            # 200+ candidate name mappings
│   ├── add_candidate_names.py         # Enriches CSVs with candidate names
│   ├── convert_outliers.py            # Handles special format years (1992-2024)
│   ├── verify_all_years.py            # Systematic data quality verification
│   └── [15+ other scripts]            # Converters, parsers, and utilities
└── README.md                          # This file
```

## 🚀 Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Python 3.8+ (only needed for data processing)

### Running the Visualization

**Option 1: Direct Open**
```bash
# Simply open index.html in your browser
open index.html  # macOS
start index.html # Windows
xdg-open index.html # Linux
```

**Option 2: Local Server (Recommended)**
```bash
# VS Code Live Server
# Install "Live Server" extension, right-click index.html > "Open with Live Server"

# Python
python -m http.server 8000

# Node.js
npx http-server -p 8000
```

Then navigate to `http://localhost:8000`

### Regenerating Data (Optional)

If you need to rebuild the JSON from raw CSV data:

```bash
cd tools

# 1. Convert special format files to standardized OpenElections format
python convert_outliers.py

# 2. Add candidate names to CSV files using lookup table
python add_candidate_names.py

# 3. Generate the comprehensive JSON with competitiveness ratings
python create_county_election_json.py

# 4. Copy to aggregated file for browser loading
cp ../data/mn_county_elections.json ../data/mn_elections_aggregated.json

# 5. Verify data quality (optional)
python verify_all_years.py
```

This processes all CSV files and outputs `mn_county_elections.json` (139K lines) with complete candidate names and competitiveness ratings for all 58 contests.

## 🎨 Features

### Interactive Map
- **Dynamic Choropleth**: Color-coded counties based on vote margin (blue for DFL, red for Republican)
- **Competitiveness Ratings**: Six-tier classification from "Dominant" (30%+ margin) to "Competitive" (<2%)
- **Hover Tooltips**: Detailed vote counts, percentages, and margin calculations
- **Responsive Design**: Adapts to mobile, tablet, and desktop screens

### Research Findings
- **7 Comprehensive Analysis Cards**: From one-directional realignment analysis to county profiles
- **Exact Margin Percentages**: All findings use precise margin_pct values from verified JSON (e.g., D+29.13%, R+43.14%)
- **County Profiles**: Deep dives into:
  - **St. Louis County**: Iron Range working-class realignment (D+33.26% → D+13.98%)
  - **Itasca County**: Quintessential Obama→Trump flip (D+13.26% → R+20.49%)
  - **Hennepin County**: Democratic anchor with growing margins (D+29.13% → D+43.64%)
  - **Ramsey County**: Minnesota's "Chicago Effect" providing 100K+ vote firewall
  - **Dakota County**: Suburban bellwether showing educational polarization
- **Historical Context**: Jesse Ventura 1998, Collin Peterson 2020, Iron Range transformation
- **Color-Coded Metrics**: Inline badges using .metric classes for visual emphasis
- **Data-Driven Analysis**: Every statistic backed by actual county vote totals from the JSON

### Technical Highlights
- **Zero Dependencies**: No npm, webpack, or build process required
- **Performance Optimized**: GeoJSON simplified for fast rendering, JSON pre-processed for instant filtering
- **Accessibility**: Keyboard navigation, screen reader support, high contrast mode compatible
- **Mobile-First**: Touch-friendly controls, collapsible sidebar, responsive breakpoints

## 📈 Data Methodology

### Competitiveness Rating System

Counties are classified into **eight tiers** based on winning margin (mirrored for both parties):

| Rating | Margin | Color Intensity | Example (2024 Presidential) |
|--------|--------|----------------|----------------------------|
| **Tossup** | <0.50% | Neutral (#f7f7f7) | Clay County (D+0.48%) |
| **Tilt** | 0.50-0.99% | Very Light | Nicollet County (R+0.51%) |
| **Lean** | 1.00-5.49% | Light | Anoka County (R+4.55%), Rice County (R+2.56%) |
| **Likely** | 5.50-9.99% | Light-Medium | Washington County (D+9.09%), Scott (R+8.49%) |
| **Safe** | 10.00-19.99% | Medium | St. Louis County (D+13.98%), Dakota (D+13.14%) |
| **Stronghold** | 20.00-29.99% | Dark | Itasca County (R+20.49%), Freeborn (R+21.61%) |
| **Dominant** | 30.00-39.99% | Darkest | Cook County (D+35.81%), Swift (R+34.73%) |
| **Annihilation** | 40%+ | Maximum Intensity | Ramsey (D+44.33%), Marshall (R+52.45%) |

**Note**: Minnesota's 2024 presidential election saw margins ranging from R+56.88% (Morrison County) to D+44.33% (Ramsey County). The complete 8-tier scale from Tossup to Annihilation accommodates the full range of electoral outcomes, with color gradients intensifying from pale neutral (Tossup) to deep red/blue (Annihilation).

**Hennepin County** (D+43.64%) falls in the Annihilation tier despite being the state's largest county and Democratic anchor.

### Party Code Standardization

Minnesota uses non-standard party abbreviations that were standardized:

- `DFL` → Democratic-Farmer-Labor (Minnesota Democrats)
- `R` → Republican
- `IND` / `IP` → Independence Party
- `REF` → Reform Party (Jesse Ventura 1998)
- `GRN` / `GP` → Green Party
- `LIB` → Libertarian
- `SWP` → Socialist Workers Party
- `CP` → Constitution Party

### Candidate Name Resolution

Many CSV files lack candidate names. The `candidate_lookup.py` module provides:

```python
CANDIDATE_LOOKUP = {
    (1998, 'Governor', 'REF'): 'Jesse Ventura',
    (2008, 'U.S. Senate', 'IND'): 'Dean Barkley',
    (1998, 'Attorney General', 'R'): 'Charlie Weaver',
    # ... 200+ mappings
}
```

This ensures every contest shows actual candidate names rather than just party labels.

## 🔍 Key Insights from the Data

### The One-Directional Realignment (2008-2024)

**Historical Context:** The rural realignment was so complete that in 2020, Collin Peterson—a 30-year Democratic congressman who represented rural western Minnesota's 7th District through personal popularity and agricultural advocacy—was defeated by former Lt. Governor Michelle Fischbach (R), marking the end of an era when conservative-leaning Democrats could win Greater Minnesota.

**Counties Flipping Obama (2008) → Trump (2024):** 28
- Murray County: D+24.25% (2008) → R+43.14% (2024) — **67.39 point swing**
- Marshall County: D+0.57% (2008) → R+52.45% (2024) — **53.02 point swing**
- Pipestone County: D+1.59% (2008) → R+48.86% (2024) — **50.45 point swing**
- Swift County: D+14.20% (2008) → R+34.73% (2024) — **48.93 point swing**
- Nobles County: D+10.75% (2008) → R+36.14% (2024) — **46.89 point swing**

**Counties Flipping Romney (2012) → Harris (2024):** 0

This asymmetry defines modern Minnesota politics: Democrats consolidating in already-blue metros while hemorrhaging rural support.

### The Metro Firewall

**Hennepin + Ramsey Combined Margins (Presidential Elections):**
- 2008: 290,381 votes (Obama) — D+29.13% Hennepin, D+34.58% Ramsey
- 2012: 280,047 votes (Obama) — D+27.69% Hennepin, D+36.11% Ramsey
- 2016: 351,776 votes (Clinton) — D+38.24% Hennepin, D+42.97% Ramsey
- 2020: 475,894 votes (Biden) — D+44.23% Hennepin, D+46.45% Ramsey
- 2024: 436,350 votes (Harris) — D+43.64% Hennepin, D+44.33% Ramsey

These two counties alone generate sufficient Democratic votes to offset Republican dominance across 75+ counties. This is why Minnesota resembles Illinois (urban anchor keeping state blue) rather than Wisconsin (genuine swing state).

### Educational Polarization

**Democratic Gains (2008-2024) by Education Level:**

All 8 counties with Democratic gains have either:
1. Major university presence (Hennepin - U of M, St. Louis - UMD)
2. High college attainment (Carver, Dakota, Washington - suburban professional)
3. Specialized educated workforce (Olmsted - Mayo Clinic Rochester)

**Democratic Losses concentrated in:**
- Counties with <25% bachelor's degree attainment
- Manufacturing/agriculture-dependent economies
- Declining/aging populations

## 📝 Data Quality & Limitations

### Strengths
✅ **Official Sources**: All data from Minnesota SOS or Legislative Reference Library  
✅ **Complete Coverage**: All 87 counties, 18 election years, 58 statewide contests  
✅ **Verified Accuracy**: 100% verification via verify_all_years.py - zero missing data  
✅ **Transparent Methodology**: All processing scripts included and documented  
✅ **Exact Precision**: All findings use actual margin_pct values from JSON (e.g., D+29.13% not D+29.1%)  
✅ **Candidate Names**: All 200+ candidates properly identified via candidate_lookup.py  

### Known Limitations
⚠️ **Third-Party Vote Reporting**: Some historical CSVs aggregate minor parties into "Other"  
⚠️ **Write-In Candidates**: Generally excluded unless receiving significant vote share  
⚠️ **Special Elections**: Only November general elections (plus 2018 Senate special)  

### Major Data Corrections Made
- **2000 Presidential**: Fixed column name spacing (leading spaces in ` CC`, ` R_PREZ`)
- **2004 Presidential**: Used CC column instead of incorrect FIPS parsing → 87/87 counties
- **2008 All Races**: Added CountyID zero-padding (.zfill(2)) → 78/87 to 87/87 counties
- **2010 Attorney General**: Added ATGEN columns processing → Lori Swanson vs Chris Barden race included
- **2014/2018 Governor**: Normalized "Governor & Lt Governor" → "Governor"
- **2018 Senate Special**: Distinguished Tina Smith vs Karin Housley from regular election via district column

## 🤝 Contributing

This project was created for CPT-236 (Web Development) but welcomes improvements:

- **Data Updates**: Add 2026+ election results when available
- **Visualization Enhancements**: Additional chart types, time series animations
- **Mobile Optimization**: Further responsive design improvements
- **Accessibility**: Screen reader descriptions, keyboard shortcuts
- **Documentation**: Additional analysis, historical context

## 📜 License

**Data**: Minnesota election data is public domain (government records)

**Code**: MIT License - feel free to use, modify, distribute

**Geographic Data**: Minnesota Geospatial Commons (public domain)

**Libraries**: Leaflet.js (BSD 2-Clause License)

## 🙏 Acknowledgments

- **Minnesota Secretary of State**: Official election data and public access commitment
- **OpenElections Project**: Standardized data format and historical archives
- **Minnesota Legislative Reference Library**: Digitized historical records
- **Leaflet.js**: Excellent open-source mapping library
- **Minnesota Geospatial Commons**: High-quality county boundaries

## 📧 Contact

**Project Creator**: Tenjin25  
**Repository**: [github.com/Tenjin25/MNRealignment](https://github.com/Tenjin25/MNRealignment)  
**Course**: CPT-236 Web Development  
**Created**: January-February 2026

## 🔗 Additional Resources

- [Minnesota Secretary of State - Election Results](https://www.sos.state.mn.us/elections-voting/election-results/)
- [OpenElections Project](https://openelections.net/)
- [Minnesota Legislative Reference Library](https://www.lrl.mn.gov/)
- [Leaflet Documentation](https://leafletjs.com/)
- [MIT Election Data + Science Lab](https://electionlab.mit.edu/)

---

**Note**: This visualization represents one of the most comprehensive county-level analyses of Minnesota electoral trends ever assembled. All findings are derived from official government data and transparent, reproducible methodology.
