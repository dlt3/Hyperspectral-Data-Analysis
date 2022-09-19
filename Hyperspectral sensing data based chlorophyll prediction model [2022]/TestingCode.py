import time
from tqdm.notebook import tqdm
from datetime import datetime, timedelta

import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import KFold, GridSearchCV


### Testing code

def HS_categorical_(data) :

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


    # afternoon, evening, morning, non-hs 중 없는 변수 추가
    time = ["afternoon", "evening", "morning", "non-hs"]
    for j in range(len(time)):
        if time[j] not in data.columns:
            data[time[j]] = [0]*data.shape[0]
                
    # spring, summer, fall, winter 중 없는 변수 추가.
    season = ["spring", "summer", "fall", "winter"]
    for i in range(len(season)) :
        if season[i] not in data.columns :
            data[season[i]] = [0]*data.shape[0]

    return data


### 최근 3개 데이터를 이름 붙여 리스트화
def lag_split_(data, lag_term = 3):
    split = []
    for j in range(lag_term):
        globals()["lag_{}".format(j)] = data.iloc[-j]
        split.append(globals()["lag_{}".format(j)])
    return split


### 변수 이름에 lag_{i} 붙이는 함수
def rename(data, lag_term):
    re_split = []
    for i in range(lag_term):
        data[i] = data[i].add_suffix("_lag{}".format(i))
        re_split.append(data[i])
    
    return data


### 데이터 프레임용 변수 이름
def column_set(data, lag_term = 3):
    col_list = []
    for i in range(lag_term):
        col = data.columns + "_lag_" + str(i+1)
        col_list += list(col.values)
    return col_list


### 최근 3개의 데이터를 lag data화
def testlag_(dataset, last_data, lag_term, before_y = "yes"):
    
    if before_y != "yes" :
        dataset = dataset.drop(columns = ['chlorophyll'])
    else :
        pass
    
    lag_data = pd.DataFrame()
    
    dataset = dataset.iloc[-lag_term:, :]
    dataset_ = dataset.iloc[:, 6:]

    split = lag_split_(dataset, lag_term = lag_term)
    re_split = rename(split, lag_term = lag_term)
    col_list = column_set(dataset, lag_term = lag_term)

    fin_data = pd.DataFrame(np.array(re_split).reshape(-1,1).T, columns = col_list)
    date = column_set(last_data.iloc[:, :5], lag_term = lag_term)
    fin_data = fin_data[fin_data.columns.drop(list(fin_data.filter(items = date)))]
    fin_data = pd.concat([last_data.iloc[:, :5] ,fin_data], axis = 1)
        
    now2 = datetime(last_data.iloc[[0]]["Year"], last_data.iloc[[0]]["Month"], last_data.iloc[[0]]["Day"], last_data.iloc[[0]]["Hour"], last_data.iloc[[0]]["Min"])
    now3 = now2 + timedelta(minutes = 15)
    future_time = [now3.year, now3.month, now3.day, now3.hour, now3.minute]
    now_time = pd.DataFrame(future_time, index = ['Year', 'Month', 'Day', 'Hour', 'Min']).T
        
    fin_data = pd.concat([now_time, fin_data.iloc[:, 5:]], axis = 1)
    fin_data = fin_data.iloc[[0],:]    
        
    return fin_data


### lag data를 Train 정보를 통해 변형
def prep_data_with_y(data, train_pls, train_std_other, train_std_reflec, hs = "yes"):
    
    data = HS_categorical_(data)

    weather_ = data.iloc[:, -8:]
    pls_fit = train_pls
    reflect_data = data.filter(regex = 'reflectance')
    
    std_reflec = train_std_reflec
    std_reflect_X = pd.DataFrame(std_reflec.transform(reflect_data), columns = reflect_data.columns).reset_index(drop = True)

    pls_X = pd.DataFrame(pls_fit.transform(reflect_data.to_numpy()), columns = ['comp' + str(i + 1) for i in range(8)]).reset_index(drop = True)
    
    ### weather, water std(std)   
    std_other = train_std_other
    other_ = data[data.columns.drop(list(data.filter(regex = 'reflectance')))]
    t_list = ["afternoon", "evening", "morning", "non-hs", "spring", "summer", "fall", "winter"]
    other_X = other_[other_.columns.drop(list(other_.filter(items = t_list)))]
    
    std_other_X = pd.DataFrame(std_other.transform(other_X.to_numpy()), columns = other_X.columns).reset_index(drop = True)

    test_dataset = pd.concat([pls_X, std_other_X, weather_], axis = 1)
    if hs == "no" :
        test_dataset = test_dataset.drop(columns = test_dataset.filter(regex = "comp"))

    return test_dataset