
#import statements
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from trainFile import predictScore
import json
import pickle


app = Flask(__name__)
# enable cross origin resource sharing
# necessary to connect with the front-end
CORS(app)

# get categorical data from the pickled file
infile1 = open('listsFile', 'rb')
lists = pickle.load(infile1)
infile1.close()

# handle route for populating categorical data


@app.route('/listdata')
def sendListData():
    # send data from list as JSON object
    response = jsonify({"venues": lists[0],
                        "bowlTeams": lists[2], "batTeams": lists[1]})
    return response


# handle route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    # get form data in JSON form
    req_data = request.get_json()
    # convert data into a python dict
    mydict = list(req_data.values())
    # call method to predict score
    calculatedScore = predictScore(mydict)
    # return the prediction to front end
    return jsonify(round(calculatedScore[0]))


if __name__ == "__main__":

    app.run(debug=True)
