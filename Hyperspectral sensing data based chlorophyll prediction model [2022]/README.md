# Hyperspectral sensing data based chlorophyll prediction model[2021]
Reference : In preprocessed

### Research purpose
- Yangpyeong Chlorophyll-a prediction after 15 minutes using hyperspectral data, weather data and water quality data
- Construction of possible pipelines for real-time data

### Data information
- explanatory variable : Chlorophyll-a
- response variable 
  - Hyperspectral data 550nm ~ 900nm
  - Weather data : temperature, humidity, wind speed, wind direction, solar radiation
  - Water quality data : water temperature, water depth, conductivity, turbidity, PH, Phycocyanin

### Analysis process
- Model is updated every midnight, Chlorophyll-a prediction after 15 minutes
- Data problems and solutions
  - The measurement time of hyperspectral, weather, and water quality data is not the same : Data reconstruction based on a certain time
  - Time zone where hyperspectral data does not exist : Express the existence of hyperspectral data as a categorical variable
- Data preprocessing
  - Hyperspectral data : Create Lag dataset
  - Weather data, water quality data : Standardized preprocessing
  - Reatl-time information data : Dimensional reduction through partial least square method(PLS)
  - Season variables : spring, summer, fall, winter
  - Time variables : morning, afternoon, evening, non-hs (time zone without hyperspectral data measured)
- Model verification : Daily R-square, MAPE
- Additional points : Set all processing process of the model as options that can be manipulated (Lag dataset time point, variable preprocessing, usage method and existence, type  of prediction model, use of ensemble)
- Dataset creation process
  - Lag Dataset : A dataset in which response variables are matched with explanatory variables at a previous point in time
    - The range of previous points in time to be matched can be selected (lag_time)
    - It is possible to select whether to use the response variable value at the previous point in time as an explanatory variable
  - Convert time variable to categorical variable
    - Using the Hour variable among the time variables, it is converted into the time when the hyperspectral variable does not enter and the time when the  hyperspectral variable enters
    - Converted into a categoricl variable meaning the season by using the Month variable among the time variables
  - Preprocessing for each dataset converted to lag dataset
    - Reduce the amount of variables using the PLS(Partial Least Square) technique
    - Other (Water quality variables, weather variables) variables are standardized, and time variables are preprocessed through One-Hot encoding.
    

![image](https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F5c6a3f85-1612-427f-ad6c-e9e12e68abfa%2FUntitled.png?id=1bd4ab1e-d0cb-4ea9-a1b8-bc710d23101c&table=block&spaceId=6cc23a96-8110-4f80-9a0b-4eb515095500&width=2000&userId=e639e6c1-7dd8-4d51-97de-be9ead475dc3&cache=v2)


