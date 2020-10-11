import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score, KFold, GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from datetime import datetime
import pickle

infile2 = open('forestModel', 'rb')
predModel = pickle.load(infile2)
infile2.close()

infile3 = open('encoder', 'rb')
myEncoder = pickle.load(infile3)
infile3.close()


def predictScore(matchValues):

    inp = np.array(matchValues)
    print(inp)
    n = inp[3:]

    n[0] = datetime.strptime(n[0], "%Y-%m-%d").toordinal()

    ni = n.astype(np.integer)
    print(ni)
    # ni[6] = 300-ni[3]
    # ni[7] = 10-ni[2]

    numericals = pd.DataFrame({'matchDate': ni[0], 'runs': ni[1], 'wickets': ni[2],
                               'strikerRuns': ni[3], 'nonStrikerRuns': ni[4], 'balls': ni[5], 'ballsRem': 300-ni[5], 'wktsRem': 10-ni[2]}, index=[0])
    print(numericals)
    encoded = myEncoder.fit_transform(inp[0:3].reshape(1, -1)).toarray()

    feature_names = myEncoder.get_feature_names(
        ['venue', 'bat_team', 'bowl_team', ])

    features = pd.concat([numericals, pd.DataFrame(
        encoded, columns=feature_names).astype(int)], axis=1)

    z = predModel.predict(features)

    print("Prediction score:", z)

    return z
