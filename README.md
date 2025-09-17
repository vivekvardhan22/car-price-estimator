# 🚗 Car Price Estimator — EDA + Prediction

This project explores **used car sales data** through **Exploratory Data Analysis (EDA)** and builds a simple **price estimation tool** in Python.  
Later, the estimator was wrapped into a web app using Django so that users can input details and instantly get an estimated selling price range.

---

## 📊 Exploratory Data Analysis (EDA)
Key parts of the analysis:
- Cleaned raw data (`car_prices.csv`) (from kaggle) by handling missing values and date formatting.
- Engineered features like:
  - `age` of car
  - `seller_rating` (authorized vs. non-authorized sellers)
  - `reliability` grading based on manufacturer
  - `model_rating` based on outlier performance
- Visualized insights:
  - **Reliability vs Selling Price**
  - **Odometer vs Selling Price**
  - **Car Age vs Selling Price**

Examples of saved plots are available in `/static/estimator/plots/`.

---

## 🔮 Price Estimation Logic
The estimator function takes:
- **Company (make)**
- **Variant (model)**
- **Seller type (authorized / non-authorized)**
- **Odometer reading**
- **Purchase year**

And returns a **min–max price range** by:
- Filtering dataset by make, model, reliability, and seller rating.
- Penalizing price for **high odometer readings** or **older cars**.
- Adjusting based on brand reliability and model performance.

This is not a machine learning model but a **rule-based data-driven estimator** built from EDA.
