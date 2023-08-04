"""

可视化USTP数据集的空间分布和时间分布

"""

# taxi
import pandas as pd
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
"""

Taxi

"""

###########################################################
#
file_path = '../Processed_data/CHI/CHI_taxi.csv'
taxi_data = pd.read_csv(file_path)

# Create a Folium heat map Travel starting point
taxi_start_m = folium.Map(location=[taxi_data['start_lat'].mean(), taxi_data['start_lng'].mean()], zoom_start=10, tiles="cartodbpositron")
taxi_end_m = folium.Map(location=[taxi_data['end_lat'].mean(), taxi_data['end_lng'].mean()], zoom_start=10, tiles="cartodbpositron")
#
# HeatMap(taxi_data[['start_lat', 'start_lng']].values).add_to(taxi_start_m)
# HeatMap(taxi_data[['end_lat', 'end_lng']].values).add_to(taxi_end_m)
#
# # Save Heatmap
# taxi_start_m.save('taxi_start_m.html')
# taxi_end_m.save('taxi_end_m.html')
#
#
# Extract time information and format
date_format = "%Y-%m-%d %H:%M:%S"
taxi_data['start_time'] = pd.to_datetime(taxi_data['start_time'], format=date_format)

# Plot frequency distribution over time dimension (grouped by hour)

start_data_by_day = taxi_data['start_time'].groupby(taxi_data['start_time'].dt.to_period('D')).count()

# 创建一个具有指定大小的图像（例如宽度为12英寸，高度为6英寸）
fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(start_data_by_day.index.to_timestamp(), start_data_by_day)

# 设置标题和坐标轴标签
plt.title('Frequency distribution of CHI taxi over time', fontsize=24)
plt.xlabel('Date', fontsize=24)
plt.ylabel('Frequency', fontsize=24)

# 修改x轴刻度，仅显示每个月份
xtick_locator = mdates.MonthLocator()
xtick_formatter = mdates.DateFormatter('%b %Y')
ax.xaxis.set_major_locator(xtick_locator)
ax.xaxis.set_major_formatter(xtick_formatter)
plt.xticks(rotation=45)

# 调整边界，确保显示完整的横坐标
plt.tight_layout()

# 保存频率分布图
plt.savefig('time_taxi_distribution.png')

###########################################################

"""

Bike


"""

# # 读取CSV文件
file_path = '../Processed_data/CHI/CHI_bike_road.csv'
bike_data = pd.read_csv(file_path)

# 创建Folium热力图   出行起始点
bike_start_m = folium.Map(location=[bike_data['start_lat'].mean(), bike_data['start_lng'].mean()], zoom_start=10, tiles="cartodbpositron")
bike_end_m = folium.Map(location=[bike_data['end_lat'].mean(), bike_data['end_lng'].mean()], zoom_start=10, tiles="cartodbpositron")

# HeatMap(bike_data[['start_lat', 'start_lng']].values).add_to(bike_start_m)
# HeatMap(bike_data[['end_lat', 'end_lng']].values).add_to(bike_end_m)
#
# # 保存热力图
# bike_start_m.save('bike_start_m.html')
# bike_end_m.save('bike_end_m.html')
#
#
# # 提取时间信息并格式化
date_format = "%Y-%m-%d %H:%M:%S"
bike_data['start_time'] = pd.to_datetime(bike_data['start_time'], format=date_format)

# # 绘制时间维度上的频率分布（按小时分组）

start_data_by_day = bike_data['start_time'].groupby(bike_data['start_time'].dt.to_period('D')).count()

# 创建一个具有指定大小的图像（例如宽度为12英寸，高度为6英寸）
fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(start_data_by_day.index.to_timestamp(), start_data_by_day)

# 设置标题和坐标轴标签
plt.title('Frequency distribution of CHI bike over time', fontsize=24)
plt.xlabel('Date', fontsize=24)
plt.ylabel('Frequency', fontsize=24)

# 修改x轴刻度，仅显示每个月份
xtick_locator = mdates.MonthLocator()
xtick_formatter = mdates.DateFormatter('%b %Y')
ax.xaxis.set_major_locator(xtick_locator)
ax.xaxis.set_major_formatter(xtick_formatter)
plt.xticks(rotation=45)

# 调整边界，确保显示完整的横坐标
plt.tight_layout()

# 保存频率分布图
plt.savefig('time_bike_distribution.png')

"""

Human


"""

# # 读取CSV文件
file_path = '../Processed_data/CHI/CHI_human.csv'
human_data = pd.read_csv(file_path)

# 创建Folium热力图   出行起始点
human_start_m = folium.Map(location=[human_data['start_lat'].mean(), human_data['start_lng'].mean()], zoom_start=10, tiles="cartodbpositron")
human_end_m = folium.Map(location=[human_data['end_lat'].mean(), human_data['end_lng'].mean()], zoom_start=10, tiles="cartodbpositron")

# HeatMap(human_data[['start_lat', 'start_lng']].values).add_to(human_start_m)
# HeatMap(human_data[['end_lat', 'end_lng']].values).add_to(human_end_m)
#
# # 保存热力图
# human_start_m.save('human_start_m.html')
# human_end_m.save('human_end_m.html')
#
#
# # 提取时间信息并格式化
date_format = "%Y-%m-%d %H:%M:%S"
human_data['start_time'] = pd.to_datetime(human_data['start_time'], format=date_format)

# 绘制时间维度上的频率分布（按小时分组）

start_data_by_day = human_data['start_time'].groupby(human_data['start_time'].dt.to_period('D')).count()

# 创建一个具有指定大小的图像（例如宽度为12英寸，高度为6英寸）
fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(start_data_by_day.index.to_timestamp(), start_data_by_day)

# 设置标题和坐标轴标签
plt.title('Frequency distribution of CHI human over time', fontsize=24)
plt.xlabel('Date', fontsize=24)
plt.ylabel('Frequency', fontsize=24)

# 修改x轴刻度，仅显示每个月份
xtick_locator = mdates.MonthLocator()
xtick_formatter = mdates.DateFormatter('%b %Y')
ax.xaxis.set_major_locator(xtick_locator)
ax.xaxis.set_major_formatter(xtick_formatter)
plt.xticks(rotation=45)

# 调整边界，确保显示完整的横坐标
plt.tight_layout()

# 保存频率分布图
plt.savefig('time_human_distribution.png')

# """
#
# crime
#
#
# """
#
# 读取CSV文件
file_path = '../Processed_data/CHI/CHI_crime.csv'

crime_data = pd.read_csv(file_path)
crime_data['time'] = pd.to_datetime(crime_data['time'], format="%m/%d/%Y %I:%M:%S %p")
crime_data['time'] = crime_data['time'].dt.strftime("%Y-%m-%d %H:%M:%S")

# # 创建Folium热力图   出行起始点
# crime_m = folium.Map(location=[crime_data['lat'].mean(), crime_data['lng'].mean()], zoom_start=10, tiles="cartodbpositron")
#
# HeatMap(crime_data[['lat', 'lng']].values).add_to(crime_m)
#
# # 保存热力图
# crime_m.save('crime_m.html')
#
#
# # 提取时间信息并格式化
date_format = "%Y-%m-%d %H:%M:%S"
crime_data['time'] = pd.to_datetime(crime_data['time'], format=date_format)

# 绘制时间维度上的频率分布（按小时分组）

start_data_by_day = crime_data['time'].groupby(crime_data['time'].dt.to_period('D')).count()

# 创建一个具有指定大小的图像（例如宽度为12英寸，高度为6英寸）
fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(start_data_by_day.index.to_timestamp(), start_data_by_day)

# 设置标题和坐标轴标签
plt.title('Frequency distribution of CHI crime over time', fontsize=24)
plt.xlabel('Date', fontsize=24)
plt.ylabel('Frequency', fontsize=24)

# 修改x轴刻度，仅显示每个月份
xtick_locator = mdates.MonthLocator()
xtick_formatter = mdates.DateFormatter('%b %Y')
ax.xaxis.set_major_locator(xtick_locator)
ax.xaxis.set_major_formatter(xtick_formatter)
plt.xticks(rotation=45)

# 调整边界，确保显示完整的横坐标
plt.tight_layout()

# 保存频率分布图
plt.savefig('time_crime_distribution.png')

"""

311 service


"""

# 读取CSV文件
file_path = '../Processed_data/CHI/CHI_311_service.csv'
service_data = pd.read_csv(file_path)

# # 创建Folium热力图   出行起始点
# service_m = folium.Map(location=[service_data['lat'].mean(), service_data['lng'].mean()], zoom_start=10, tiles="cartodbpositron")
#
# HeatMap(service_data[['lat', 'lng']].values).add_to(service_m)
#
# # 保存热力图
# service_m.save('service_m.html')
#
#
# 提取时间信息并格式化
date_format = "%Y-%m-%d %H:%M:%S"
service_data['time'] = pd.to_datetime(service_data['time'], format=date_format)

# 绘制时间维度上的频率分布（按小时分组）

start_data_by_day = service_data['time'].groupby(service_data['time'].dt.to_period('D')).count()

# 创建一个具有指定大小的图像（例如宽度为12英寸，高度为6英寸）
fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(start_data_by_day.index.to_timestamp(), start_data_by_day)

# 设置标题和坐标轴标签
plt.title('Frequency distribution of CHI 311 service over time', fontsize=24)
plt.xlabel('Date', fontsize=24)
plt.ylabel('Frequency', fontsize=24)

# 修改x轴刻度，仅显示每个月份
xtick_locator = mdates.MonthLocator()
xtick_formatter = mdates.DateFormatter('%b %Y')
ax.xaxis.set_major_locator(xtick_locator)
ax.xaxis.set_major_formatter(xtick_formatter)
plt.xticks(rotation=45)

# 调整边界，确保显示完整的横坐标
plt.tight_layout()

# 保存频率分布图
plt.savefig('time_service_distribution.png')