import numpy as np
from flask import Flask, request, jsonify
import json
import pickle
#from joblib import dump, load

app = Flask(__name__)

infile1 = open('listsFile', 'rb')
lists = pickle.load(infile1)
infile1.close()


infile2 = open('forestModel', 'rb')
predModel = pickle.load(infile2)
infile2.close()


@app.route('/venues')
def home():
    response = jsonify({"venues": lists.exportVenues,
                        "bowlTeams": lists.exportBowlTeams, "batTeams": lists.exportBatTeams})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# @app.route('/predict', methods=['POST'])
# def predict():

#     int_features = [int(x) for x in request.form.values()]
#     final_features = [np.array(int_features)]
#     prediction = model.predict(final_features)

#     output = round(prediction[0], 2)

#     return render_template('index.html', prediction_text='Sales should be $ {}'.format(output))


# @app.route('/results', methods=['POST'])
# def results():

#     data = request.get_json(force=True)
#     prediction = model.predict([np.array(list(data.values()))])

#     output = prediction[0]
#     return jsonify(output)


if __name__ == "__main__":

    #infile = open(filename, 'rb')
    #forestModel = pickle.load(infile)
    # infile.close()

    #modelfile = 'models/final_prediction.pickle'
    #model = p.load(open(modelfile, 'rb'))
    #app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)
