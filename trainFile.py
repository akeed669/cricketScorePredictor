#import statements
import pandas as pd
import numpy as np
from datetime import datetime
import pickle

# retrieve the trained model
infile2 = open('forestModel', 'rb')
predModel = pickle.load(infile2)
infile2.close()

# retrieve the encoder model encoding for categorical inputs
infile3 = open('encoder', 'rb')
myEncoder = pickle.load(infile3)
infile3.close()

# method to predict score


def predictScore(matchValues):
    # convert list into numpy array
    userInputs = np.array(matchValues)
    # match date is set to 2017 (dataset has records only upto 2017)
    userInputs[3] = "2017"

    # convert the numerical inputs into numpy numbers
    numericalInputs = userInputs[4:]
    numValues = numericalInputs.astype(np.integer)

    # create a dataframe of the numerical inputs
    numericals = pd.DataFrame({'runs': numValues[0], 'wickets': numValues[1],
                               'strikerRuns': numValues[2],
                               'nonStrikerRuns': numValues[3],
                               'balls': numValues[4]}, index=[0])

    # encode the categorical inputs into dummy variables
    # creates dummies that match those in trained model
    encoded = myEncoder.fit_transform(userInputs[0:4].reshape(1, -1)).toarray()

    feature_names = myEncoder.get_feature_names(
        ['venue', 'bat_team', 'bowl_team', 'date'])

    # combine numerical and categorical inputs and create new dataframe
    features = pd.concat([numericals, pd.DataFrame(
        encoded, columns=feature_names).astype(int)], axis=1)

    # predict score with random forest model
    predScore = predModel.predict(features)

    #print("Prediction score:", predScore)

    # return the prediction
    return predScore
