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

    inp[3] = datetime.strptime(inp[3], "%Y-%m-%d").toordinal()

    numericals = pd.DataFrame({'matchDate': inp[3], 'runs': inp[4], 'wickets': inp[5],
                               'balls': inp[6], 'strikerRuns': inp[7], 'nonStrikerRuns': inp[8], }, index=[0])

    print(inp)
    encoded = myEncoder.fit_transform(inp[0:3].reshape(1, -1)).toarray()

    feature_names = myEncoder.get_feature_names(
        ['venue', 'bat_team', 'bowl_team', ])

    features = pd.concat([numericals, pd.DataFrame(
        encoded, columns=feature_names).astype(int)], axis=1)

    z = predModel.predict(features)

    print("Prediction score:", z)

    return z
