import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from datetime import datetime


# retrieve the dataset from the csv file
allColumns = pd.read_csv('odiBallsReduced.csv')

#myColumns = allColumns.iloc[:50000]

# drop any unneccesary columns
myColumns = allColumns.drop(
    ['mid', 'runs_last_5', 'wickets_last_5', 'batsman', 'bowler'], axis=1)


# specify what the model will predict
labels = myColumns['total']

# specify the features that the model will use as inputs
allFeatures = myColumns.drop('total', axis=1)

# convert the string dates to datetime objects
allFeatures['date'] = pd.to_datetime(allFeatures['date'])
# extract the year from each date
allFeatures['date'] = allFeatures['date'].dt.year


# select all columns where the data type = object
forEncoding = allFeatures.select_dtypes('object')
# date also needs to be encoded
forEncoding.insert(3, 'date', allFeatures['date'])

catArray = forEncoding.values

venues = np.unique(catArray[:, 0])
exportVenues = venues.tolist()

bat_team = np.unique(catArray[:, 1])
exportBatTeams = bat_team.tolist()

bowl_team = np.unique(catArray[:, 2])
exportBowlTeams = bowl_team.tolist()

date = np.unique(catArray[:, 3])

listsArray = [exportVenues, exportBatTeams, exportBowlTeams]

# storing/pickling the items for the lists into a file
filename1 = 'listsFile'
outfile1 = open(filename1, 'wb')
pickle.dump(listsArray, outfile1)
outfile1.close()


# encode all the categorical columns
encoder = OneHotEncoder(
    categories=[venues, bat_team, bowl_team, date], handle_unknown="ignore")

encoded = encoder.fit_transform(catArray).toarray()

# storing/pickling the encoder into a file
filename3 = 'encoder'
outfile3 = open(filename3, 'wb')
pickle.dump(encoder, outfile3)
outfile3.close()

feature_names = encoder.get_feature_names(
    ['venue', 'bat_team', 'bowl_team', 'date'])

features = pd.concat([allFeatures.select_dtypes(exclude='object').drop(columns='date'), pd.DataFrame(
    encoded, columns=feature_names).astype(int)], axis=1)


train_features, test_features, train_labels, test_labels = train_test_split(
    features, labels, test_size=0.25, random_state=0)

rf = RandomForestRegressor(n_estimators=800, random_state=42, min_samples_split=5,
                           min_samples_leaf=1, max_features='sqrt', max_depth=90, bootstrap=False)
rf.fit(train_features, train_labels)

# storing/pickling the fitted model into a file
filename2 = 'forestModel'
outfile2 = open(filename2, 'wb')
pickle.dump(rf, outfile2)
outfile2.close()
