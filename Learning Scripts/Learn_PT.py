"""APPLY PYTHAGOREAN THEOREM IN LEARNING DATA + SMOOTH VELOCITIES"""

import os
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from helper import img_id, sub_id, TRIALS_PATH

# Apply PT into smoothed learning data to find sample-to-sample distance:

for file in os.listdir(TRIALS_PATH):
    dataset = pd.read_csv(os.path.join(TRIALS_PATH, file))
    x = dataset["BPOGX"].diff().fillna(0).to_numpy()
    y = dataset["BPOGY"].diff().fillna(0).to_numpy()
    sample_2_sample_distance = (x ** 2 + y ** 2) ** 0.5
    dataset["Distance"] = np.nan_to_num(sample_2_sample_distance)
    dataset["Time"] = dataset["TIME"].diff().fillna(0).to_numpy()
    dataset["Velocity_px"] = dataset["Distance"] / dataset["Time"]
    dataset["Velocity_deg"] = dataset["Velocity_px"] * 0.021
    dataset["Velocity_deg"] = dataset["Velocity_deg"].fillna(0)
    dataset = dataset[dataset["Velocity_deg"] != 0]
    vel = dataset["Velocity_deg"]
    sav_vel = savgol_filter(vel, 13, 2)
    dataset["Smoothed_Velocity_deg"] = sav_vel.tolist()
    fix_or_sac = dataset["Smoothed_Velocity_deg"] > 120
    dataset["Fix_or_Sac"] = np.where(fix_or_sac, "Sac", "Fix")
    write_f = dataset[dataset["Smoothed_Velocity_deg"] < 1000]
    write_f.to_csv(os.path.join(TRIALS_PATH, file), index=False)


# Plot smoothed velocity vs. unsmoothed velocity
for k, i in itertools.product(sub_id, img_id):
    try:
        file = (
            "Sub_" + str(k) + "_Image_" + i.split(".")[0] + "_Block_4.csv"
        )  # Block 1,2,3,4
        dataset = pd.read_csv(os.path.join(TRIALS_PATH, file))
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 11))
        fig.suptitle(
            f'Subject:{str(k)} , Image:{i.split(".")[0]}, Block: 4', size=30
        )  # Block 1,2,3,4
        time = dataset["Time"].cumsum()
        smoothed_velocity1 = dataset["Velocity_deg"]
        smoothed_velocity2 = dataset["Smoothed_Velocity_deg"]
        ax1.plot(time, smoothed_velocity1)
        ax1.set_ylim([0, 1000])
        ax1.set_title("Unsmoothed velocity", size=15)
        ax2.plot(time, smoothed_velocity2)
        ax2.set_ylim([0, 1000])
        ax2.set_title("Smoothed velocity", size=15)
        # plt.axhline(90, color='red')
        # plt.title(f'Subject:{str(k)} , Image:{i.split(".")[0]} , Block: 1')
        ax2.axhline(120, color="red")
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
    except OSError:
        continue

#Plot to fine-tune the velocity threshold
for k, i in itertools.product(sub_id, img_id):
    file = (
        "Sub_" + str(k) + "_Image_" + i.split(".")[0] + "_Block_1.csv"
    )  # Block 1,2,3,4
    dataset = pd.read_csv(os.path.join(TRIALS_PATH, file))
    time = dataset["Time"].cumsum().fillna(0)
    velocity = dataset["Smoothed_Velocity_deg"]
    plt.plot(time, velocity)
    plt.axhline(100, color="red")
    plt.ylim(0, 1000)
    plt.title(f"Subject:{str(k)} , Image:{str(i)}")
    plt.xlabel("Time (sec)")
    plt.ylabel("Velocity values")
    plt.show()
    plt.close()
