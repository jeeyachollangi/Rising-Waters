import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from joblib import load

# Initialize Flask app
app = Flask(__name__)

# Load model and scaler from root directory as specified in PDF
try:
    model = load('floods.save')
    sc = load('transform.save')
    print("Successfully loaded model (floods.save) and scaler (transform.save)")
except Exception as e:
    model, sc = None, None
    print(f"Error loading model assets from root directory: {e}")

# Helper to verify models are loaded
def check_assets():
    global model, sc
    if model is None or sc is None:
        try:
            model = load('floods.save')
            sc = load('transform.save')
        except Exception:
            return False
    return True

# ----------------------------------------------------
# Route 1: Home Page (home.html)
# ----------------------------------------------------
@app.route('/')
def home():
    return render_template('home.html')

# ----------------------------------------------------
# Route 2: Predict Input Form (index.html) (GET) and Submission (POST)
# ----------------------------------------------------
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if not check_assets():
            return render_template('index.html', error_msg="Prediction models are not loaded. Run train.py first.")
            
        try:
            # 1. Retrieve inputs from form
            cloud_cover_raw = request.form.get('cloud_cover')
            annual_raw = request.form.get('annual_rainfall')
            jan_feb_raw = request.form.get('jan_feb')
            mar_may_raw = request.form.get('mar_may')
            jun_sep_raw = request.form.get('jun_sep')
            
            # Form check
            if not all([cloud_cover_raw, annual_raw, jan_feb_raw, mar_may_raw, jun_sep_raw]):
                return render_template('index.html', error_msg="All meteorological parameters must be provided.")
            
            # Convert to floats
            cloud_cover = float(cloud_cover_raw)
            annual = float(annual_raw)
            jan_feb = float(jan_feb_raw)
            mar_may = float(mar_may_raw)
            jun_sep = float(jun_sep_raw)
            
            # Simple logical checks
            errors = []
            if cloud_cover < 0 or cloud_cover > 100:
                errors.append("Cloud Cover must be between 0% and 100%.")
            if annual < 0 or annual > 20000:
                errors.append("Annual Rainfall must be between 0 and 20,000 mm.")
            if jan_feb < 0 or mar_may < 0 or jun_sep < 0:
                errors.append("Rainfall values cannot be negative.")
            if (jan_feb + mar_may + jun_sep) > annual:
                errors.append("Sum of seasonal rainfall cannot exceed Annual Rainfall.")
                
            if errors:
                return render_template('index.html', error_msg=" | ".join(errors))
            
            # 2. Structure into DataFrame matching train.py order
            input_df = pd.DataFrame([{
                'Cloud Cover': cloud_cover,
                'ANNUAL': annual,
                'Jan-Feb': jan_feb,
                'Mar-May': mar_may,
                'Jun-Sep': jun_sep
            }])
            
            # 3. Transform and predict
            scaled_features = sc.transform(input_df)
            prediction = int(model.predict(scaled_features)[0])
            
            # 4. Render intermediate loading page
            if prediction == 1:
                dest = url_for('chance')
            else:
                dest = url_for('no_chance')
            return render_template('loading.html', redirect_url=dest)
                
        except ValueError:
            return render_template('index.html', error_msg="Please enter valid numerical values for all parameters.")
        except Exception as e:
            return render_template('index.html', error_msg=f"An error occurred during prediction: {str(e)}")
            
    # GET request: render the form template
    return render_template('index.html')

# ----------------------------------------------------
# Route 3: Chance of Flood (chance.html)
# ----------------------------------------------------
@app.route('/chance')
def chance():
    return render_template('chance.html')

# ----------------------------------------------------
# Route 4: No Chance of Flood (no_chance.html)
# ----------------------------------------------------
@app.route('/no_chance')
def no_chance():
    return render_template('no_chance.html')

if __name__ == '__main__':
    # Standard Flask listener
    app.run(debug=True, port=5000)
