"""

save processed dta to ./processed_data:
    borough.csv: borough_id, borough_name, borough_polygon
    area.csv: area_id, area_name, area_polygon
    poi.csv: poi_id, poi_name, poi_category, lat, lng, borough_id, area_id
    road.csv: road_id, road_name, road_category, from_junction, to_junction, road_polygon, lat, lng, borough_id, area_id
    junction.csv: junction_id, junction_catogory, lat, lng, borough_id, area_id

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
"""
    
    borough, area  multi-polygon 
    
"""

######################################
dataframe1 = gpd.read_file('./Meta_data/NYC/Administrative_data/Borough/Borough.shp')
#
dataframe1 = dataframe1.to_crs('EPSG:4326')
seleceted_colums1 = ['BoroCode', 'BoroName', 'geometry']
borough_dataframe = dataframe1[seleceted_colums1]
borough_dataframe.to_csv('./Processed_data/NYC/NYC_borough.csv')
######################################
dataframe2 = gpd.read_file('./Meta_data/NYC/Administrative_data/Area/Area.shp')
#
dataframe2 = dataframe2.to_crs('EPSG:4326')
seleceted_colums2 = ['OBJECTID', 'zone', 'geometry']
area_dataframe = dataframe2[seleceted_colums2]
##
area_dataframe = area_dataframe[area_dataframe['OBJECTID'] != 1]
area_dataframe = area_dataframe[area_dataframe['OBJECTID'] != 103]
area_dataframe = area_dataframe[area_dataframe['OBJECTID'] != 104]
area_dataframe.to_csv('./Processed_data/NYC/NYC_area.csv')
######################################

"""

    POI align to borough, area

"""
poi_dataframe = pd.read_csv('./Meta_data/NYC/POI/poi_filter.csv')
poi_datanumpy = poi_dataframe[['lng', 'lat']].values

# borough, area
poi_borough_area_id = np.full((poi_datanumpy.shape[0], 2), 999)

for i in tqdm(range(poi_datanumpy.shape[0])):
    poi_point = Point(poi_datanumpy[i][0], poi_datanumpy[i][1])
    ##  borough
    for j in range(borough_dataframe.shape[0]):
        borough_polygon = borough_dataframe.iloc[j].geometry
        if borough_polygon.contains(poi_point):
            poi_borough_area_id[i][0] = borough_dataframe.iloc[j].BoroCode
            break
    ##  area
    for k in range(area_dataframe.shape[0]):
        area_polygon = area_dataframe.iloc[k].geometry
        if area_polygon.contains(poi_point):
            poi_borough_area_id[i][1] = area_dataframe.iloc[k].OBJECTID
            break

# add dataframe, filter
poi_dataframe[['borough_id', 'area_id']] = poi_borough_area_id
poi_dataframe = poi_dataframe[ (poi_dataframe['borough_id'] != 999)]
poi_dataframe = poi_dataframe[ (poi_dataframe['area_id'] != 999)]

poi_dataframe.to_csv('./Processed_data/NYC/NYC_poi.csv')

######################################
"""

    road align borough, area, 

"""
road_dataframe = pd.read_csv('./Meta_data/NYC/RoadNetwork/road_filter.csv')
road_datanumpy = road_dataframe[['geometry']].values

# borough, area
road_borough_area_id = np.full((road_datanumpy.shape[0], 2), 999)
for i in tqdm(range(road_datanumpy.shape[0])):
    road_linestring = wkt.loads(str(road_datanumpy[i][0]))
    ##  borough
    for j in range(borough_dataframe.shape[0]):
        borough_polygon = borough_dataframe.iloc[j].geometry
        if borough_polygon.contains(road_linestring) or borough_polygon.touches(road_linestring):
            road_borough_area_id[i][0] = borough_dataframe.iloc[j].BoroCode
            break
    ##  area
    for j in range(area_dataframe.shape[0]):
        area_polygon = area_dataframe.iloc[j].geometry
        if area_polygon.contains(road_linestring) or area_polygon.touches(road_linestring):
            road_borough_area_id[i][1] = area_dataframe.iloc[j].OBJECTID
            break
# filter
road_dataframe[['borough_id', 'area_id']] = road_borough_area_id
road_dataframe = road_dataframe[(road_dataframe['borough_id'] != 999)]
road_dataframe = road_dataframe[(road_dataframe['area_id'] != 999)]

road_dataframe.to_csv('./Processed_data/NYC/NYC_road.csv')

######################################
"""

    junction align borough, area

"""
junction_dataframe = pd.read_csv('./Meta_data/NYC/RoadNetwork/node_filter.csv')
junction_datanumpy = junction_dataframe[['lat', 'lng']].values

# borough, area
junction_borough_area_id = np.full((junction_datanumpy.shape[0], 2), 999)

for i in tqdm(range(junction_datanumpy.shape[0])):
    junction_point = Point(junction_datanumpy[i][0], junction_datanumpy[i][1])
    ##  borough
    for j in range(borough_dataframe.shape[0]):
        borough_polygon = borough_dataframe.iloc[j].geometry
        if borough_polygon.contains(junction_point):
            junction_borough_area_id[i][0] = borough_dataframe.iloc[j].BoroCode
            break
    ##  area
    for k in range(area_dataframe.shape[0]):
        area_polygon = area_dataframe.iloc[k].geometry
        if area_polygon.contains(junction_point):
            junction_borough_area_id[i][1] = area_dataframe.iloc[k].OBJECTID
            break

# filter
junction_dataframe[['borough_id', 'area_id']] = junction_borough_area_id
junction_dataframe = junction_dataframe[ (junction_dataframe['borough_id'] != 999)]
junction_dataframe = junction_dataframe[ (junction_dataframe['area_id'] != 999)]

junction_dataframe.to_csv('./Processed_data/NYC/NYC_junction.csv')