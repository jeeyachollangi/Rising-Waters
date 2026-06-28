import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import joblib

app = Flask(__name__)
app.secret_key = "rising_waters_secret_session_key_1298"

# Define paths for models
MODEL_PATH = os.path.join("models", "model.pkl")
SCALER_PATH = os.path.join("models", "scaler.pkl")

# Helper function to check if models are loaded
def load_ml_assets():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        return None, None
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        return model, scaler
    except Exception as e:
        print(f"Error loading models: {e}")
        return None, None

# ----------------------------------------------------
# Route 1: Home Page
# ----------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# ----------------------------------------------------
# Route 2: Prediction Page (GET/POST)
# ----------------------------------------------------
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # Retrieve history from session
    if 'history' not in session:
        session['history'] = []
        
    if request.method == 'POST':
        # Load models
        model, scaler = load_ml_assets()
        if model is None or scaler is None:
            return render_template('predict.html', 
                                   error_msg="Machine Learning models are not available. Please run train.py first.", 
                                   history=session['history'])
        
        try:
            # 1. Retrieve and Parse Inputs
            annual_rainfall_raw = request.form.get('annual_rainfall')
            seasonal_rainfall_raw = request.form.get('seasonal_rainfall')
            cloud_visibility_raw = request.form.get('cloud_visibility')
            meteorological_parameters_raw = request.form.get('meteorological_parameters')
            
            # Input presence check
            if not all([annual_rainfall_raw, seasonal_rainfall_raw, cloud_visibility_raw, meteorological_parameters_raw]):
                return render_template('predict.html', 
                                       error_msg="All form fields are required.", 
                                       history=session['history'])
            
            annual_rainfall = float(annual_rainfall_raw)
            seasonal_rainfall = float(seasonal_rainfall_raw)
            cloud_visibility = float(cloud_visibility_raw)
            meteorological_parameters = float(meteorological_parameters_raw)
            
            # 2. Input Validation Bounds
            errors = []
            if annual_rainfall < 0 or annual_rainfall > 15000:
                errors.append("Annual Rainfall must be between 0 and 15,000 mm.")
            if seasonal_rainfall < 0 or seasonal_rainfall > 10000:
                errors.append("Seasonal Rainfall must be between 0 and 10,000 mm.")
            if seasonal_rainfall > annual_rainfall:
                errors.append("Seasonal Rainfall cannot exceed Annual Rainfall.")
            if cloud_visibility < 0 or cloud_visibility > 100:
                errors.append("Cloud Visibility must be a percentage between 0% and 100%.")
            if meteorological_parameters < 0 or meteorological_parameters > 100:
                errors.append("Weather parameter index must be between 0 and 100.")
                
            if errors:
                return render_template('predict.html', 
                                       error_msg=" | ".join(errors), 
                                       history=session['history'])
            
            # 3. Preprocess and Scale Data
            # Note: Features list in train.py is ['Annual_Rainfall', 'Cloud_Visibility', 'Seasonal_Rainfall', 'Meteorological_Parameters']
            import pandas as pd
            input_features = pd.DataFrame([{
                'Annual_Rainfall': annual_rainfall,
                'Cloud_Visibility': cloud_visibility,
                'Seasonal_Rainfall': seasonal_rainfall,
                'Meteorological_Parameters': meteorological_parameters
            }])
            scaled_features = scaler.transform(input_features)
            
            # 4. Generate Prediction
            prediction_array = model.predict(scaled_features)
            prediction = int(prediction_array[0])
            
            # 5. Save prediction in Session History (limit to 10 records for size)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history_item = {
                'date': timestamp,
                'annual_rainfall': annual_rainfall,
                'cloud_visibility': cloud_visibility,
                'prediction': prediction
            }
            # Append and slice
            history_list = session['history']
            history_list.insert(0, history_item)
            session['history'] = history_list[:10]
            
            # Store latest result parameters to render in /result
            session['latest_prediction'] = {
                'prediction': prediction,
                'inputs': {
                    'annual_rainfall': annual_rainfall,
                    'seasonal_rainfall': seasonal_rainfall,
                    'cloud_visibility': cloud_visibility,
                    'meteorological_parameters': meteorological_parameters
                }
            }
            
            # Redirect to result route (PRG pattern)
            return redirect(url_for('result'))
            
        except ValueError:
            return render_template('predict.html', 
                                   error_msg="Please enter valid numeric values for all parameters.", 
                                   history=session['history'])
        except Exception as e:
            return render_template('predict.html', 
                                   error_msg=f"An error occurred during calculation: {str(e)}", 
                                   history=session['history'])
            
    # GET request
    return render_template('predict.html', history=session['history'])

# ----------------------------------------------------
# Route 3: Result Page
# ----------------------------------------------------
@app.route('/result')
def result():
    latest = session.get('latest_prediction')
    if not latest:
        return redirect(url_for('predict'))
        
    return render_template('result.html', 
                           prediction=latest['prediction'], 
                           inputs=latest['inputs'])

if __name__ == "__main__":
    # Standard Flask port 5000 execution
    app.run(debug=True, host="0.0.0.0", port=5000)
