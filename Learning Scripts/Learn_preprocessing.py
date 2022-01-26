"""LEARNING PREPROCESSING"""

import os
import itertools
import pandas as pd
from helper import *

for file in os.listdir(DATA_PATH):
    
    subject = file.split("_")[1]

    # Read the raw ET Memory files
    dataset = pd.read_csv(os.path.join(DATA_PATH, file), 
                          sep="\t", 
                          low_memory=False
                          )
    dataset = dataset[(dataset["USER"].astype(str).str.startswith("S"))]

    """Check how many samples correspond 
    to invalid data (blinks and trackloss)"""
    
    # Step 1: Select invalid samples based on eye-trackers BPOGV column
    blinks_trackloss = dataset[dataset["BPOGV"] == 0]

    # Step 2: Estimate percentage of invalid samples
    len_data = len(dataset.index)
    len_blinks_trackloss = len(blinks_trackloss.index)
    percentage_blinks_trackloss = (len_blinks_trackloss * 100) / len_data

    """Check how many samples (not included above) 
    are invalid (out of range)"""
    
    # Step 1: Convert from gp3 coords to psychopy coords
    dataset.loc[:, "BPOGX"] = (dataset.loc[:, "BPOGX"] - 0.5) * screen_X
    dataset.loc[:, "BPOGY"] = -1 * (dataset.loc[:, "BPOGY"] - 0.5) * screen_Y
    dataset.loc[:, "FPOGX"] = (dataset.loc[:, "FPOGX"] - 0.5) * screen_X
    dataset.loc[:, "FPOGY"] = -1 * (dataset.loc[:, "FPOGY"] - 0.5) * screen_Y
    dataset.loc[:, "RPOGX"] = (dataset.loc[:, "RPOGX"] - 0.5) * screen_X
    dataset.loc[:, "RPOGY"] = -1 * (dataset.loc[:, "RPOGY"] - 0.5) * screen_Y
    dataset.loc[:, "LPOGX"] = (dataset.loc[:, "LPOGX"] - 0.5) * screen_X
    dataset.loc[:, "LPOGY"] = -1 * (dataset.loc[:, "LPOGY"] - 0.5) * screen_Y

    # Step 2: Select only valid samples
    v_samples = dataset[dataset["BPOGV"] == 1]

    # Step 3: From valid samples select those out of range (-5px each side)
    X_right = (screen_X / 2) - 5
    X_left = -1 * (screen_X / 2) + 5
    Y_upper = (screen_Y / 2) - 5
    Y_lower = -1 * (screen_Y / 2) + 5

    out_of_range = v_samples[
        (v_samples["BPOGX"] > X_right)
        | (v_samples["BPOGX"] < X_left)
        | (v_samples["BPOGY"] > Y_upper)
        | (v_samples["BPOGY"] < Y_lower)
    ]

    # Step 4: Estimate percentage of out of range samples
    len_out_of_range = len(out_of_range.index)
    percentage_oof = (len_out_of_range * 100) / len_data

    """ Print total percentage of samples excluded for each participant"""
    total_percent_loss = percentage_blinks_trackloss + percentage_oof
    

    print(
        f"For participant {subject}, a total of {round(total_percent_loss,2)}"
        f" % samples were excluded, with {round(percentage_oof,2)} % being"
        f" out of range and {round(percentage_blinks_trackloss,2)} % due to"
        f" blinks/trackloss."
    )

    """ Drop invalid samples and get a clean dataset"""
    all_invalid = blinks_trackloss.append(out_of_range)
    dataset.drop(all_invalid.index, axis=0, inplace=True)

    """Split large csv files into smaller ones based on trial/image"""
    
    print(
        f"Processing participant {subject}." 
        f"This may take a while. Please wait!"
    )

    for i, j in itertools.product(img_id, range(0, 4)):
        try:
            query_str = "USER.str.startswith('S" + i + str(j) + "').values"
            trial = dataset.query(query_str)
            trial[["IMAGE","CLUTTER","BLOCK","START_END"]] = (
                trial["USER"].str.split("_", -1, expand=True)
                )
            image = trial["IMAGE"].str.split(".",expand=True)
            trial.loc[:, "IMG"] = image.loc[:, 0]
            trial.drop(["USER", "IMAGE"], axis=1, inplace=True)
            m = trial["CS"].eq(1)
            clean = trial.loc[: m.idxmax()] if m.any() else trial.loc[:]
            img_num = i.split(".")[0]
            file_name = (
                "Sub_"
                + str(subject)
                + "_Image_"
                + img_num
                + "_Block_"
                + str(j + 1)
                + ".csv"
            )
            clean.to_csv(
                os.path.join(TRIALS_PATH, file_name),
                columns=[
                    "TIME",
                    "BPOGX",
                    "BPOGY",
                    "CLUTTER",
                    "BLOCK",
                    "START_END",
                    "IMG",
                ],
                index=False,
            )
        except:
            # Participant 516, image 6, block 3 is completely out
            continue