# Hyperspectral-Data-Analysis
This study describes how to develop a model to predict chlorophyll-a concentrations utilizing hyperspectral sensor data.

### What is Chlorophyll-a?
Chlorophyll-a is an oxygen compound that plays an important role in photosynthesis in photosynthetic organisms such as plants and algae. The concentration of chlorophyll-a is closely related to environmental changes, such as the growth of photosynthetic organisms and changes in atmospheric CO2 concentration.

### Data collection and preprocessing
In this study, hyperspectral data related to the concentration of chlorophyll-a were collected in the Paldang Dam water system using a hyperspectral sensor. Afterwards, the collected data was processed into a form that can be used for modeling through preprocessing, such as removing unnecessary noise and interpolating missing values.

### Research progress direction and purpose
The study was conducted by dividing it into primary analysis and secondary analysis. In the primary analysis, data analysis received in real time using hyperspectral data was used to develop a current prediction model capable of predicting Paldang Dam Chlorophyll-a and continuously updating at the same time. In the secondary analysis, the purpose was to build a pipeline to predict Chlorophyll-a at 15 minutes using hyperspectral data and meteorological/water quality data.


```bash
├── Hyperspectral-Data-Analysis[2021] 
│   ├── Model_Fitting.ipynb
│   ├── Fitting_result.ipynb
│   └── Paper_code.ipynb
├── Hyperspectral-Data-Analysis[2022]
│   ├── Training_code.ipynb
│   ├── Testing.ipynb  
│   ├── Dataset_code.ipynb
│   └── Prediction_code.ipynb
└── PLS
    └── PLS_components.ipynb
```
