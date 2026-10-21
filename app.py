import pickle
import numpy as np
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Load the trained model
with open('linear_pro.pkl', 'rb') as f:
    model = pickle.load(f)

# HTML template with embedded modern CSS styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Insurance Cost Predictor</title>
    <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --bg-gradient: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            --card-bg: #ffffff;
            --text-color: #1f2937;
            --border-color: #d1d5db;
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
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 550px;
        }

        h2 {
            margin-top: 0;
            color: var(--primary);
            text-align: center;
            font-size: 28px;
            margin-bottom: 25px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            font-size: 14px;
        }

        input, select {
            width: 100%;
            padding: 12px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-size: 16px;
            box-sizing: border-box;
            transition: border-color 0.3s, box-shadow 0.3s;
        }

        input:focus, select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
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
            background-color: #e0e7ff;
            border-radius: 8px;
            text-align: center;
            border-left: 5px solid var(--primary);
        }

        .result-card h3 {
            margin: 0 0 8px 0;
            color: #312e81;
            font-size: 16px;
        }

        .prediction-value {
            font-size: 26px;
            font-weight: bold;
            color: var(--primary);
            margin: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Insurance Cost Predictor</h2>
        <form method="POST">
            <div class="row">
                <div class="form-group">
                    <label for="age">Age</label>
                    <input type="number" id="age" name="age" required placeholder="e.g. 30">
                </div>
                <div class="form-group">
                    <label for="sex">Sex</label>
                    <select id="sex" name="sex" required>
                        <option value="1">Male</option>
                        <option value="0">Female</option>
                    </select>
                </div>
            </div>

            <div class="form-group">
                <label for="bmi">BMI (Body Mass Index)</label>
                <input type="number" step="0.1" id="bmi" name="bmi" required placeholder="e.g. 24.5">
            </div>

            <div class="row">
                <div class="form-group">
                    <label for="children">Children</label>
                    <input type="number" id="children" name="children" required placeholder="e.g. 2">
                </div>
                <div class="form-group">
                    <label for="smoker">Smoker</label>
                    <select id="smoker" name="smoker" required>
                        <option value="1">Yes</option>
                        <option value="0">No</option>
                    </select>
                </div>
            </div>

C           <div class="form-group">
                <label for="region">Region (Encoded Index)</label>
                <input type="number" id="region" name="region" required placeholder="e.g. 0 to 3">
            </div>

            <button type="submit">Calculate Prediction</button>
        </form>

        {% if prediction is not none %}
        <div class="result-card">
            <h3>Estimated Charges</h3>
            <p class="prediction-value">${{ "%.2f"|format(prediction) }}</p>
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
            # Extract inputs matching your model's features: age, sex, bmi, children, smoker, region
            age = float(request.form['age'])
            sex = float(request.form['sex'])
            bmi = float(request.form['bmi'])
            children = float(request.form['children'])
            smoker = float(request.form['smoker'])
            region = float(request.form['region'])

            # Create feature array
            features = np.array([[age, sex, bmi, children, smoker, region]])
            
            # Predict
            prediction = float(model.predict(features)[0])
        except Exception as e:
            print(f"Error during prediction: {e}")

    return render_template_string(HTML_TEMPLATE, prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
