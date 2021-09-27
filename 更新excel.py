import pandas as pd
import json
import time
path="gzh.csv"
df=pd.read_csv(path,index_col="stu_name")
print(df)
