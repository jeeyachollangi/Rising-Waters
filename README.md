# Rising Waters: A Machine Learning Approach to Flood Prediction

An end-to-end Machine Learning web application designed to predict the likelihood of floods using historical weather, precipitation, and cloud visibility parameters. The application assists disaster management authorities and government agencies in identifying flood risks early, enabling timely evacuation planning and efficient resource allocation.

---

## 🚀 Key Features

*   **Premium Web UI:** Fully responsive, glassmorphic dark-themed interface built using HTML5, CSS3 (with custom variables and animations), and JavaScript.
*   **Meteorological Inputs:** Evaluate risk levels based on Annual Rainfall (mm), Seasonal Rainfall (mm), Cloud Visibility percentage, and custom Weather Parameter Index.
*   **Predictive ML Layer:** Compares four classification models trained on a custom clean dataset:
    *   **Random Forest Classifier** (Best Performer: **90.25% Accuracy**)
    *   **K-Nearest Neighbors (KNN)** (89.75% Accuracy)
    *   **XGBoost Classifier** (88.00% Accuracy)
    *   **Decision Tree Classifier** (84.75% Accuracy)
*   **Auto Model Selector:** The pipeline automatically selects and saves the highest-accuracy model for web application inference.
*   **Prediction Session History:** Displays a dynamic history log of recent calculations performed during the session.
*   **Robust Input Validation:** Server-side and client-side checks ensure high data entry integrity.

---

## 📁 Repository Structure

```text
Rising-Waters/
├── dataset/
│   └── flood.csv                  # Meteorological training dataset
├── models/
│   ├── model.pkl                  # Saved optimal classifier (Random Forest)
│   └── scaler.pkl                 # StandardScaler mapping for inputs
├── notebook/
│   └── Flood_Prediction.ipynb     # Jupyter Notebook detailing steps, EDA & plots
├── static/
│   ├── css/
│   │   └── styles.css             # Glassmorphic, modern CSS style rules
│   ├── js/
│   │   └── main.js               # Frontend validation and micro-interactions
│   └── images/
│       ├── box_plots.png          # Boxplot outlier detection charts
│       ├── correlation_heatmap.png # Correlation matrix visualization
│       ├── count_plot.png         # Target variable class balance plot
│       ├── distribution_plots.png # Feature distribution visualizations
│       └── pair_plot.png          # Pairwise relationships grid
├── templates/
│   ├── index.html                 # Main dashboard landing page
│   ├── predict.html               # Prediction inputs form & history log
│   └── result.html                # Result alerts & hazard guidance
├── app.py                         # Flask application layer (routes & validation)
├── train.py                       # Machine learning pipeline training script
├── requirements.txt               # Dependencies list
├── Procfile                       # Deployment process definition
└── runtime.txt                    # Python environment declaration
```

---

## 🛠️ Installation & Setup (Local)

1.  **Clone or Open the workspace:**
    Ensure you are in the project folder.

2.  **Create a Virtual Environment & Activate:**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute the Training Pipeline:**
    Run this to run preprocessing, generate visual graphs, train all 4 classifiers, and save the best model:
    ```bash
    python train.py
    ```

5.  **Run the Web Application:**
    Start the local server:
    ```bash
    python app.py
    ```
    Open [http://localhost:5000](http://localhost:5000) in your web browser.

---

## ☁️ Deployment Readiness (IBM Cloud)

This project is prepared with the necessary structures for seamless deployment to IBM Cloud Foundry or Code Engine:
*   **`Procfile`**: Specifies the process command: `web: gunicorn app:app`
*   **`runtime.txt`**: Declares the Python execution version.
*   **`requirements.txt`**: Includes production-grade WSGI server (`gunicorn`).

---

## 📈 ML Pipeline & Preprocessing Details

*   **Handling Missing Values:** Missing weather features were imputed using column-wise median values.
*   **Duplicate Records:** 15 identical rows were dropped to prevent overfitting.
*   **Outlier Treatment:** Capped extreme outliers at the $1.5 \times \text{IQR}$ bounds to maintain the data variance structure while smoothing noise.
*   **Scaling:** Features are scaled using `StandardScaler` to ensure optimal performance for K-Nearest Neighbors and tree model conversions.
