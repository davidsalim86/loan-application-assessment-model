import numpy as np 
import pandas as pd
import joblib
from flask import Flask,render_template, redirect, request, session
from sqlalchemy import create_engine, text
from flask_sqlalchemy import SQLAlchemy
import json

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///database/loan_application_data.db")

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

db = SQLAlchemy(app)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index.html")
def returnhome():
    return render_template("index.html")

@app.route("/form.html")
def form():
    return render_template("form.html")

@app.route("/form.html", methods=["POST","GET"])
def result():
    if request.method=="POST":
        array = [x for x in request.form.values()]
        print(input)
        input_df = pd.DataFrame({'business_or_commercial':[array[0]],
                        'loan_amount':[array[1]],
                        'rate_of_interest':[array[2]],
                        'term':[array[3]],
                        'interest_only':[array[4]],
                        'property_value':[array[5]],
                        'income':[array[6]],
                        'credit_score':[array[7]],
                        'age':[array[8]],
                        'ltv':[array[9]],
                        'dtir1':[array[10]]})
        X_scaler = joblib.load('models/X_scaler.sav')
        model = joblib.load('models/rf.sav')    
        scaled_values = X_scaler.transform(np.array(input_df))
        predict = model.predict(scaled_values)
        if predict[0]==1:
            result = "Approved"
        else:
            result = "Not approved"    
    return render_template("form.html",result=result)


@app.route("/pairplot.html")
def compare():
    return render_template("pairplot.html")



# data for chartx
# @app.route("/api/chartx")
# def chartx():
#     database_df = pd.read_sql(f"Select loan_amount, status from loan_data",engine)
#     database_JSON = database_df.to_json(orient = 'records')
#     return database_JSON

if __name__ == "__main__":
    app.run()