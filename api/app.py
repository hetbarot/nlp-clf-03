from flask import Flask, request, jsonify, session, render_template

import mlflow.pyfunc
import json

# Name of the apps module package
app = Flask(__name__, template_folder='./material-dashboard', static_folder='./material-dashboard/assets')

# Load in the model at app startup
model = mlflow.pyfunc.load_model('./model')


# Load in our meta_data
# f = open("./model/code/meta_data.txt", "r")
# load_meta_data = json.loads(f.read())


@app.route("/", methods=["GET"])
def main():
    return render_template("dashboard.html")


@app.route("/dashboard.html", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")


@app.route("/calendar.html", methods=["GET"])
def calendar():
    return render_template("calendar.html")


@app.route("/form.html", methods=["GET"])
def form():
    return render_template("form.html")


@app.route("/classify/<string:sentence>", methods=["GET"])
def classify(sentence):
    print(sentence)
    # Get model prediction - convert from np to list
    pred = model.predict([sentence])
    print(pred[0])
    pred = response(pred[0])
    print(pred)
    # Log the prediction
    print({'response': pred})

    # Return prediction as reponse
    return jsonify(pred)


# Meta data endpoint
@app.route('/', methods=['GET'])
def meta_data():
    return "Welcome to the home page"


# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    req = request.get_json()

    data = req['data']
    print(data)

    # Get model prediction - convert from np to list
    pred = model.predict(data).tolist()
    print(pred)
    pred = response(pred)

    print(pred)
    # Log the prediction
    print({'response': pred})

    # Return prediction as reponse
    return jsonify(pred)

def response(i):
    switcher = {
        'ENTY': 'Entities',
        'LOC': 'Location',
        'NUM': 'Numeric values',
        'HUM': 'Human',
        "DESC": 'Description and abstract concepts',
        'ABBR': 'Abbreviation'
    }
    return switcher.get(i)

app.run(host='0.0.0.0', port=5001, debug=True)