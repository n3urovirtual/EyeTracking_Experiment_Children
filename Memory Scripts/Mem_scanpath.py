import os
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from helper import *


#Visualize scanpath for all participants based on I-VT fixations:
for h,j in itertools.product(sub_id,img_id):
    file='Sub_'+str(h)+'_Image_'+str(j)+'.csv'
    events=pd.read_csv(os.path.join(EVENTS_PATH,file),low_memory=False)
    x=events['FPOG_X']
    y=events['FPOG_Y']
    fix_dur=events['FPOG_DUR']
    fig, ax = plt.subplots(figsize=(20, 11))
    ax.scatter(x,
               y,
               zorder=1
               ,marker='o',
               s=fix_dur*10000,
               color='lime',
               alpha=0.5)
    ax.plot(x,
            y,
            '-o',
            linewidth=3,
            color='blue')
    img = plt.imread(IMG_PATH+"\S"+str(j)+".jpg")
    plt.imshow(img, 
               zorder=0, 
               extent=[-960, 960, -540, 540],
               aspect='auto')
    for i in range(len(fix_dur)):
        ax.annotate(str(i+1),
                    xy=(fix_dur.iloc[i],
                        fix_dur.iloc[i]),
                    xytext=(x.iloc[i], 
                            y.iloc[i]),
                    fontsize=30,
                    color='black',
                    ha='center',
                    va='center')
    plt.xlabel('X coordinates (in pixels)', size=20)
    plt.ylabel('Y coordinates (in pixels)', size=20)
    plt.title('Scanpath for Subject '+str(h)+' , Image '+str(j), size=30)
    
    #draw a rectangle around the location of the star
    target_coords=pd.read_csv(BEHAVIORAL_FILE)
    slice=target_coords[(target_coords['Image']==j) & 
                        (target_coords['participant']==h)]
    left=int(slice['StarX'])-50 #X coordinate
    bottom=int(slice['StarY'])-50 #Y coordinate
    width=100
    height=100
    rect=mpatches.Rectangle((left,bottom),width, height, 
                            fill=False,
                            color='orange',
                            linewidth=5)
    plt.gca().add_patch(rect)
    my_img='Subject_'+str(h)+'_Image_'+str(j)+'.png'
    fig.savefig(os.path.join(IVT_SCANPATH,my_img))
    #plt.show()
    plt.close()
