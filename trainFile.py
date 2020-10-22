import pandas as pd
import numpy as np
from datetime import datetime
import pickle

infile2 = open('forestModel', 'rb')
predModel = pickle.load(infile2)
infile2.close()

infile3 = open('encoder', 'rb')
myEncoder = pickle.load(infile3)
infile3.close()


def predictScore(matchValues):

    userInputs = np.array(matchValues)
    userInputs[3] = "2017"
    print(type(userInputs[3]))
    numericalInputs = userInputs[4:]

    numValues = numericalInputs.astype(np.integer)
    print(numValues)
    # numValues[6] = 300-numValues[3]
    # numValues[7] = 10-numValues[2]

    numericals = pd.DataFrame({'runs': numValues[0], 'wickets': numValues[1],
                               'strikerRuns': numValues[2], 'nonStrikerRuns': numValues[3], 'balls': numValues[4]}, index=[0])
    print(numericals)
    encoded = myEncoder.fit_transform(userInputs[0:4].reshape(1, -1)).toarray()

    feature_names = myEncoder.get_feature_names(
        ['venue', 'bat_team', 'bowl_team', 'date'])

    features = pd.concat([numericals, pd.DataFrame(
        encoded, columns=feature_names).astype(int)], axis=1)

    print(features)

    predScore = predModel.predict(features)

    print("Prediction score:", predScore)

    return predScore
