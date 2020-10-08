import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score, KFold, GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from datetime import datetime
from joblib import dump, load

# retrieve the dataset from the csv file
allColumns = pd.read_csv('odiBalls.csv')

# drop any unneccesary columns
myColumns = allColumns.drop(
    ['mid', 'runs_last_5', 'wickets_last_5', 'batsman', 'bowler'], axis=1)

# convert the date input to a pandas datetime object
myColumns['date'] = pd.to_datetime(myColumns['date'])

# convert all the dates in the date column to type ordinal
myColumns['date'] = myColumns['date'].apply(datetime.toordinal)

# specify what the model will predict
labels = np.array(myColumns['total'])

# specify the features that the model will use as inputs
allFeatures = myColumns.drop('total', axis=1)

# select all columns where the data type = object
forEncoding = allFeatures.select_dtypes('object')

chi = forEncoding.values

venues = np.unique(chi[:, 0])
bat_team = np.unique(chi[:, 1])
bowl_team = np.unique(chi[:, 2])

# encode all the categorical columns
encoder = OneHotEncoder(
    categories=[venues, bat_team, bowl_team], handle_unknown="ignore")

encoded = encoder.fit_transform(chi).toarray()

dump(encoder, 'savedEncoderModel')

feature_names = encoder.get_feature_names(['venue', 'bat_team', 'bowl_team'])

features = pd.concat([allFeatures.select_dtypes(exclude='object'), pd.DataFrame(
    encoded, columns=feature_names).astype(int)], axis=1)

train_features, test_features, train_labels, test_labels = train_test_split(
    features, labels, test_size=0.25, random_state=0)

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(train_features, train_labels)
dump(rf, 'randomForest')
# Use the forest's predict method on the new data

inp = np.array(['10/23/2018', 72, 0, 33, 35, 60,
                'R Premadasa Stadium', 'Sri Lanka', 'England'])

inp[0] = datetime.strptime(inp[0], "%m/%d/%Y").toordinal()

venues2 = np.unique(inp[6])
batTeam2 = np.unique(inp[7])
bowlTeam2 = np.unique(inp[8])

numericals = pd.DataFrame({'date': inp[0], 'runs': inp[1], 'wickets': inp[2],
                           'striker': inp[3], 'non-striker': inp[4], 'balls': inp[5]}, index=[0])

importedEncodermodel = load('savedEncoderModel')

encoded2 = importedEncodermodel.fit_transform(inp[6:].reshape(1, -1)).toarray()

feature_names2 = importedEncodermodel.get_feature_names(
    ['venue', 'bat_team', 'bowl_team', ])

features2 = pd.concat([numericals, pd.DataFrame(
    encoded2, columns=feature_names2).astype(int)], axis=1)

importedRF = load('randomForest')

z = importedRF.predict(features2)

print("Prediction score:", z)
