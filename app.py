import pickle
import numpy as np
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Load the trained model
with open('logistic_pro.pkl', 'rb') as f:
    model = pickle.load(f)

# HTML template with modern CSS styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loan Eligibility Predictor</title>
    <style>
        :root {
            --primary: #0284c7;
            --primary-hover: #0369a1;
            --bg-gradient: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            --card-bg: #ffffff;
            --text-color: #0f172a;
            --border-color: #cbd5e1;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-gradient);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            background: var(--card-bg);
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
            width: 100%;
            max-width: 650px;
        }

        h2 {
            margin-top: 0;
            color: var(--primary);
            text-align: center;
            font-size: 28px;
            margin-bottom: 25px;
        }

        .form-group {
            margin-bottom: 18px;
        }

        label {
            display: block;
            margin-bottom: 6px;
            font-weight: 600;
            font-size: 13px;
            color: #334155;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        input, select {
            width: 100%;
            padding: 11px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-size: 15px;
            box-sizing: border-box;
            transition: border-color 0.3s, box-shadow 0.3s;
        }

        input:focus, select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15);
        }

        .row {
            display: flex;
            gap: 15px;
        }

        .row .form-group {
            flex: 1;
        }

        button {
            width: 100%;
            background-color: var(--primary);
            color: white;
            padding: 14px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.1s;
            margin-top: 10px;
        }

        button:hover {
            background-color: var(--primary-hover);
        }

        button:active {
            transform: scale(0.98);
        }

        .result-card {
            margin-top: 25px;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }

        .approved {
            background-color: #dcfce7;
            border-left: 5px solid #22c55e;
            color: #166534;
        }

        .rejected {
            background-color: #fee2e2;
            border-left: 5px solid #ef4444;
            color: #991b1b;
        }

        .result-card h3 {
            margin: 0 0 5px 0;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Loan Eligibility Checker</h2>
        <form method="POST">
            <div class="row">
                <div class="form-group">
                    <label for="Gender">Gender (1: Male, 0: Female)</label>
                    <select id="Gender" name="Gender" required>
                        <option value="1">Male</option>
                        <option value="0">Female</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="Married">Married (1: Yes, 0: No)</label>
                    <select id="Married" name="Married" required>
                        <option value="1">Yes</option>
                        <option value="0">No</option>
                    </select>
                </div>
            </div>

            <div class="row">
                <div class="form-group">
                    <label for="Dependents">Dependents (0, 1, 2, 3+)</label>
                    <input type="number" id="Dependents" name="Dependents" required placeholder="e.g. 0">
                </div>
                <div class="form-group">
                    <label for="Education">Education (1: Graduate, 0: Not)</label>
                    <select id="Education" name="Education" required>
                        <option value="1">Graduate</option>
                        <option value="0">Not Graduate</option>
                    </select>
                </div>
            </div>

            <div class="row">
                <div class="form-group">
                    <label for="Self_Employed">Self Employed (1: Yes, 0: No)</label>
                    <select id="Self_Employed" name="Self_Employed" required>
                        <option value="0">No</option>
                        <option value="1">Yes</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="Credit_History">Credit History (1 or 0)</label>
                    <input type="number" step="1" id="Credit_History" name="Credit_History" required placeholder="e.g. 1">
                </div>
            </div>

            <div class="row">
                <div class="form-group">
                    <label for="ApplicantIncome">Applicant Income</label>
                    <input type="number" id="ApplicantIncome" name="ApplicantIncome" required placeholder="e.g. 5000">
                </div>
                <div class="form-group">
                    <label for="CoapplicantIncome">Coapplicant Income</label>
                    <input type="number" step="0.01" id="CoapplicantIncome" name="CoapplicantIncome" required placeholder="e.g. 0">
                </div>
            </div>

            <div class="row">
                <div class="form-group">
                    <label for="LoanAmount">Loan Amount</label>
                    <input type="number" id="LoanAmount" name="LoanAmount" required placeholder="e.g. 150">
                </div>
                <div class="form-group">
                    <label for="Loan_Amount_Term">Loan Term (Months)</label>
                    <input type="number" id="Loan_Amount_Term" name="Loan_Amount_Term" required placeholder="e.g. 360">
                </div>
            </div>

            <div class="form-group">
                <label for="Property_Area">Property Area (Encoded: 0, 1, 2)</label>
                <input type="number" id="Property_Area" name="Property_Area" required placeholder="e.g. 2">
            </div>

            <button type="submit">Check Eligibility</button>
        </form>

        {% if prediction is not none %}
        <div class="result-card {% if prediction == 1 %}approved{% else %}rejected{% endif %}">
            <h3>Prediction Result</h3>
            <p style="font-size: 20px; font-weight: bold; margin: 0;">
                {% if prediction == 1 %}
                    Congratulations! Your Loan is Likely Approved.
                {% else %}
                    Sorry, Your Loan Application May Be Rejected.
                {% endif %}
            </p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        try:
            # Extract inputs in the exact order trained by the model
            features = np.array([[
                float(request.form['Gender']),
                float(request.form['Married']),
                float(request.form['Dependents']),
                float(request.form['Education']),
                float(request.form['Self_Employed']),
                float(request.form['ApplicantIncome']),
                float(request.form['CoapplicantIncome']),
                float(request.form['LoanAmount']),
                float(request.form['Loan_Amount_Term']),
                float(request.form['Credit_History']),
                float(request.form['Property_Area'])
            ]])
            
            # Predict
            prediction = int(model.predict(features)[0])
        except Exception as e:
            print(f"Error during prediction: {e}")

    return render_template_string(HTML_TEMPLATE, prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
