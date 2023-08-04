"""

处理后的文件 存储到 ./UrbanKG 里面
对齐、过滤与预处理之后的文件格式：
    UrbanKG_CHI.txt: entity, relaltion, entity

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
#####################################
# load data
dataframe1 = gpd.read_file('./Meta_data/CHI/Administrative_data/Borough/Borough.shp')
# 转换为经纬度坐标系
dataframe1 = dataframe1.to_crs('EPSG:4326')
seleceted_colums1 = ['BoroCode', 'BoroName', 'geometry']
borough_dataframe = dataframe1[seleceted_colums1]
######################################
dataframe2 = gpd.read_file('./Meta_data/CHI/Administrative_data/Area/Area.shp')
# Convert to latitude-longitude coordinate system
dataframe2 = dataframe2.to_crs('EPSG:4326')
seleceted_colums2 = ['area_numbe', 'community', 'geometry']
area_dataframe = dataframe2[seleceted_colums2]
#####################################
"""

Relation 1: Borough Nearby Borough BNB

"""
#####################################

BNB = []
for i in tqdm(range(borough_dataframe.shape[0])):
    head_borough = borough_dataframe.iloc[i].geometry
    for j in range(borough_dataframe.shape[0]):
        tail_borough = borough_dataframe.iloc[j].geometry
        if head_borough.touches(tail_borough):
            BNB.append('Borough/' + str(borough_dataframe.iloc[i].BoroCode) + ' BNB ' + 'Borough/' + str(borough_dataframe.iloc[j].BoroCode))

#####################################

"""

Relation 2: Area Nearby Area ANA

"""

#####################################

ANA = []
for i in tqdm(range(area_dataframe.shape[0])):
    head_area = area_dataframe.iloc[i].geometry
    for j in range(area_dataframe.shape[0]):
        tail_area = area_dataframe.iloc[j].geometry
        if head_area.touches(tail_area):
            ANA.append('Area/' + str(area_dataframe.iloc[i].area_numbe) + ' ANA ' + 'Area/' + str(area_dataframe.iloc[j].area_numbe))

#####################################

"""

Relation 3: POI Locates at Area PLA
Relation 4: POI Belongs to Borough PBB
Relation 5: POI Has POI Category PHPC

"""

#####################################

PLA = []
PBB = []
PHPC = []

poi_dataframe = pd.read_csv('./Processed_data/CHI/CHI_poi.csv')
poi_datanumpy = np.array(poi_dataframe[[ "poi_id", "borough_id", "area_id", "cate"]])

for i in tqdm(range(poi_datanumpy.shape[0])):
    PBB.append('POI/' + str(poi_datanumpy[i][0]) + ' PBB '
               + 'Borough/' + str(poi_datanumpy[i][1]))

for i in tqdm(range(poi_datanumpy.shape[0])):
    PLA.append('POI/' + str(poi_datanumpy[i][0]) + ' PLA '
               + 'Area/' + str(poi_datanumpy[i][2]))

for i in tqdm(range(poi_datanumpy.shape[0])):
    PHPC.append('POI/' + str(poi_datanumpy[i][0]) + ' PHPC '
               + 'PC/' + str(poi_datanumpy[i][3]))

####################################

"""

Relation 6: Road Locates at Area RLA
Relation 7: Road Belongs to Borough RBB
Relation 8: Road Has POI Category RHRC

"""

#####################################

RLA = []
RBB = []
RHRC = []

road_dataframe = pd.read_csv('./Processed_data/CHI/CHI_road.csv')
road_datanumpy = np.array(road_dataframe[[ "link_id", "borough_id", "area_id", "link_type_name"]])

for i in tqdm(range(road_datanumpy.shape[0])):
    RBB.append('Road/' + str(road_datanumpy[i][0]) + ' RBB '
               + 'Borough/' + str(road_datanumpy[i][1]))

for i in tqdm(range(road_datanumpy.shape[0])):
    RLA.append('Road/' + str(road_datanumpy[i][0]) + ' RLA '
               + 'Area/' + str(road_datanumpy[i][2]))

for i in tqdm(range(road_datanumpy.shape[0])):
    RHRC.append('Road/' + str(road_datanumpy[i][0]) + ' RHRC '
               + 'RC/' + str(road_datanumpy[i][3]))

###############################################

"""

Relation 9: Junction Locates at Area JLA
Relation 10: Junction Belongs to Borough JBB
Relation 11: Junction Has POI Category JHJC

"""

#####################################

JLA = []
JBB = []
JHJC = []

junction_dataframe = pd.read_csv('./Processed_data/CHI/CHI_junction.csv')
junction_datanumpy = np.array(junction_dataframe[[ "node_id", "borough_id", "area_id", "osm_highway"]])

for i in tqdm(range(junction_datanumpy.shape[0])):
    JBB.append('Junction/' + str(junction_datanumpy[i][0]) + ' JBB '
               + 'Borough/' + str(junction_datanumpy[i][1]))

for i in tqdm(range(junction_datanumpy.shape[0])):
    JLA.append('Junction/' + str(junction_datanumpy[i][0]) + ' JLA '
               + 'Area/' + str(junction_datanumpy[i][2]))

for i in tqdm(range(junction_datanumpy.shape[0])):
    JHJC.append('Junction/' + str(junction_datanumpy[i][0]) + ' JHJC '
               + 'JC/' + str(junction_datanumpy[i][3]))

#####################################

"""

Relation 12：Junction Belongs to Road JBR

"""

# #####################################
JBR = []

road_dataframe = pd.read_csv('./Processed_data/CHI/CHI_road.csv')
road_datanumpy = road_dataframe[['from_node_id', 'to_node_id', 'link_id']].values
for i in tqdm(range(road_datanumpy.shape[0])):
    JBR.append('Junction/' + str(road_datanumpy[i][0]) + ' JBR '
                   + 'Road/' + str(road_datanumpy[i][2]))
    JBR.append('Junction/' + str(road_datanumpy[i][1]) + ' JBR '
                   + 'Road/' + str(road_datanumpy[i][2]))
# #####################################

"""

Relation 13：Area Locates at Borough ALB

"""

#####################################
ALB = []

for i in tqdm(range(area_dataframe.shape[0])):
    area = area_dataframe.iloc[i].geometry
    for j in range(borough_dataframe.shape[0]):
        borough = borough_dataframe.iloc[j].geometry
        if area.within(borough) or area.intersects(borough):
            ALB.append('Area/' + str(area_dataframe.iloc[i].area_numbe) + ' ALB ' + 'Borough/' + str(borough_dataframe.iloc[j].BoroCode))

####################################

PLA.extend(RLA)
PLA.extend(JLA)
PLA.extend(PBB)
PLA.extend(RBB)
PLA.extend(JBB)
PLA.extend(ALB)
PLA.extend(JBR)
PLA.extend(BNB)
PLA.extend(ANA)
PLA.extend(PHPC)
PLA.extend(RHRC)
PLA.extend(JHJC)
with open(r'./UrbanKG/CHI/UrbanKG_CHI.txt','w') as f2:
    for i in range(len(PLA)):
        f2.write(PLA[i])
        f2.write('\n')

f2.close()