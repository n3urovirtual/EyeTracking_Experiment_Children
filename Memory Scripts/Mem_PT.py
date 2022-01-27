'''APPLY PYTHAGOREAN THEOREM IN SMOOTHED MEMORY DATA'''

import os
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
from helper import TRIALS_PATH

#Apply PT into smoothed memory data to find sample-to-sample distance: 
for file in os.listdir(TRIALS_PATH):
    try:
        attributes = file.split("_")
        subject = attributes[1]
        image = attributes[3].split(".")[0]
        dataset=pd.read_csv(os.path.join(TRIALS_PATH,file),low_memory=False)
        x=dataset['BPOGX'].diff().fillna(0).to_numpy()
        y=dataset['BPOGY'].diff().fillna(0).to_numpy()
        sample_2_sample_distance= (x ** 2 + y ** 2) ** 0.5
        dataset['Distance']=np.nan_to_num(sample_2_sample_distance)
        dataset['Time']=dataset['TIME'].diff().fillna(0).to_numpy()
        dataset['Velocity_px']= dataset['Distance']/dataset['Time']
        dataset['Velocity_deg']= dataset['Velocity_px']*0.024
        dataset['Velocity_deg']= dataset['Velocity_deg'].fillna(0)
        dataset=dataset[dataset['Velocity_deg']!=0]
        vel=dataset['Velocity_deg']
        sav_vel=savgol_filter(vel, 11, 2)
        dataset['Smoothed_Velocity_deg']=sav_vel.tolist()
        dataset['Fix_or_Sac']=np.where(dataset['Smoothed_Velocity_deg']>120, 
                                       'Sac',
                                       'Fix')    
        write_f=dataset[dataset['Smoothed_Velocity_deg']<1000]
        write_f.to_csv(os.path.join(TRIALS_PATH,file), index=False)
    except:
        print('Exception raised: ' + subject + '_' + image)
        break
    
    

    

   


