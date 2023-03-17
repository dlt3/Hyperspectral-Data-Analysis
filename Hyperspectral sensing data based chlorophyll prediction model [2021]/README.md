# Hyperspectral sensing data based chlorophyll prediction model[2021]

### Research purpose
- Prediction of Paldang Dam Chlorophyll-a at the same time using hyperspectral data
- Development of an Chlorophyll-a prediction model that can be continuously updated through real-time water quality data analysis

### Data information
- explanatory variable : Chlorophyll-a
- response variable : Hyperspectral data 550nm ~ 900nm


### Analysis process
- Comparison of using simple data standardization techniques and feature extraction due to the large number of variables, and comparison of regression and machine learning techniques as prediction models
- Data preprocessing
  - Standardization : StandardScaler, MinMaxScaler
  - Feature extraction : Principal Component Analysis(PCA), Partial Least Square(PLS)
- Used prediction model : RandomForest, ExtraTree, GradientBoosting, AdaBoost, KNN, SVM, XGBoost, Ordinary Least Square
- Model performance evaluation metrics : R-square, MSE, MAPE, NSE, d, PSR
- Additional analysis : Identification of significant wavelengths for Chlorophyll-a prediction through feature importance
  
  
