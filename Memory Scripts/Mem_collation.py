''' MEMORY DATA COLLATION (VARIABLES OF INTEREST FOR EACH PARTICIPANT/TRIAL)'''

import os
import itertools
import pandas as pd
import numpy as np
from helper import *

collation=pd.DataFrame()

##TO DO: check why it omits subject 1, image 1.

for file in os.listdir(EVENTS_PATH):
    try:
        attributes = file.split("_")
        subject = attributes[1]
        image = attributes[3].split(".")[0]
        events=pd.read_csv(os.path.join(EVENTS_PATH,file),low_memory=False)
        dir_route=pd.read_csv(os.path.join(DIR_ROUTE_PATH,file),low_memory=False)
        collation['Subject_ID'] = subject
        collation['Image_ID'] = image
        collation['Clutter'] = events['Clutter'].iloc[0]
        collation['Total_num_fixations'] = events['Event_ID'].count()
        collation['Mean_fixation_dur'] = events['FPOG_DUR'].mean()
        collation['First_saccade_latency'] = events['SAC_LATENCY'].iloc[0]
        collation['Mean_saccade_length'] = events['SAC_AMPLITUDE'].mean()
        collation['Scanpath_length'] = events['SAC_AMPLITUDE'].sum()
        path_ratio = collation['Scanpath_length'] / dir_route['Direct_Route']
        collation['Scanpath_ratio'] = path_ratio
        file_to_write = 'Mem_collate.csv'
        output_path = os.path.join(COLLATION_PATH,file_to_write)
        head = not os.path.exists(output_path)
        collation.to_csv(output_path, index = False, mode = 'a', header = head)
    except FileNotFoundError:
        print("Exception raised: " + subject + "_" + image)
        continue
        
    