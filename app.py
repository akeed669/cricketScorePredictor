import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from trainFile import predictScore
import json
import pickle


app = Flask(__name__)
CORS(app)

infile1 = open('listsFile', 'rb')
lists = pickle.load(infile1)
infile1.close()


@app.route('/listdata')
def sendListData():
    response = jsonify({"venues": lists[0],
                        "bowlTeams": lists[2], "batTeams": lists[1]})
    return response


@app.route('/predict', methods=['POST'])
def predict():
    req_data = request.get_json()
    mydict = list(req_data.values())
    calculatedScore = predictScore(mydict)
    return jsonify(round(calculatedScore[0]))


if __name__ == "__main__":

    app.run(debug=True)
