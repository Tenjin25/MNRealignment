"""
Convert Minnesota county shapefile to GeoJSON format
"""

import geopandas as gpd
import json

def convert_shapefile_to_geojson():
    """Convert the MN county shapefile to GeoJSON"""
    
    # Input shapefile path
    shapefile_path = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data\tl_2020_27_county20\tl_2020_27_county20.shp"
    
    # Output GeoJSON path - use same base name as shapefile
    import os
    base_name = os.path.splitext(os.path.basename(shapefile_path))[0]
    data_dir = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\MNRealignment\data"
    output_path = os.path.join(data_dir, f"{base_name}.geojson")
    
    print(f"Reading shapefile: {shapefile_path}")
    
    # Read the shapefile
    gdf = gpd.read_file(shapefile_path)
    
    # Display information about the data
    print(f"\nShapefile loaded successfully!")
    print(f"  - Number of counties: {len(gdf)}")
    print(f"  - CRS: {gdf.crs}")
    print(f"\nColumns: {list(gdf.columns)}")
    
    # Show first few rows
    print(f"\nFirst few counties:")
    print(gdf[['NAME20', 'COUNTYFP20']].head())
    
    # Convert to GeoJSON (WGS84 is standard for web mapping)
    print(f"\nConverting to GeoJSON (EPSG:4326)...")
    gdf_wgs84 = gdf.to_crs(epsg=4326)
    
    # Save as GeoJSON
    gdf_wgs84.to_file(output_path, driver='GeoJSON')
    
    print(f"\n✓ GeoJSON saved to: {output_path}")
    print(f"  - {len(gdf_wgs84)} counties")
    print(f"  - CRS: {gdf_wgs84.crs}")
    
    # Create a simplified version with just essential properties
    simplified_output = output_path.replace('.geojson', '_simplified.geojson')
    
    # Keep only essential columns
    essential_columns = ['NAME20', 'COUNTYFP20', 'GEOID20', 'geometry']
    available_columns = [col for col in essential_columns if col in gdf_wgs84.columns]
    gdf_simplified = gdf_wgs84[available_columns].copy()
    
    # Rename columns to remove the "20" suffix
    gdf_simplified = gdf_simplified.rename(columns={
        'NAME20': 'name',
        'COUNTYFP20': 'county_code',
        'GEOID20': 'geoid'
    })
    
    gdf_simplified.to_file(simplified_output, driver='GeoJSON')
    print(f"\n✓ Simplified GeoJSON saved to: {simplified_output}")
    
    return output_path

if __name__ == "__main__":
    print("="*60)
    print("Converting Minnesota County Shapefile to GeoJSON")
    print("="*60 + "\n")
    
    convert_shapefile_to_geojson()
    
    print("\n" + "="*60)
    print("Conversion complete!")
    print("="*60)
