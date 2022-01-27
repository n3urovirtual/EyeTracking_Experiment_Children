''' PLOT VELOCITY DATA '''

import os
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from helper import TRIALS_PATH

for file in os.listdir(TRIALS_PATH):
    attributes = file.split("_")
    subject = attributes[1]
    image = attributes[3].split(".")[0]
    dataset=pd.read_csv(os.path.join(TRIALS_PATH,file),low_memory=False)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,11))
    fig.suptitle(f'Subject:{subject} , Image:{image}',size=30)
    time=dataset['Time'].cumsum()
    smoothed_velocity1=dataset['Velocity_deg']
    smoothed_velocity2=dataset['Smoothed_Velocity_deg']
    ax1.plot(time, smoothed_velocity1)
    ax1.set_ylim([0, 1000])
    ax2.plot(time, smoothed_velocity2)
    ax2.set_ylim([0, 1000])
    #plt.axhline(90, color='red')
    #plt.title(f'Subject:1 , Image:{str(k)}')
    ax2.axhline(120, color='red')
    ax1.set_title('Unsmoothed velocity',size=15)
    ax2.set_title('Smoothed velocity',size=15)
    fig.text(
        0.5, 
        0.04, 
        "Time (in seconds)", 
        ha="center", 
        va="center", 
        fontsize=22
    )
    fig.text(
        0.08,
        0.5,
        "Velocity (deg/sec.)",
        ha="center",
        va="center",
        rotation="vertical",
        fontsize=22,
    )
    plt.show()
    plt.close()
  
    
'''  
for i,k in itertools.product(sub_id, img_id):
    file='Sub_'+str(i)+'_Image_'+str(k)+'.csv'
    dataset=pd.read_csv(os.path.join(TRIALS_PATH,file),low_memory=False)
    time=dataset['Sampling_Rate'].cumsum().fillna(0)
    velocity=dataset['Velocity_in_deg']
    plt.plot(time, velocity)
    plt.axhline(90, color='red')
    plt.title(f'Subject:{str(i)} , Image:{str(k)}')
    plt.xlabel('Time (sec)')
    plt.ylabel('Velocity values')
    plt.show()
    plt.close()'''