import pandas as pd
idx = 1
pvdf = pd.read_csv('data/PV.csv')
demanddf = pd.read_csv('data/pattern2.csv')
demanddf_pertner = pd.read_csv('data/pattern3.csv')
pv_pertner:float = pvdf.at[idx, 'PV']
pvdf = 
print(pv_pertner)