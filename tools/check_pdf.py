"""
Improved PDF extractor for Minnesota 1990 election data
"""

import sys
import os

def check_pdf_content(pdf_path):
    """Check the content and structure of the PDF"""
    try:
        import pdfplumber
    except ImportError:
        print("Installing pdfplumber...")
        os.system(f'"{sys.executable}" -m pip install pdfplumber')
        import pdfplumber
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}\n")
        
        # Check first few pages
        for i in range(min(3, len(pdf.pages))):
            print(f"=== PAGE {i+1} ===")
            page = pdf.pages[i]
            
            # Extract text
            text = page.extract_text()
            if text:
                print("Text content (first 500 chars):")
                print(text[:500])
                print()
            
            # Check for tables
            tables = page.extract_tables()
            if tables:
                print(f"Found {len(tables)} table(s)")
                if tables[0]:
                    print("First table preview:")
                    for row in tables[0][:5]:  # First 5 rows
                        print(row)
            print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    pdf_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\1990-11-06-g-sec.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"Error: PDF file not found at {pdf_file}")
        sys.exit(1)
    
    print("Analyzing PDF structure...\n")
    check_pdf_content(pdf_file)
