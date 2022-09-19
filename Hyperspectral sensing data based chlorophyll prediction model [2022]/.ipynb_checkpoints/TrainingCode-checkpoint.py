import time
from tqdm.notebook import tqdm
from datetime import datetime, timedelta

import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import KFold, GridSearchCV


### Training code

def HS_lag (data, lag_term = 3, before_y = "yes", target = "chlorophyll") :
    
    lag_data = data[[target, "Year", "Month", "Day", "Hour", "Min"]]
    
    if before_y == "yes" :
        data2 = data.drop(columns = ["Year", "Month", "Day", "Hour", "Min"])
    else :
        data2 = data.drop(columns = [target, "Year", "Month", "Day", "Hour", "Min"])
    
    # lag_data 생성
    for i in range(1, lag_term+1) : 
        lag = data2.shift(i)
        lag.columns = lag.columns + "_lag_" + str(i)
        lag_data = pd.concat([lag_data, lag], axis = 1)

    lag_data = lag_data.iloc[lag_term :].reset_index(drop = True)  
    
    return lag_data


def HS_categorical (data) :

    ### 불필요한 변수 제거
    data = data.drop(columns = ["Year", "Day", "Min"])
    
    ### HS time from Hour -> "hs" or "non hs"
    morning = [10,11,12]   ;   afternoon = [13,14,15]   ;   evening = [16,17]
    
    x = data["Hour"].astype("int")
    condlist = [x.isin(morning), x.isin(afternoon), x.isin(evening)]
    choicelist = ["morning", "afternoon", "evening"]
    data["HS time"] = np.select(condlist, choicelist, "non-hs")
    data.drop(columns = "Hour", inplace = True)

    # HS time -> One-Hot encodint
    encode_hs_time = pd.get_dummies(data["HS time"], sparse = True)
    data = pd.concat([data.drop(columns = "HS time"), encode_hs_time], axis = 1)

    

    ### Season from Month -> "sprin, summer, fall, winter"
    spring = [3,4,5]   ;   summer = [6,7,8]   ;   fall = [9,10,11]
    
    y = data["Month"].astype("int")
    condlist = [y.isin(spring), y.isin(summer), y.isin(fall)]
    choicelist = ["spring", "summer", "fall"]
    data["season"] = np.select(condlist, choicelist, "winter")
    data.drop(columns = "Month", inplace = True)

    # Season -> One-Hot encodint
    encode_season = pd.get_dummies(data["season"], sparse = True)
    data = pd.concat([data.drop(columns = "season"), encode_season], axis = 1)


    # spring, summer, fall, winter 중 없는 변수 추가.
    season = ["spring", "summer", "fall", "winter"]
    for i in range(len(season)) :
        if season[i] not in data.columns :
            data[season[i]] = [0]*data.shape[0]

    return data


def HS_train (train_X, train_y, comp = 8) :
    
    ### 변수 구분
    category = ["spring", "summer", "fall", "winter", "morning", "afternoon", "evening", "non-hs"]
    category_X = train_X[category]
    reflec_X = train_X.filter(regex = "reflectance")
    other_X = train_X.drop(columns = (list(reflec_X.columns) + category))
    
    
    ### 표준화
    std_other = StandardScaler().fit(other_X)
    std_other_X = pd.DataFrame(std_other.transform(other_X), columns = other_X.columns).reset_index(drop = True)

    std_reflec = StandardScaler().fit(reflec_X)
    std_reflec_X = pd.DataFrame(std_reflec.transform(reflec_X), columns = reflec_X.columns).reset_index(drop = True)

    std_y = (train_y - train_y.mean())/train_y.std()


    ### PLS
    pls_fit = PLSRegression(n_components = comp).fit(std_reflec_X, std_y)
    pls_X = pd.DataFrame(pls_fit.transform(std_reflec_X), columns = ["comp" + str(i+1) for i in range(comp)]).reset_index(drop = True)

    new_train_X = pd.concat([std_other_X, pls_X, category_X], axis = 1)
    
    
    return {"new train X" : new_train_X, "pls" : pls_fit, "std other" : std_other, "std reflec" : std_reflec}    


def HS_model (data, MODEL, lag_term = 3, comp = 8, SEED = 999, before_y = "yes", hs = "yes", target = "chlorophyll") :
    
    lag_data = HS_lag(data, lag_term = lag_term, before_y = before_y, target = target)
    categorical_data = HS_categorical(lag_data)
    
    train_X = categorical_data.drop([target], axis = 1)
    train_y = categorical_data[target]
    
    Train = HS_train(train_X, train_y, comp)
    
    new_train_X = Train["new train X"]
    if hs == "no" :
        new_train_X = new_train_X.drop(columns = new_train_X.filter(regex = "comp"))
        
    train_columns = new_train_X.columns
    train_pls = Train["pls"]
    train_std_other = Train["std other"]
    train_std_reflec = Train["std reflec"]
    
    model = MODEL.fit(new_train_X, np.ravel(train_y))
    

    return {"model" : model, "train pls" : train_pls, "train std other" : train_std_other, "train std reflec" : train_std_reflec, "train columns" : train_columns}


def HS_model_grid (data, MODEL, param_grid, lag_term = 3, comp = 8, SEED = 999, before_y = "yes", target = "chlorophyll") :
    
    lag_data = HS_lag(data, lag_term = lag_term, before_y = before_y, target = target)
    categorical_data = HS_categorical(lag_data)
    
    train_X = categorical_data.drop([target], axis = 1)
    train_y = categorical_data[target]
    
    Train = HS_train(train_X, train_y, comp)
    
    new_train_X = Train["new train X"]
    train_columns = new_train_X.columns
    train_pls = Train["pls"]
    train_std_other = Train["std other"]
    train_std_reflec = Train["std reflec"]
    
    
    gcv = GridSearchCV(MODEL,      
                       param_grid = param_grid,  
                       cv = KFold(n_splits = 5, random_state = 999, shuffle = True),
                       scoring = "r2",
                       n_jobs = -1)

    gcv.fit(new_train_X, np.ravel(train_y))
 
    model = gcv.best_estimator_ 
    

    return {"model" : model, "train pls" : train_pls, "train std other" : train_std_other, "train std reflec" : train_std_reflec, "train columns" : train_columns}
