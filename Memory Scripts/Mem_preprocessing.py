"""EYE-TRACKING DATA PREPROCESSING (MEMORY TASK"""

import os
import pandas as pd
from helper import *


for file in os.listdir(DATA_PATH):

    subject_id = file.split("_")[1]

    # Read the raw ET Memory files
    dataset = pd.read_csv(
        os.path.join(DATA_PATH, file), sep="\t", dtype={"USER": object}
    )

    # Keep only samples that correspond to trials (no breaks etc.)
    dataset = dataset[(dataset["USER"].str.startswith("S"))]

    # Clean the dataset for further processing
    dataset[["IMAGE", "CLUTTER", "START_END"]] = (
        dataset["USER"].str.split("_", -1, expand=True)
    )
    dataset["IMAGE"] = dataset["IMAGE"].str.split(".", expand = True)[0]
    dataset.drop(["USER"], axis=1, inplace=True)

    """Check how many samples correspond to blinks and trackloss"""
    # Step 1: Select invalid samples based on eye-trackers BPOGV column
    blinks_trackloss = dataset[dataset["BPOGV"] == 0]

    # Step 2: Estimate percentage of invalid samples
    len_data = len(dataset.index)
    len_blinks_trackloss = len(blinks_trackloss.index)
    percentage_blinks_trackloss = (len_blinks_trackloss * 100) / len_data

    """Check how many samples (not included above) are out of range)"""
    # Step 1: Convert from gp3 coords to psychopy coords
    dataset["BPOGX"] = (dataset.loc[:, "BPOGX"] - 0.5) * screen_resX
    dataset["BPOGY"] = -1 * (dataset.loc[:, "BPOGY"] - 0.5) * screen_resY
    dataset["FPOGX"] = (dataset.loc[:, "FPOGX"] - 0.5) * screen_resX
    dataset["FPOGY"] = -1 * (dataset.loc[:, "FPOGY"] - 0.5) * screen_resY
    dataset["RPOGX"] = (dataset.loc[:, "RPOGX"] - 0.5) * screen_resX
    dataset["RPOGY"] = -1 * (dataset.loc[:, "RPOGY"] - 0.5) * screen_resY
    dataset["LPOGX"] = (dataset.loc[:, "LPOGX"] - 0.5) * screen_resX
    dataset["LPOGY"] = -1 * (dataset.loc[:, "LPOGY"] - 0.5) * screen_resY

    # Step 2: Select only valid samples
    v_samples = dataset[dataset["BPOGV"] == 1]

    # Step 3: From valid samples select those out of range (-5px each side)
    X_right = (screen_resX / 2) - 5
    X_left = -1 * (screen_resX / 2) + 5
    Y_upper = (screen_resY / 2) - 5
    Y_lower = -1 * (screen_resY / 2) + 5

    out_of_range = v_samples[
        (v_samples["BPOGX"] > X_right)
        | (v_samples["BPOGX"] < X_left)
        | (v_samples["BPOGY"] > Y_upper)
        | (v_samples["BPOGY"] < Y_lower)
    ]


    # Step 4: Estimate percentage of out of range samples
    len_out_of_range = len(out_of_range.index)
    percentage_oof = (len_out_of_range * 100) / len_data


    # Step 5: Print total percentage of samples excluded for each participant
    total_percent_loss = percentage_blinks_trackloss + percentage_oof

    print(
        f"For participant {subject_id}, a total of "
        f"{round(total_percent_loss,2)} % samples were excluded, "
        f"with {round(percentage_oof,2)} % being out of range and "
        f"{round(percentage_blinks_trackloss,2)} % due to blinks/trackloss."
    )


    #Drop invalid samples and get a clean dataset
    all_invalid = blinks_trackloss.append(out_of_range)
    dataset.drop(all_invalid.index, axis=0, inplace=True)


    #Split large csv files into smaller ones based on trial/image
    print(f"Processing participant {subject_id}...Please wait!")

    for k in img_id:
        query_str = "IMAGE == 'S" + str(k) +"'"
        trial = dataset.query(query_str)
        m = trial["CS"].eq(1)
        clean = trial.loc[: m.idxmax()] if m.any() else trial.loc[:]
        file_name = "Sub_" + subject_id + "_Image_" + str(k) + ".csv"
        clean.to_csv(
            os.path.join(TRIALS_PATH, file_name),
            columns=[
                "TIME", 
                "BPOGX", 
                "BPOGY", 
                "CLUTTER", 
                "START_END", 
                "IMAGE",
            ],
            index=False
        )

