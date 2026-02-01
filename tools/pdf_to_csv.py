"""
PDF to CSV converter for election data
Extracts tabular data from PDF files and converts to CSV format
"""

import sys
import os

def extract_with_pdfplumber(pdf_path, output_csv):
    """Extract tables from PDF using pdfplumber"""
    try:
        import pdfplumber
    except ImportError:
        print("pdfplumber not installed. Installing...")
        os.system(f'"{sys.executable}" -m pip install pdfplumber')
        import pdfplumber
    
    import csv
    
    all_tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Processing {len(pdf.pages)} pages...")
        
        for i, page in enumerate(pdf.pages, 1):
            print(f"  Page {i}...")
            tables = page.extract_tables()
            
            if tables:
                for table in tables:
                    all_tables.extend(table)
    
    # Write to CSV
    if all_tables:
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(all_tables)
        
        print(f"\n✓ Successfully extracted {len(all_tables)} rows to {output_csv}")
        return True
    else:
        print("\n✗ No tables found in PDF")
        return False

def extract_with_tabula(pdf_path, output_csv):
    """Extract tables from PDF using tabula"""
    try:
        import tabula
    except ImportError:
        print("tabula-py not installed. Installing...")
        os.system(f'"{sys.executable}" -m pip install tabula-py')
        import tabula
    
    try:
        # Extract all tables from PDF
        dfs = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
        
        if dfs:
            # Combine all dataframes
            import pandas as pd
            combined_df = pd.concat(dfs, ignore_index=True)
            
            # Save to CSV
            combined_df.to_csv(output_csv, index=False)
            
            print(f"\n✓ Successfully extracted data to {output_csv}")
            print(f"  {len(combined_df)} rows, {len(combined_df.columns)} columns")
            return True
        else:
            print("\n✗ No tables found in PDF")
            return False
            
    except Exception as e:
        print(f"\n✗ Error with tabula: {e}")
        return False

if __name__ == "__main__":
    # PDF file path
    pdf_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\1990-11-06-g-sec.pdf"
    output_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\1990-11-06-g-sec.csv"
    
    if not os.path.exists(pdf_file):
        print(f"Error: PDF file not found at {pdf_file}")
        sys.exit(1)
    
    print(f"Converting PDF to CSV...")
    print(f"Input:  {pdf_file}")
    print(f"Output: {output_file}\n")
    
    # Try pdfplumber first (more reliable for complex PDFs)
    print("Method 1: Trying pdfplumber...")
    success = extract_with_pdfplumber(pdf_file, output_file)
    
    if not success:
        print("\nMethod 2: Trying tabula-py...")
        success = extract_with_tabula(pdf_file, output_file)
    
    if success:
        print("\n✓ Conversion complete!")
    else:
        print("\n✗ Conversion failed. You may need to extract the data manually.")
