from pyexpat import model
from statistics import mode
from typing import final
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
import warnings


# app = Flask(__name__)
# model = pickle.load(open('model.pkl', 'rb'))

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")




@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        Term = float(request.form["Term"])
        BorrowerRate = float(request.form["BorrowerRate"])
        ProsperScore = float(request.form["ProsperScore"])
        CreditScoreRangeUpper = float(request.form["CreditScoreRangeUpper"])
        TotalInquiries = float(request.form["TotalInquiries"])
        CurrentDelinquencies = float(request.form["CurrentDelinquencies"])
        AmountDelinquent = float(request.form["AmountDelinquent"])
        DelinquenciesLast7Years = float(request.form["DelinquenciesLast7Years"])
        PublicRecordsLast10Years = float(request.form["PublicRecordsLast10Years"])
        PublicRecordsLast12Months = float(request.form["PublicRecordsLast12Months"])
        RevolvingCreditBalance = float(request.form["RevolvingCreditBalance"])
        BankcardUtilization = float(request.form["BankcardUtilization"])
        AvailableBankcardCredit = float(request.form["AvailableBankcardCredit"])
        TotalTrades = float(request.form["TotalTrades"])
        TradesOpenedLast6Months = float(request.form["TradesOpenedLast6Months"])
        DebtToIncomeRatio = float(request.form["DebtToIncomeRatio"])
        StatedMonthlyIncome = float(request.form["StatedMonthlyIncome"])
        MonthlyLoanPayment = float(request.form["MonthlyLoanPayment"])
        InvestmentFromFriendsCount = float(request.form["InvestmentFromFriendsCount"])
        Investors = float(request.form["Investors"])

        IsBorrowerHomeowner = request.form['IsBorrowerHomeowner']
        if IsBorrowerHomeowner == 'Yes':
            IsBorrowerHomeowner_Yes = 1
        else:
            IsBorrowerHomeowner_Yes = 0

        EmploymentStatus = request.form['EmploymentStatus']
        if EmploymentStatus == 'Full-time':
            EmploymentStatus_Fulltime = 1
            EmploymentStatus_Notavailable = 0
            EmploymentStatus_Notemployed = 0
            EmploymentStatus_Other = 0
            EmploymentStatus_Parttime = 0
            EmploymentStatus_Retired = 0
            EmploymentStatus_Selfemployed = 0
        elif EmploymentStatus == 'Not available':
            EmploymentStatus_Fulltime = 0
            EmploymentStatus_Notavailable = 1
            EmploymentStatus_Notemployed = 0
            EmploymentStatus_Other = 0
            EmploymentStatus_Parttime = 0
            EmploymentStatus_Retired = 0
            EmploymentStatus_Selfemployed = 0
        elif EmploymentStatus == 'Not employed':
            EmploymentStatus_Fulltime = 0
            EmploymentStatus_Notavailable = 0
            EmploymentStatus_Notemployed = 1
            EmploymentStatus_Other = 0
            EmploymentStatus_Parttime = 0
            EmploymentStatus_Retired = 0
            EmploymentStatus_Selfemployed = 0
        elif EmploymentStatus == 'Other':
            EmploymentStatus_Fulltime = 0
            EmploymentStatus_Notavailable = 0
            EmploymentStatus_Notemployed = 0
            EmploymentStatus_Other = 1
            EmploymentStatus_Parttime = 0
            EmploymentStatus_Retired = 0
            EmploymentStatus_Selfemployed = 0
        elif EmploymentStatus == 'Part-time':
            EmploymentStatus_Fulltime = 0
            EmploymentStatus_Notavailable = 0
            EmploymentStatus_Notemployed = 0
            EmploymentStatus_Other = 0
            EmploymentStatus_Parttime = 1
            EmploymentStatus_Retired = 0
            EmploymentStatus_Selfemployed = 0
        elif EmploymentStatus == 'Retired':
            EmploymentStatus_Fulltime = 0
            EmploymentStatus_Notavailable =0
            EmploymentStatus_Notemployed = 0
            EmploymentStatus_Other = 0
            EmploymentStatus_Parttime = 0
            EmploymentStatus_Retired = 1
            EmploymentStatus_Selfemployed = 0
        elif EmploymentStatus == 'Self-employed':
            EmploymentStatus_Fulltime = 0
            EmploymentStatus_Notavailable = 0
            EmploymentStatus_Notemployed = 0
            EmploymentStatus_Other = 0
            EmploymentStatus_Parttime = 0
            EmploymentStatus_Retired = 0
            EmploymentStatus_Selfemployed = 1
        else :
            EmploymentStatus_Fulltime = 0
            EmploymentStatus_Notavailable = 0
            EmploymentStatus_Notemployed = 0
            EmploymentStatus_Other = 0
            EmploymentStatus_Parttime = 0
            EmploymentStatus_Retired = 0
            EmploymentStatus_Selfemployed = 0

        CurrentlyInGroup = request.form['CurrentlyInGroup']
        if CurrentlyInGroup == 'Yes':
            CurrentlyInGroup_Yes = 1
        else:
            CurrentlyInGroup_Yes = 0

        IncomeRange = request.form['IncomeRange']
        if IncomeRange == '$100,000+':
            IncomeRange_more_than_100000 = 1
            IncomeRange_25000_49999 = 0
            IncomeRange_50000_74999 = 0
            IncomeRange_75000_99999 = 0
            IncomeRange_NotEmployed = 0
            IncomeRange_Notdisclosed = 0
        elif IncomeRange == '$25,000-49,999':
            IncomeRange_more_than_100000 = 0
            IncomeRange_25000_49999 = 1
            IncomeRange_50000_74999 = 0
            IncomeRange_75000_99999 = 0
            IncomeRange_NotEmployed = 0
            IncomeRange_Notdisclosed = 0
        elif IncomeRange == '$50,000-74,999':
            IncomeRange_more_than_100000 = 0
            IncomeRange_25000_49999 = 0
            IncomeRange_50000_74999 = 1
            IncomeRange_75000_99999 = 0
            IncomeRange_NotEmployed = 0
            IncomeRange_Notdisclosed = 0
        elif IncomeRange == '$75,000-99,999':
            IncomeRange_more_than_100000 = 0
            IncomeRange_25000_49999 = 0
            IncomeRange_50000_74999 = 0
            IncomeRange_75000_99999 = 1
            IncomeRange_NotEmployed = 0
            IncomeRange_Notdisclosed = 0
        elif IncomeRange == 'Not Employed':
            IncomeRange_more_than_100000 = 0
            IncomeRange_25000_49999 = 0
            IncomeRange_50000_74999 = 0
            IncomeRange_75000_99999 = 0
            IncomeRange_NotEmployed = 1
            IncomeRange_Notdisclosed = 0
        elif IncomeRange == 'Not disclosed':
            IncomeRange_more_than_100000 = 0
            IncomeRange_25000_49999 = 0
            IncomeRange_50000_74999 = 0
            IncomeRange_75000_99999 = 0
            IncomeRange_NotEmployed = 0
            IncomeRange_Notdisclosed = 1
        else:
            IncomeRange_more_than_100000 = 0
            IncomeRange_25000_49999 = 0
            IncomeRange_50000_74999 = 0
            IncomeRange_75000_99999 = 0
            IncomeRange_NotEmployed = 0
            IncomeRange_Notdisclosed = 0

        features = [
            Term, BorrowerRate, ProsperScore , CreditScoreRangeUpper,
            TotalInquiries, CurrentDelinquencies, AmountDelinquent,
            DelinquenciesLast7Years, PublicRecordsLast10Years,
            PublicRecordsLast12Months, RevolvingCreditBalance,
            BankcardUtilization, AvailableBankcardCredit, TotalTrades,
            TradesOpenedLast6Months, DebtToIncomeRatio, StatedMonthlyIncome,
            MonthlyLoanPayment, InvestmentFromFriendsCount, Investors,
            IsBorrowerHomeowner_Yes,
            EmploymentStatus_Fulltime,
            EmploymentStatus_Notavailable,
            EmploymentStatus_Notemployed,
            EmploymentStatus_Other,
            EmploymentStatus_Parttime,
            EmploymentStatus_Retired,
            EmploymentStatus_Selfemployed, CurrentlyInGroup_Yes,
            IncomeRange_more_than_100000,
            IncomeRange_25000_49999,
            IncomeRange_50000_74999,
            IncomeRange_75000_99999,
            IncomeRange_NotEmployed,
            IncomeRange_Notdisclosed,
        ]
        features1 = [np.array(features)]
        prediction = model.predict(features1)

        if prediction == 0:
            output = 'Low Risk'
        elif prediction == 1:
            output = 'High Risk'

        return render_template('index.html', prediction_text= "Status of the loan is {}".format(output))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)