"""INDIVIDUAL ET PREPROCESSING AND ANALYSIS OF CHILD EXPERIMENT"""

import os
import itertools
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm

def convert_gaze_coords(datafile):
    datafile['BPOGX']=(datafile.loc[:,'BPOGX']-0.5)*1920
    datafile['BPOGY']=-1*(datafile.loc[:,'BPOGY']-0.5)*1080
    datafile['FPOGX']=(datafile.loc[:,'FPOGX']-0.5)*1920
    datafile['FPOGY']=-1*(datafile.loc[:,'FPOGY']-0.5)*1080
    datafile['RPOGX']=(datafile.loc[:,'RPOGX']-0.5)*1920
    datafile['RPOGY']=-1*(datafile.loc[:,'RPOGY']-0.5)*1080
    datafile['LPOGX']=(datafile.loc[:,'LPOGX']-0.5)*1920
    datafile['LPOGY']=-1*(datafile.loc[:,'LPOGY']-0.5)*1080

    return datafile

file=r'C:/Users/presi/Desktop/PhD/Children experiment/Tasks/Task1/ET_Data/L_513_2021_Nov_14_1513.tsv'
IMG_PATH=r'C:/Users/presi/Desktop/PhD/Children experiment/Tasks/Images'

df=pd.read_csv(file,sep="\t")

df=convert_gaze_coords(df)

df2=df[df['BPOGV']==1]


for j,k in itertools.product(os.listdir(IMG_PATH),range(0,4)):
    dataset=df2.query("USER.str.startswith('"+str(j).split('.')[0]+".JPG_HIGH_"+str(k)+"_START').values")
    x=dataset.groupby('FPOGID')['FPOGX'].mean()
    y=dataset.groupby('FPOGID')['FPOGY'].mean()
    fix_dur=dataset.groupby('FPOGID')['FPOGD'].max()
    fig, ax = plt.subplots(figsize=(20, 11))
    ax.scatter(x,
               y,
               zorder=1,
               marker='o',
               s=fix_dur*10000,
               color='lime',
               alpha=0.5)
    ax.plot(x,
            y,
            '-o',
            linewidth=3,
            color='blue')
    img = plt.imread(IMG_PATH+ "/" + str(j))
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
                    fontsize=25,
                    color='black',
                    ha='center',
                    va='center')
    plt.xlabel('X coordinates (in pixels)', size=20)
    plt.ylabel('Y coordinates (in pixels)', size=20)
    plt.title('Scanpath for Subject 13 / Image '+str(j)+' / Block '+str(k+1), size=30)
    plt.show()

