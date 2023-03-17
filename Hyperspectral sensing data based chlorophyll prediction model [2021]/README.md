# Hyperspectral sensing data based chlorophyll prediction model[2021]

### Research purpose
- Prediction of Paldang Dam Chlorophyll-a at the same time using hyperspectral data
- Development of an Chlorophyll-a prediction model that can be continuously updated through real-time water quality data analysis

### Data information
- explanatory variable : Chlorophyll-a
- response variable : Hyperspectral data 550nm ~ 900nm

![image](https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F234ff89f-fcdf-4385-b1d8-e56757189364%2FUntitled.png?id=799b5c0b-80ed-4f8c-a7ef-fdd8ddaec4fe&table=block&spaceId=6cc23a96-8110-4f80-9a0b-4eb515095500&width=2000&userId=e639e6c1-7dd8-4d51-97de-be9ead475dc3&cache=v2
)

### Analysis process
- Comparison of using simple data standardization techniques and feature extraction due to the large number of variables, and comparison of regression and machine learning techniques as prediction models
- Data preprocessing
  - Standardization : StandardScaler, MinMaxScaler
  - Feature extraction : Principal Component Analysis(PCA), Partial Least Square(PLS)
- Used prediction model : RandomForest, ExtraTree, GradientBoosting, AdaBoost, KNN, SVM, XGBoost, Ordinary Least Square
- Model performance evaluation metrics : R-square, MSE, MAPE, NSE, d, PSR
- Additional analysis : Identification of significant wavelengths for Chlorophyll-a prediction through feature importance

![image](https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F99d79070-4a0f-40d5-99c4-1e0224a99968%2FUntitled.png?id=d47391b7-7c72-414c-a5f9-8b249902d377&table=block&spaceId=6cc23a96-8110-4f80-9a0b-4eb515095500&width=2000&userId=e639e6c1-7dd8-4d51-97de-be9ead475dc3&cache=v2)

