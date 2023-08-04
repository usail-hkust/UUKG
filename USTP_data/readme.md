### Guidance on data usage and processing

We store the original unprocessed files in the **'./Meta_data'** directory. To preprocess, align, and filter these files, we utilize either the **`preprocess_meta_data_nyc.py`** or **`preprocess_meta_data_chi.py`** script. The processed data is then saved in the **'./Processed_data'** directory. 

Finally, we execute the **`construct_USTP_Pointflow_XXX.py`** script to obtain the spatiotemporal flow prediction dataset and derive **`construct_USTP_Event_XXX.py`** script to obtain the constructed urban event prediction dataset. 

We storage them in the  **'./USTP'** directory with the special format mentioned in [here](https://github.com/usail-hkust/UUKG/blob/main/USTP_Model/readme.md).

The file information in each directory is as follows:

```
./Meta_data    Raw data set: taxi, bike, crime and 311 service event data.
./Processed_data   Aligned datasets: taxi, bike, human, crime and 311 service spatiotemporal dataset which are aligned with area, road and POI.
./USTP    The reformatted USTP dataset is now ready for use with downstream USTP models. 
```

### To create your USTP dataset
Our urban spatiotemporal prediction dataset construction scheme is highly reusable. You can prepare your urban downstream task data following either the file format in **'./Meta_data'** or **'./Processed_data'**, and then run scripts **`construct_USTP_Pointflow_XXX.py`** or **`construct_USTP_Event_XXX.py`** to build your personalized USTP dataset. This flexibility allows you to adapt the construction process to various cities and datasets easily.

### Visualization
<img src="https://github.com/usail-hkust/UUKG/blob/main/USTP_data/bike_start_m.html" width="440px">

We offer spatial and temporal visualization implement for all types of USTP dataset. By leveraging the powerful visualization capabilities of **Folium**, we provide an intuitive understanding of different USTP tasks. 

You can run **`visualize_USTP.py`** to get the overall spatial and temporal distribution of USTP dataset. You can also develop other visualization function according to your preferences.
