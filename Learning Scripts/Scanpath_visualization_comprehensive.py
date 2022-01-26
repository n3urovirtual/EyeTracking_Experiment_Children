""" Comprehensive visualization of scanpath"""

import os
import itertools
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from helper import *

# Visualize scanpath for all participants based on I-VT fixations:
for file in os.listdir(EVENTS_PATH):
    try:
        attributes = file.split("_")
        sub = attributes[1]
        image = attributes[3]
        block = attributes[5].split(".")[0]
        set = pd.read_csv(os.path.join(EVENTS_PATH, file), low_memory=False)
        dataset = set.query("Event_ID.str.startswith('F').values")
        x = dataset["FPOG_X"]
        y = dataset["FPOG_Y"]
        fix_dur = dataset["FPOG_DUR"]
        fig, ax = plt.subplots(figsize=(20, 11))
        ax.scatter(
            x, 
            y, 
            zorder=1, 
            marker="o", 
            s=fix_dur * 10000, 
            color="lime", 
            alpha=0.5
        )
        ax.plot(
            x, 
            y, 
            "-o", 
            linewidth=3, 
            color="blue"
        )
        img = plt.imread(IMG_PATH + "\S" + image + ".jpg")
        plt.imshow(
            img, 
            zorder=0, 
            extent=[-960, 960, -540, 540], 
            aspect="auto"
        )
        for h in range(len(fix_dur)):
            ax.annotate(
                str(h + 1),
                xy=(fix_dur.iloc[h], fix_dur.iloc[h]),
                xytext=(x.iloc[h], y.iloc[h]),
                fontsize=30,
                color="black",
                ha="center",
                va="center",
            )
        plt.xlabel("X coordinates (in pixels)", size=20)
        plt.ylabel("Y coordinates (in pixels)", size=20)
        title = (
            "Scanpath for Subject "
            + str(sub)
            + " /Image "
            + str(image)
            + " /Block "
            + str(block)
        )
        plt.title(title, size=30)
        
        # draw a rectangle around the location of the star
        target_coords = pd.read_csv(BEHAVIORAL_FILE)
        slice = target_coords[
            (target_coords["Image"] == int(image))
            & (target_coords["Subject_ID"] == float(sub))
        ]
        left_up = slice.iloc[0, 2]  # X coordinate
        bottom_right = slice.iloc[0, 4]  # Y coordinate
        width = 200
        height = 200
        rect = mpatches.Rectangle(
            (left_up - 100, bottom_right - 100),
            width,
            height,
            fill=False,
            color="orange",
            linewidth=2,
        )
        circle = mpatches.Circle(
            (left_up, bottom_right), 
            radius=10, 
            color="red"
        )
        plt.gca().add_patch(rect)
        plt.gca().add_patch(circle)
        output_img = (
            "Sub_" 
            + str(sub) 
            + "_Image_" 
            + str(image) 
            + "_Block_" 
            + str(block) 
            + ".png"
        )
        # fig.savefig(os.path.join(IVT_SCANPATH,output_img))
        plt.show()
        plt.close()
    except OSError:
        continue
