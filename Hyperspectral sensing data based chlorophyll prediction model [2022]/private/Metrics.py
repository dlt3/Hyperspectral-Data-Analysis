def R2(true, pred) :
  import numpy as np
  sse = ((np.array(true) - np.array(pred))**2).sum()
  ssr = ((np.array(pred) - np.mean(true))**2).sum()
  sst = ((np.array(true) - np.mean(true))**2).sum()
  # r2 = 1 - (sse/sst)
  r2 = ssr/sst
  return np.round(r2, 3)

def MAPE(true, pred) :
  import numpy as np
  mape = np.mean(np.abs((np.array(true) - np.array(pred)) / (np.array(true) + 0.00000001))) * 100
  return np.round(mape, 3)

def RMSE(true, pred) :
  import numpy as np
  mse = np.mean((np.array(true) - np.array(pred))**2)
  rmse = np.sqrt(mse)
  return np.round(rmse, 3)

def MAE(true, pred) :
  import numpy as np
  mae = np.mean(np.abs((np.array(true) - np.array(pred))))
  return np.round(mae, 3)


def R2_OLS(true, pred) :
  import statsmodels.api as sm
  import numpy as np
  const_pred = sm.add_constant(pred, has_constant = "add")
  ols = sm.OLS(true, const_pred).fit()
  return np.round(ols.rsquared, 3)