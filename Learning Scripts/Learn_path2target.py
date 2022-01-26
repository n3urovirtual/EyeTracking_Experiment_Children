''' CALCULATE DISTANCE FROM (0,0) TO TARGET FOR ALL SUBJECTS/IMAGES'''

import pandas as pd
from helper import *
import os


dataset = pd.read_csv(BEHAVIORAL_FILE)

for i in range(len(dataset)):
    row = dataset.iloc[[i]].reset_index(drop=True)
    subject = row.iloc[0, 0]
    image = row.iloc[0, -3]
    file = "Sub_" + str(subject) + "_Image_" + str(image) + ".csv"
    row.to_csv(os.path.join(DIR_ROUTE_PATH, file), index=False)
    print(subject, image)
