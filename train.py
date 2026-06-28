import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving charts
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

def main():
    print("=" * 60)
    print("Starting Machine Learning Pipeline for Rising Waters Project")
    print("=" * 60)
    
    # Define paths
    dataset_path = "dataset/flood.csv"
    models_dir = "models"
    images_dir = os.path.join("static", "images")
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    # ----------------------------------------------------
    # 1. Load Dataset
    # ----------------------------------------------------
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at {dataset_path}. Please run generate_data.py first.")
        
    df = pd.read_csv(dataset_path)
    print(f"Dataset Loaded Successfully.")
    print(f"Shape of Dataset: {df.shape}")
    print("\nDataset Info Summary:")
    print(df.info())
    print("\nDescriptive Statistics:")
    print(df.describe())
    
    # ----------------------------------------------------
    # 2. Preprocessing & Data Cleaning
    # ----------------------------------------------------
    print("\n--- Data Preprocessing ---")
    
    # Check for missing values
    missing = df.isnull().sum()
    print("Missing values before imputation:")
    print(missing)
    
    # Impute missing values with median
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"Imputed missing values in '{col}' with median: {median_val:.2f}")
            
    # Check for duplicates
    duplicates_count = df.duplicated().sum()
    print(f"Duplicate records found: {duplicates_count}")
    if duplicates_count > 0:
        df = df.drop_duplicates().reset_index(drop=True)
        print("Duplicate records removed successfully.")
        print(f"New shape after removing duplicates: {df.shape}")
        
    # Outlier treatment using Boxplot bounds (IQR method)
    # We will identify outliers and cap them to 1.5 * IQR to preserve data shape while removing noise.
    features = ['Annual_Rainfall', 'Cloud_Visibility', 'Seasonal_Rainfall', 'Meteorological_Parameters']
    
    print("\nOutlier Detection & Treatment:")
    for feature in features:
        q1 = df[feature].quantile(0.25)
        q3 = df[feature].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers = df[(df[feature] < lower_bound) | (df[feature] > upper_bound)]
        print(f"Feature '{feature}': Found {len(outliers)} outliers (Bounds: {lower_bound:.2f} to {upper_bound:.2f})")
        
        # Cap outliers
        df[feature] = np.clip(df[feature], lower_bound, upper_bound)
        print(f"  --> Capped outliers in '{feature}' to bounds [{lower_bound:.2f}, {upper_bound:.2f}]")
        
    # ----------------------------------------------------
    # 3. Exploratory Data Analysis (EDA) Visualizations
    # ----------------------------------------------------
    print("\n--- Generating EDA Visualizations ---")
    sns.set_theme(style="whitegrid")
    
    # Chart 1: Box Plots for Outlier / Distribution Check
    plt.figure(figsize=(12, 6))
    for i, feature in enumerate(features, 1):
        plt.subplot(2, 2, i)
        sns.boxplot(y=df[feature], color='#3a86c8')
        plt.title(f'Box Plot of {feature}')
    plt.tight_layout()
    box_plot_path = os.path.join(images_dir, 'box_plots.png')
    plt.savefig(box_plot_path, dpi=150)
    plt.close()
    print(f"Saved: {box_plot_path}")
    
    # Chart 2: Correlation Matrix Heatmap
    plt.figure(figsize=(8, 6))
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='Blues', fmt='.2f', linewidths=0.5, cbar=True)
    plt.title('Correlation Matrix Heatmap')
    plt.tight_layout()
    heatmap_path = os.path.join(images_dir, 'correlation_heatmap.png')
    plt.savefig(heatmap_path, dpi=150)
    plt.close()
    print(f"Saved: {heatmap_path}")
    
    # Chart 3: Histograms & Distribution Plots
    plt.figure(figsize=(12, 8))
    for i, feature in enumerate(features, 1):
        plt.subplot(2, 2, i)
        sns.histplot(df[feature], kde=True, color='#2a9d8f')
        plt.title(f'Distribution of {feature}')
    plt.tight_layout()
    dist_plot_path = os.path.join(images_dir, 'distribution_plots.png')
    plt.savefig(dist_plot_path, dpi=150)
    plt.close()
    print(f"Saved: {dist_plot_path}")
    
    # Chart 4: Count Plot for Target Variable
    plt.figure(figsize=(6, 5))
    sns.countplot(x='Flood', data=df, palette='Blues')
    plt.title('Distribution of Target Variable (Flood)')
    plt.xticks(ticks=[0, 1], labels=['No Flood (0)', 'Flood (1)'])
    plt.tight_layout()
    count_plot_path = os.path.join(images_dir, 'count_plot.png')
    plt.savefig(count_plot_path, dpi=150)
    plt.close()
    print(f"Saved: {count_plot_path}")
    
    # Chart 5: Pair Plot
    # We use a subset of rows if it takes too long, but with 2000 rows it's relatively quick
    pair_grid = sns.pairplot(df, hue='Flood', diag_kind='kde', palette='coolwarm')
    pair_plot_path = os.path.join(images_dir, 'pair_plot.png')
    pair_grid.savefig(pair_plot_path, dpi=150)
    plt.close()
    print(f"Saved: {pair_plot_path}")

    # ----------------------------------------------------
    # 4. Feature Scaling & Train-Test Split
    # ----------------------------------------------------
    print("\n--- Train-Test Split & Scaling ---")
    X = df[features]
    y = df['Flood']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    print(f"Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save the scaler
    scaler_path = os.path.join(models_dir, 'scaler.pkl')
    joblib.dump(scaler, scaler_path)
    print(f"StandardScaler saved to: {scaler_path}")
    
    # ----------------------------------------------------
    # 5. Model Training, Evaluation, and Comparison
    # ----------------------------------------------------
    print("\n--- Training Machine Learning Classification Models ---")
    
    models = {
        'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=6),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100, max_depth=8),
        'KNN': KNeighborsClassifier(n_neighbors=7),
        'XGBoost': XGBClassifier(random_state=42, n_estimators=100, max_depth=5, learning_rate=0.08, eval_metric='logloss')
    }
    
    comparison_results = []
    trained_models = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train_scaled, y_train)
        
        # Predictions
        y_pred = model.predict(X_test_scaled)
        
        # Evaluation
        acc = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        print(f"Accuracy Score: {acc * 100:.2f}%")
        print("Confusion Matrix:")
        print(cm)
        print("Classification Report:")
        print(report)
        
        comparison_results.append({
            'Model': name,
            'Accuracy': acc * 100
        })
        trained_models[name] = (model, acc)
        
    # Print Comparison Table
    print("\n" + "="*40)
    print("          MODEL COMPARISON TABLE")
    print("="*40)
    print(f"{'Model':<20} | {'Accuracy':<10}")
    print("-" * 40)
    for res in comparison_results:
        print(f"{res['Model']:<20} | {res['Accuracy']:.2f}%")
    print("="*40)
    
    # ----------------------------------------------------
    # 6. Select and Save the Best Model
    # ----------------------------------------------------
    best_model_name = max(comparison_results, key=lambda x: x['Accuracy'])['Model']
    best_model, best_accuracy = trained_models[best_model_name]
    
    print(f"\n--> Selecting the Best Model: {best_model_name} with Accuracy: {best_accuracy * 100:.2f}%")
    
    model_path = os.path.join(models_dir, 'model.pkl')
    joblib.dump(best_model, model_path)
    print(f"Best Model saved as: {model_path}")
    print("\nPipeline execution completed successfully.")
    print("=" * 60)

if __name__ == "__main__":
    main()
