import pandas as pd
import numpy as np
import pickle
#import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score, KFold, GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from datetime import datetime


# retrieve the dataset from the csv file
allColumns = pd.read_csv('odiBalls.csv')

myColumns = allColumns.iloc[:100000]

# drop any unneccesary columns
myColumns = myColumns.drop(
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
exportVenues = venues.tolist()

bat_team = np.unique(chi[:, 1])
exportBatTeams = bat_team.tolist()

bowl_team = np.unique(chi[:, 2])
exportBowlTeams = bowl_team.tolist()

listsArray = [exportVenues, exportBatTeams, exportBowlTeams]

# storing/pickling the items for the lists into a file
filename1 = 'listsFile'
outfile1 = open(filename1, 'wb')
pickle.dump(listsArray, outfile1)
outfile1.close()


# encode all the categorical columns
encoder = OneHotEncoder(
    categories=[venues, bat_team, bowl_team], handle_unknown="ignore")

encoded = encoder.fit_transform(chi).toarray()

# storing/pickling the encoder into a file
filename3 = 'encoder'
outfile3 = open(filename3, 'wb')
pickle.dump(encoder, outfile3)
outfile3.close()

feature_names = encoder.get_feature_names(['venue', 'bat_team', 'bowl_team'])

features = pd.concat([allFeatures.select_dtypes(exclude='object'), pd.DataFrame(
    encoded, columns=feature_names).astype(int)], axis=1)

train_features, test_features, train_labels, test_labels = train_test_split(
    features, labels, test_size=0.25, random_state=0)

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(train_features, train_labels)

# storing/pickling the fitted model into a file
filename2 = 'forestModel'
outfile2 = open(filename2, 'wb')
pickle.dump(rf, outfile2)
outfile2.close()
