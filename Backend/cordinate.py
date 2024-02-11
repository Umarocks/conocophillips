# import geopandas as gpd

# # Assuming you have a GeoDataFrame with a column 'geometry' containing MULTIPOLYGON geometries
# gdf = gpd.read_file('./USOilGasAggregation.gpkg')

# # Convert the 'geometry' column to latitude and longitude
# gdf['latitude'] = gdf['geometry'].centroid.y
# gdf['longitude'] = gdf['geometry'].centroid.x

# # Print the resulting DataFrame
# print(gdf[['latitude', 'longitude']])



from shapely.geometry import MultiPolygon
from pyproj import Proj, transform

# Example multipolygon in a projected coordinate system
multipolygon_str = "[[[-373368.5547000002 -473148.0822999999, -370149.86030000076 -473148.0822999999, -370149.86030000076 -469929.38790000044, -373368.5547000002 -469929.38790000044, -373368.5547000002 -473148.0822999999]]]"

# Parse the WKT string to a Shapely MultiPolygon object
multipolygon = MultiPolygon([MultiPolygon([tuple(map(float, point.split())) for point in polygon[1:-1].split(', ')]) for polygon in multipolygon_str[13:-3].split('), (')])

# Define the source and target coordinate systems using EPSG codes
source_crs = Proj(init='epsg:3857')  # UTM Zone 13N for West Texas # Replace 'your_source_epsg_code' with the actual EPSG code of your source coordinate system
target_crs = Proj(init='epsg:4326')  # EPSG code for WGS 84, the coordinate system used for latitude and longitude

# Perform the coordinate transformation
transformed_multipolygon = MultiPolygon(
    [MultiPolygon([transform(source_crs, target_crs, x, y) for x, y in polygon.exterior.coords]) for polygon in multipolygon]
)

# Display the result
print(transformed_multipolygon)

