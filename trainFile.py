import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score, KFold, GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from datetime import datetime
from joblib import dump, load

predModel = load('randomForest')
importedEncodermodel = load('savedEncoderModel')


inp = np.array(['10/23/2018', 72, 0, 33, 35, 60,
                'R Premadasa Stadium', 'Sri Lanka', 'England'])

inp[0] = datetime.strptime(inp[0], "%m/%d/%Y").toordinal()

venues2 = np.unique(inp[6])
batTeam2 = np.unique(inp[7])
bowlTeam2 = np.unique(inp[8])

numericals = pd.DataFrame({'date': inp[0], 'runs': inp[1], 'wickets': inp[2],
                           'striker': inp[3], 'non-striker': inp[4], 'balls': inp[5]}, index=[0])


encoded2 = importedEncodermodel.fit_transform(inp[6:].reshape(1, -1)).toarray()

feature_names2 = importedEncodermodel.get_feature_names(
    ['venue', 'bat_team', 'bowl_team', ])

features2 = pd.concat([numericals, pd.DataFrame(
    encoded2, columns=feature_names2).astype(int)], axis=1)

importedRF = load('randomForest')

z = importedRF.predict(features2)

print("Prediction score:", z)
