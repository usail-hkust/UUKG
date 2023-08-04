### Guidance on data usage and processing

We store the original unprocessed files in the **'./Meta_data'** directory. To preprocess, align, and filter these files, we utilize either the **`preprocess_meta_data_nyc.py`** or **`preprocess_meta_data_chi.py`** script. The processed data is then saved in the **'./Processed_data'** directory. Finally, we execute the **`construct_UrbanKG_NYC.py`** or **`construct_UrbanKG_CHI.py`** script to obtain the constructed urban knowledge graphs, which are stored in the **'./UrbanKG'** directory.

We divide the training set, verification set and test set by **`train_val_test_ent2id_rel2id.py`**

The file information in each directory is as follows:

```
./Meta_data    Raw data set: administrative division data, POI and road network data
./Processed_data   Aligned datasets: administrative region entity, POI entity, road network entity
./UrbanKG    City fact triples obtained from 8 entities and 13 relationships
```

