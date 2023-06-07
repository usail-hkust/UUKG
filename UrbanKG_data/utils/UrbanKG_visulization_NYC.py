"""

Visualize the distribution of borough, area, road, POI
Save to the current folder:
    borough.html
    area.html
    road.html
    POI.html
"""
from shapely import wkt
from tqdm import tqdm
import geopandas as gpd
import pandas as pd
import folium
import re
from shapely.geometry import MultiPolygon
import numpy as np
from shapely.geometry import Point
from folium.plugins import HeatMap
from folium.features import GeoJson

dataframe1 = gpd.read_file('../Meta_data/NYC/Administrative_data/Borough/Borough.shp')

dataframe1 = dataframe1.to_crs('EPSG:4326')
seleceted_colums1 = ['BoroCode', 'BoroName', 'geometry']
borough_dataframe = dataframe1[seleceted_colums1]
######################################
dataframe2 = gpd.read_file('../Meta_data/NYC/Administrative_data/Area/Area.shp')

dataframe2 = dataframe2.to_crs('EPSG:4326')
seleceted_colums2 = ['OBJECTID', 'zone', 'geometry']
area_dataframe = dataframe2[seleceted_colums2]
## filter
area_dataframe = area_dataframe[area_dataframe['OBJECTID'] != 1]
area_dataframe = area_dataframe[area_dataframe['OBJECTID'] != 103]
area_dataframe = area_dataframe[area_dataframe['OBJECTID'] != 104]

################### borough #######################
m_borough = folium.Map(location=[40.70, -74.00], zoom_start=10, tiles="cartodbpositron")

geojson_borough = GeoJson(data=borough_dataframe.__geo_interface__,
                  style_function=lambda feature: {
                      'color': 'DarkBlue',
                      'weight': 2,
                      'fillOpacity': 0
                  })

geojson_borough.add_to(m_borough)


m_borough.save('borough_NYC.html')

############################### area ################################
m_area = folium.Map(location=[40.70, -74.00], zoom_start=10, tiles="cartodbpositron")

geojson_area = GeoJson(data=area_dataframe.__geo_interface__,
                  style_function=lambda feature: {
                      'color': 'DarkBlue',
                      'weight': 2,
                      'fillOpacity': 0
                  })

geojson_area.add_to(m_area)


m_area.save('area_NYC.html')

########################################## road ################
road_dataframe = pd.read_csv('../Processed_data/NYC/NYC_road.csv')
road_datanumpy = road_dataframe[['geometry', 'link_type']].values
junction_dataframe =  pd.read_csv('../Processed_data/NYC/NYC_junction.csv')

m_road = folium.Map(location=[40.70, -74.00], zoom_start=10, tiles="cartodbpositron")

color = {1: 'DarkBlue', 2: 'DarkOrange', 3: 'Green', 4: 'Purple', 5:'DeepSkyBlue', 6:'LightSlateGray'}
weight = {1: 4, 2: 2.5, 3: 2, 4: 1.2, 5: 0.7, 6:0.2}

def get_loc(node_df, node_id):
    df = node_df[node_df.node_id == node_id]
    return [df.lng.values[0], df.lat.values[0]]


total_link = road_dataframe.shape[0]
for i in tqdm(range(total_link)):
    from_node_id = road_dataframe.iloc[i].from_node_id
    to_node_id = road_dataframe.iloc[i].to_node_id
    try:
        from_loc = get_loc(junction_dataframe, from_node_id)
        to_loc = get_loc(junction_dataframe, to_node_id)
    except:
        continue
    type = road_dataframe.iloc[i].link_type
    color_selcet = color[type]
    if type == 1:
        folium.PolyLine(locations=[from_loc, to_loc], weight=4, color = color_selcet, no_clip=True).add_to(m_road)
    if type == 2:
        folium.PolyLine(locations=[from_loc, to_loc], weight=2.5, color = color_selcet, no_clip=True).add_to(m_road)
    if type == 3:
        folium.PolyLine(locations=[from_loc, to_loc], weight=2, color = color_selcet, no_clip=True).add_to(m_road)
    if type == 4:
        folium.PolyLine(locations=[from_loc, to_loc], weight=1.2, color = color_selcet, no_clip=True).add_to(m_road)
    if type == 5:
        folium.PolyLine(locations=[from_loc, to_loc], weight=0.7, color = color_selcet, no_clip=True).add_to(m_road)
    if type == 6:
        folium.PolyLine(locations=[from_loc, to_loc], weight=0.2, color = color_selcet, no_clip=True).add_to(m_road)


m_road.save('road_NYC.html')

########################################## POI ################
POI_dataframe = pd.read_csv('../Processed_data/NYC/NYC_poi.csv')


m_POI = folium.Map(location=[40.70, -74.00], zoom_start=10, tiles="cartodbpositron")


for index, row in POI_dataframe.iterrows():

    folium.CircleMarker(location=[row['lat'], row['lng']], radius=1, fill=True, fill_opacity=0,
                        color = 'DarkBlue', weight = 1).add_to(m_POI)

# Save the map as an HTML file
m_POI.save('POI_NYC.html')

########################################## POI ################
Junction_dataframe = pd.read_csv('../Processed_data/NYC/NYC_junction.csv')

#
m_Junction = folium.Map(location=[40.70, -74.00], zoom_start=10, tiles="cartodbpositron")

#
for index, row in Junction_dataframe.iterrows():

    folium.RegularPolygonMarker(location=[row['lng'], row['lat']], radius=0.1, min_size=0.1, fill=True, fill_opacity=0,
                        color = 'DarkBlue',).add_to(m_Junction)


m_Junction.save('Junction_NYC.html')