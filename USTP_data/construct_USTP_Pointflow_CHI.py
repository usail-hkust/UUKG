"""

trafficstatepoin The spatial dimension is one-dimensional datasets (i.e. point-based/segment-based/area-based datasets)

The processed files are stored in ./USTP_Model
File format after alignment, filtering and preprocessing:
    flow dataset
   .geo：geo_id,type,coordinates
   .grid：dyna_id,type,time,row_id,column_id,inflow,outflow
   .rel：rel_id,type,origin_id,destination_id,cost


"""
from tqdm import tqdm
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from shapely import wkt
from tqdm import tqdm
import geopandas as gpd
import pandas as pd
import folium
import re
from shapely.geometry import MultiPolygon
import numpy as np
from shapely.geometry import Point

dataframe2 = gpd.read_file('../UrbanKG_data/Meta_data/CHI/Administrative_data/Area/Area.shp')
# 转Convert to latitude-longitude coordinate system
dataframe2 = dataframe2.to_crs('EPSG:4326')
seleceted_colums2 = ['area_numbe', 'community', 'geometry']
area_dataframe = dataframe2[seleceted_colums2]


"""

USTP_data 1: taxi

"""
##################################################################################################
##################################################################################################
taxi_dataframe = pd.read_csv('./Processed_data/CHI/CHI_taxi.csv')

taxi_numpy = taxi_dataframe[['start_time', 'end_time', 'start_area_id', 'end_area_id']].values

begin_time = '2019-04-01 00:00:00'
format_pattern = '%Y-%m-%d %H:%M:%S'

in_flow = np.zeros([91 * 24 * 2, 77])
out_flow = np.zeros([91 * 24 * 2, 77])

for i in tqdm(range(taxi_numpy.shape[0])):
    time_spannn_out = datetime.strptime(str(taxi_numpy[i][0]), format_pattern) - datetime.strptime(begin_time, format_pattern)
    total_seconds_out = int(time_spannn_out.total_seconds())
    time_step_out =  int(total_seconds_out / 1800)
    if 0<= time_step_out <= 4367:
        out_flow[time_step_out][ int(taxi_numpy[i][2]) - 1] += 1

    time_spannn_in = datetime.strptime(str(taxi_numpy[i][1]), format_pattern) - datetime.strptime(begin_time, format_pattern)
    total_seconds_in = int(time_spannn_in.total_seconds())
    time_step_in = int(total_seconds_in / 1800)
    if 0 <= time_step_in <= 4367:
        in_flow[time_step_in][int(taxi_numpy[i][3])- 1] += 1

begin_time = '2019-04-01T00:00:00Z'
format_pattern = '%Y-%m-%dT%H:%M:%SZ'
now = datetime.strptime(begin_time, format_pattern)

NYCTaxi20200406_dyna = []
NYCTaxi20200406_dyna.append('dyna_id,type,time,entity_id,inflow,outflow')
NYCTaxi20200406_geo = []
NYCTaxi20200406_geo.append('geo_id,type,coordinates')

dyna_id = 0
type = 'state'

for i in tqdm(range(in_flow.shape[1])):
    for j in range(in_flow.shape[0]):
        time_origin = now + timedelta(minutes = 30 * j)
        time_write = time_origin.strftime('%Y-%m-%dT%H:%M:%SZ')
        inflow = in_flow[j][i]
        outflow = out_flow[j][i]

        grid_record = str(dyna_id) + ',' + type + ',' + str(time_write) + ',' + str(i+1) + ',' + str(int(inflow)) + ',' + str(int(outflow))
        dyna_id += 1
        NYCTaxi20200406_dyna.append(grid_record)

    geo_record = str(i+1) + ',' + 'Point' + ',"[]"'
    NYCTaxi20200406_geo.append(geo_record)

with open(r'./USTP/CHI/CHITaxi20190406/CHITaxi20190406.dyna','w') as f1:
    for i in range(len(NYCTaxi20200406_dyna)):
        f1.write(NYCTaxi20200406_dyna[i])
        f1.write('\n')
f1.close()

with open(r'./USTP/CHI/CHITaxi20190406/CHITaxi20190406.geo','w') as f1:
    for i in range(len(NYCTaxi20200406_geo)):
        f1.write(NYCTaxi20200406_geo[i])
        f1.write('\n')
f1.close()

NYCTaxi20200406_rel = []
NYCTaxi20200406_rel.append('rel_id,type,origin_id,destination_id,cost')

rel_id = 0
type = 'geo'
region_region_top16_adj = np.zeros([77, 77])
for i in tqdm(range(area_dataframe.shape[0])):
    head_area = area_dataframe.iloc[i].geometry
    for j in range(area_dataframe.shape[0]):
        tail_area = area_dataframe.iloc[j].geometry
        distance = head_area.distance(tail_area)
        NYCTaxi20200406_rel.append(str(rel_id) + ',' +  type + ',' + str(area_dataframe.iloc[i].area_numbe) + ',' + str(area_dataframe.iloc[j].area_numbe)
                                   + ',' + str(distance))
        rel_id += 1

with open(r'./USTP/CHI/CHITaxi20190406/CHITaxi20190406.rel','w') as f1:
    for i in range(len(NYCTaxi20200406_rel)):
        f1.write(NYCTaxi20200406_rel[i])
        f1.write('\n')
f1.close()

##################################################################################################
##################################################################################################

"""

USTP_data 2: bike

"""

bike_dataframe = pd.read_csv('./Processed_data/CHI/CHI_bike_road.csv')

taxi_numpy = bike_dataframe[['start_time', 'end_time', 'start_road_id', 'end_road_id']].values

begin_time = '2019-04-01 00:00:00'
format_pattern = '%Y-%m-%d %H:%M:%S'

# 建立 road_id 的 index
unique_strat_road_id = bike_dataframe['start_road_id'].unique()
unique_end_road_id = bike_dataframe['end_road_id'].unique()
c = np.concatenate((unique_strat_road_id, unique_end_road_id))
# 去重
unique_road_id = np.unique(c)

index_dict = {}
revers_index_dict = {}
for index, element in enumerate(unique_road_id):
    index_dict[index] = element
    revers_index_dict[element] = index

in_flow = np.zeros([91 * 24 * 2, len(index_dict)])
out_flow = np.zeros([91 * 24 * 2, len(index_dict)])

for i in tqdm(range(taxi_numpy.shape[0])):
    time_spannn_out = datetime.strptime(str(taxi_numpy[i][0]), format_pattern) - datetime.strptime(begin_time, format_pattern)
    total_seconds_out = int(time_spannn_out.total_seconds())
    time_step_out =  int(total_seconds_out / 1800)
    if 0<= time_step_out <= 4367:
        out_flow[time_step_out][ int(revers_index_dict[taxi_numpy[i][2]]) ] += 1

    time_spannn_in = datetime.strptime(str(taxi_numpy[i][1]), format_pattern) - datetime.strptime(begin_time, format_pattern)
    total_seconds_in = int(time_spannn_in.total_seconds())
    time_step_in = int(total_seconds_in / 1800)
    if 0 <= time_step_in <= 4367:
        in_flow[time_step_in][int(revers_index_dict[taxi_numpy[i][3]]) ] += 1

begin_time = '2019-04-01T00:00:00Z'
format_pattern = '%Y-%m-%dT%H:%M:%SZ'
now = datetime.strptime(begin_time, format_pattern)

NYCTaxi20200406_dyna = []
NYCTaxi20200406_dyna.append('dyna_id,type,time,entity_id,inflow,outflow')
NYCTaxi20200406_geo = []
NYCTaxi20200406_geo.append('geo_id,type,coordinates')

dyna_id = 0
type = 'state'

for i in tqdm(range(in_flow.shape[1])):
    for j in range(in_flow.shape[0]):
        time_origin = now + timedelta(minutes = 30 * j)
        time_write = time_origin.strftime('%Y-%m-%dT%H:%M:%SZ')
        inflow = in_flow[j][i]
        outflow = out_flow[j][i]

        grid_record = str(dyna_id) + ',' + type + ',' + str(time_write) + ',' + str(index_dict[i]) + ',' + str(int(inflow)) + ',' + str(int(outflow))
        dyna_id += 1
        NYCTaxi20200406_dyna.append(grid_record)

    geo_record = str(index_dict[i]) + ',' + 'Point' + ',"[]"'
    NYCTaxi20200406_geo.append(geo_record)

with open(r'./USTP/CHI/CHIBike20190406/CHIBike20190406.dyna','w') as f1:
    for i in range(len(NYCTaxi20200406_dyna)):
        f1.write(NYCTaxi20200406_dyna[i])
        f1.write('\n')
f1.close()

with open(r'./USTP/CHI/CHIBike20190406/CHIBike20190406.geo','w') as f1:
    for i in range(len(NYCTaxi20200406_geo)):
        f1.write(NYCTaxi20200406_geo[i])
        f1.write('\n')
f1.close()

NYCTaxi20200406_rel = []
NYCTaxi20200406_rel.append('rel_id,type,origin_id,destination_id,cost')

rel_id = 0
type = 'geo'

## 取出 road dataframe
road_dafaframe = pd.read_csv('../UrbanKG_data/Processed_data/CHI/CHI_road.csv')
road_dafaframe_filter = road_dafaframe[road_dafaframe['link_id'].isin(unique_road_id)]
road_datanumpy = road_dafaframe_filter[['geometry', 'link_id']].values

for i in tqdm(range(road_datanumpy.shape[0])):
    head_road_linestring = wkt.loads(str(road_datanumpy[i][0]))
    for j in range(road_datanumpy.shape[0]):
        tail_road_linestring = wkt.loads(str(road_datanumpy[j][0]))
        distance = head_road_linestring.distance(tail_road_linestring)

        NYCTaxi20200406_rel.append(str(rel_id) + ',' +  type + ',' + str(road_datanumpy[i][1]) + ',' + str(road_datanumpy[j][1])
                                   + ',' + str(distance))
        rel_id += 1

with open(r'./USTP/CHI/CHIBike20190406/CHIBike20190406.rel','w') as f1:
    for i in range(len(NYCTaxi20200406_rel)):
        f1.write(NYCTaxi20200406_rel[i])
        f1.write('\n')
f1.close()

##################################################################################################
##################################################################################################

"""

USTP_data 3: human

"""

bike_dataframe = pd.read_csv('./Processed_data/CHI/CHI_human.csv')

taxi_numpy = bike_dataframe[['start_time', 'end_time', 'start_poi_id', 'end_poi_id']].values

begin_time = '2019-04-01 00:00:00'
format_pattern = '%Y-%m-%d %H:%M:%S'

# 建立 road_id 的 index
unique_strat_road_id = bike_dataframe['start_poi_id'].unique()
unique_end_road_id = bike_dataframe['end_poi_id'].unique()
c = np.concatenate((unique_strat_road_id, unique_end_road_id))
# 去重
unique_road_id = np.unique(c)

index_dict = {}
revers_index_dict = {}
for index, element in enumerate(unique_road_id):
    index_dict[index] = element
    revers_index_dict[element] = index

in_flow = np.zeros([91 * 24 * 2, len(index_dict)])
out_flow = np.zeros([91 * 24 * 2, len(index_dict)])

for i in tqdm(range(taxi_numpy.shape[0])):
    time_spannn_out = datetime.strptime(str(taxi_numpy[i][0]), format_pattern) - datetime.strptime(begin_time, format_pattern)
    total_seconds_out = int(time_spannn_out.total_seconds())
    time_step_out =  int(total_seconds_out / 1800)
    if 0<= time_step_out <= 4367:
        out_flow[time_step_out][ int(revers_index_dict[taxi_numpy[i][2]]) ] += 1

    time_spannn_in = datetime.strptime(str(taxi_numpy[i][1]), format_pattern) - datetime.strptime(begin_time, format_pattern)
    total_seconds_in = int(time_spannn_in.total_seconds())
    time_step_in = int(total_seconds_in / 1800)
    if 0 <= time_step_in <= 4367:
        in_flow[time_step_in][int(revers_index_dict[taxi_numpy[i][3]]) ] += 1

begin_time = '2019-04-01T00:00:00Z'
format_pattern = '%Y-%m-%dT%H:%M:%SZ'
now = datetime.strptime(begin_time, format_pattern)

NYCTaxi20200406_dyna = []
NYCTaxi20200406_dyna.append('dyna_id,type,time,entity_id,inflow,outflow')
NYCTaxi20200406_geo = []
NYCTaxi20200406_geo.append('geo_id,type,coordinates')

dyna_id = 0
type = 'state'

for i in tqdm(range(in_flow.shape[1])):
    for j in range(in_flow.shape[0]):
        time_origin = now + timedelta(minutes = 30 * j)
        time_write = time_origin.strftime('%Y-%m-%dT%H:%M:%SZ')
        inflow = in_flow[j][i]
        outflow = out_flow[j][i]

        grid_record = str(dyna_id) + ',' + type + ',' + str(time_write) + ',' + str(index_dict[i]) + ',' + str(int(inflow)) + ',' + str(int(outflow))
        dyna_id += 1
        NYCTaxi20200406_dyna.append(grid_record)

    geo_record = str(index_dict[i]) + ',' + 'Point' + ',"[]"'
    NYCTaxi20200406_geo.append(geo_record)

with open(r'./USTP/CHI/CHIHuman20190406/CHIHuman20190406.dyna','w') as f1:
    for i in range(len(NYCTaxi20200406_dyna)):
        f1.write(NYCTaxi20200406_dyna[i])
        f1.write('\n')
f1.close()

with open(r'./USTP/CHI/CHIHuman20190406/CHIHuman20190406.geo','w') as f1:
    for i in range(len(NYCTaxi20200406_geo)):
        f1.write(NYCTaxi20200406_geo[i])
        f1.write('\n')
f1.close()

NYCTaxi20200406_rel = []
NYCTaxi20200406_rel.append('rel_id,type,origin_id,destination_id,cost')

rel_id = 0
type = 'geo'

## 取出 road dataframe
poi_dafaframe = pd.read_csv('../UrbanKG_data/Processed_data/CHI/CHI_poi.csv')
poi_dafaframe_filter = poi_dafaframe[poi_dafaframe['poi_id'].isin(unique_road_id)]
poi_datanumpy = poi_dafaframe_filter[['lng', 'lat', 'poi_id']].values

for i in tqdm(range(poi_datanumpy.shape[0])):
    head_point = Point(poi_datanumpy[i][0], poi_datanumpy[i][1])
    for j in range(poi_datanumpy.shape[0]):
        tail_point = Point(poi_datanumpy[j][0], poi_datanumpy[j][1])
        distance = head_point.distance(tail_point)

        NYCTaxi20200406_rel.append(str(rel_id) + ',' +  type + ',' + str(poi_datanumpy[i][2]) + ',' + str(poi_datanumpy[j][2])
                                   + ',' + str(distance))
        rel_id += 1

with open(r'./USTP/CHI/CHIHuman20190406/CHIHuman20190406.rel','w') as f1:
    for i in range(len(NYCTaxi20200406_rel)):
        f1.write(NYCTaxi20200406_rel[i])
        f1.write('\n')
f1.close()