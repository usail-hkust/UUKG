"""

可视化 borough, area, road, POI的分布
存储至当前文件夹下：
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
from folium.features import GeoJson
# 读取数据
dataframe1 = gpd.read_file('../Meta_data/CHI/Administrative_data/Borough/Borough.shp')
# 转换为经纬度坐标系
dataframe1 = dataframe1.to_crs('EPSG:4326')
seleceted_colums1 = ['BoroCode', 'BoroName', 'geometry']
borough_dataframe = dataframe1[seleceted_colums1]
######################################
dataframe2 = gpd.read_file('../Meta_data/CHI/Administrative_data/Area/Area.shp')
# 转换为经纬度坐标系
dataframe2 = dataframe2.to_crs('EPSG:4326')
seleceted_colums2 = ['area_numbe', 'community', 'geometry']
area_dataframe = dataframe2[seleceted_colums2]

# ################### borough #######################
# m_borough = folium.Map(location=[41.80, -87.80], zoom_start=10, tiles="cartodbpositron")
#
# geojson_borough = GeoJson(data=borough_dataframe.__geo_interface__,
#                   style_function=lambda feature: {
#                       'color': 'DarkBlue',
#                       'weight': 2,
#                       'fillOpacity': 0
#                   })
#
# geojson_borough.add_to(m_borough)
#
# # 保存地图为HTML文件
# m_borough.save('borough_CHI.html')
#
# ############################### area ################################
# m_area = folium.Map(location=[41.80, -87.80], zoom_start=10, tiles="cartodbpositron")
#
# geojson_area = GeoJson(data=area_dataframe.__geo_interface__,
#                   style_function=lambda feature: {
#                       'color': 'DarkBlue',
#                       'weight': 2,
#                       'fillOpacity': 0
#                   })
#
# geojson_area.add_to(m_area)
#
# # 保存地图为HTML文件
# m_area.save('area_CHI.html')
#
# ########################################## road ################
# road_dataframe = pd.read_csv('../Processed_data/CHI/CHI_road.csv')
# junction_dataframe =  pd.read_csv('../Processed_data/CHI/CHI_junction.csv')
# # 创建一个基本地图
# m_road = folium.Map(location=[41.80, -87.80], zoom_start=10, tiles="cartodbpositron")
#
# color = {1: 'DarkBlue', 2: 'DarkOrange', 3: 'Green', 4: 'Purple', 5:'DeepSkyBlue', 6:'LightSlateGray'}
#
# def get_loc(node_df, node_id):
#     df = node_df[node_df.node_id == node_id]
#     return [df.lng.values[0], df.lat.values[0]]
#
# # 遍历每一行数据
# total_link = road_dataframe.shape[0]
# for i in tqdm(range(total_link)):
#     from_node_id = road_dataframe.iloc[i].from_node_id
#     to_node_id = road_dataframe.iloc[i].to_node_id
#     try:
#         from_loc = get_loc(junction_dataframe, from_node_id)
#         to_loc = get_loc(junction_dataframe, to_node_id)
#     except:
#         continue
#     type = road_dataframe.iloc[i].link_type
#     color_selcet = color[type]
#     if type == 1:
#         folium.PolyLine(locations=[from_loc, to_loc], weight=4, color = color_selcet, no_clip=True).add_to(m_road)
#     if type == 2:
#         folium.PolyLine(locations=[from_loc, to_loc], weight=2.5, color = color_selcet, no_clip=True).add_to(m_road)
#     if type == 3:
#         folium.PolyLine(locations=[from_loc, to_loc], weight=2, color = color_selcet, no_clip=True).add_to(m_road)
#     if type == 4:
#         folium.PolyLine(locations=[from_loc, to_loc], weight=1.2, color = color_selcet, no_clip=True).add_to(m_road)
#     if type == 5:
#         folium.PolyLine(locations=[from_loc, to_loc], weight=0.7, color = color_selcet, no_clip=True).add_to(m_road)
#     if type == 6:
#         folium.PolyLine(locations=[from_loc, to_loc], weight=0.2, color = color_selcet, no_clip=True).add_to(m_road)
#
# # 保存地图为HTML文件
# m_road.save('road_CHI.html')
#
# ########################################## POI ################
# POI_dataframe = pd.read_csv('../Processed_data/CHI/CHI_poi.csv')
#
# # 创建一个基本地图
# m_POI = folium.Map(location=[41.80, -87.80], zoom_start=10, tiles="cartodbpositron")
#
# # 遍历每一行数据
# for index, row in POI_dataframe.iterrows():
#     # 获取经纬度信息
#     # 在地图上添加Marker对象
#     folium.CircleMarker(location=[row['lat'], row['lng']], radius=1, fill=True, fill_opacity=0,
#                         color = 'DarkBlue', weight = 1).add_to(m_POI)
#
# # 保存地图为HTML文件
# m_POI.save('POI_CHI.html')

########################################## Junction ################
Junction_dataframe = pd.read_csv('../Processed_data/CHI/CHI_junction.csv')

# 创建一个基本地图
m_Junction = folium.Map(location=[41.80, -87.80], zoom_start=10, tiles="cartodbpositron")

# 遍历每一行数据
for index, row in Junction_dataframe.iterrows():
    # 获取经纬度信息
    # 在地图上添加Marker对象
    folium.RegularPolygonMarker(location=[row['lng'], row['lat']], radius=0.1, min_size=0.1, fill=True, fill_opacity=0,
                        color = 'DarkBlue',).add_to(m_Junction)


# 保存地图为HTML文件
m_Junction.save('Junction_CHI.html')