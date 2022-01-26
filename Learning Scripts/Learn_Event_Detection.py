""" Event Detection and collation into separate files """

import os
import itertools
import pandas as pd
from helper import *

# Categorize fixations and saccades based on their order:
for file in os.listdir(TRIALS_PATH):
    try:
        dataset = pd.read_csv(os.path.join(TRIALS_PATH, file))
        category = dataset["Fix_or_Sac"]
        watch_next = category != category.shift()
        rank_order = watch_next.cumsum().groupby(category).rank(method="dense")
        dataset["Group"] = category + "_" + rank_order.astype(int).astype(str)
        dataset.to_csv(os.path.join(TRIALS_PATH, file), index=False)
    except:
        print("Exception raised...")
        break

# Create separate files for each participant's fixations:
for file in os.listdir(TRIALS_PATH):
    try:
        trials = pd.read_csv(os.path.join(TRIALS_PATH, file))
        events = pd.DataFrame()
        events["Fixation_Start"] = trials.groupby("Group")["TIME"].min()
        events["Event_ID"] = trials.groupby("Group")["Group"].first()
        only_fixations = trials.query("Group.str.startswith('F').values")
        time_fix_max = only_fixations.groupby("Group")["TIME"].max()
        time_fix_min = only_fixations.groupby("Group")["TIME"].min()
        events["FPOG_DUR"] = time_fix_max - time_fix_min
        events["FPOG_X"] = only_fixations.groupby("Group")["BPOGX"].mean()
        events["FPOG_Y"] = only_fixations.groupby("Group")["BPOGY"].mean()
        events["Idx"] = events["Event_ID"].str.rsplit("_").str[-1].astype(int)
        events.sort_values("Idx", inplace=True)
        events.drop("Idx", axis=1, inplace=True)
        write_f = events[events["FPOG_DUR"] > 0.050]
        
        ###TO DO: Delete fixation with duration over 2 seconds###
        
        # add some descriptive variables as well:
        write_f.loc[write_f.index[0], "Trial_Start"] = trials["TIME"].iloc[0]
        write_f.loc[write_f.index[0], "Clutter"] = trials["CLUTTER"].iloc[0]
        total_trial_time = (write_f.iloc[-1, 0] + write_f.iloc[-1,2]) - write_f.iloc[0, 0]
        write_f.loc[write_f.index[0], "RT"] = total_trial_time
        # write_f.loc[write_f.index[0], 'Accuracy'] = trials['CS'].iloc[-1]
        
        write_f.to_csv(os.path.join(EVENTS_PATH, file), index=False)
    except:
        print("Exception raised...")
        continue


# Add columns about saccades to the files created above:
for file in os.listdir(EVENTS_PATH):
    try:
        events = pd.read_csv(os.path.join(EVENTS_PATH, file), low_memory=False)
        trial_start = events.iloc[0, 5]
        first_fixation_start = events.iloc[0, 0]
        first_fixation_dur = events.iloc[0, 2]
        events.loc[events.index[0], "SAC_LATENCY"] = (
            first_fixation_dur
            if trial_start == first_fixation_start
            else (first_fixation_start - trial_start) + first_fixation_dur
        )
        x = events["FPOG_X"].diff()
        y = events["FPOG_Y"].diff()
        events["SAC_AMPLITUDE"] = (x ** 2 + y ** 2) ** 0.5
        fix_dur_wo_last = events.iloc[:-1, 2].reset_index(drop=True)
        fix_start_dif = (
            events["Fixation_Start"].diff().dropna().reset_index(drop=True)
        )
        events["SAC_DUR"] = fix_start_dif - fix_dur_wo_last
        
        events.to_csv(os.path.join(EVENTS_PATH, file), index=False)
    except:
        print("Exception raised...")
        continue


