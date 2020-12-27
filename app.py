from flask import Flask,request, url_for, redirect, render_template, jsonify
import pandas as pd
from pycaret.classification import *
import pickle
import numpy as np
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(42)

pkl_filename = 'models/model_ridge'

model = load_model(pkl_filename)
print('Model loaded: ', model)

cols = ['Gender','Married','Dependents', 'Education', 'Self_Employed', 'ApplicantIncome',
        'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Property_Area']

@app.route('/')

def index():
    return render_template("index.html")

@app.route('/predict',methods=['POST'])


def predict():
    int_features = [x for x in request.form.values()]
    all_feats = np.array(int_features)
    live_data = pd.DataFrame([all_feats], columns = cols)
    prediction = predict_model(model, data=live_data, round = 0)
    prediction = int(prediction.Label[0])
    pred = 'Eligible' if prediction==1 else 'Not Eligible'
    return render_template('index.html',pred='Is the person eligible for loan? {}'.format(pred))

@app.route('/predict_loan_api',methods=['POST'])

def predict_loan_api():
    data = request.get_json(force=True)
    live_data = pd.DataFrame([data])
    prediction = predict_model(model, data=live_data)
    pred = prediction.Label[0]
    return jsonify(pred)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
