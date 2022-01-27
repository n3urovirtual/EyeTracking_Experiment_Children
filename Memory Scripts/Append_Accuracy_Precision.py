import os
import pandas as pd

preprocessed_path=(
    "C:/Users/presi/Desktop/PhD\Memory guided attention in cluttered"
    " scenes v.3/Behavioral Data/Memory/Preprocessed/"
    "Memory_preprocessed_v3.csv"
    )

collated_path=(
    "C:/Users/presi/Desktop/PhD/Memory guided attention in cluttered"
    " scenes v.3/Eye Tracking Data/2. Memory/Mem_collation/"
    "Mem_collate.csv"
    )

pre_df = pd.read_csv(preprocessed_path)
col_df=pd.read_csv(collated_path)

new_df=[]
for ind in pre_df.index:
    subject = pre_df["Subject_ID"][ind]
    image = pre_df["Image"][ind]
    acc = pre_df["Accuracy"][ind]
    precision = pre_df["Precision"][ind]
    query_string = f'Subject_ID=={subject} and Image_ID=={image}'
    slice = col_df.query(query_string).reset_index(drop=True)
    if not slice.empty:
        slice.loc[0,'Accuracy'] = acc
        slice.loc[0,'Precision'] = precision
        new_df.append(slice)

appended_data = pd.concat(new_df)
appended_data.to_csv("../Mem_collation/Mem_collate_Acc+Pre.csv", index=False)
