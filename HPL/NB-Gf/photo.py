import pandas as pd
import matplotlib.pyplot as mpl
import os

testlist = os.listdir("NB-Gf")
xlslist = []
for file in testlist:
    if file.endswith('xls') and file.find("64") == -1:
        xlslist.append(pd.read_excel(io = "NB-Gf/"+file , header=0 , names=["NB" , file[3:-4]] , converters={"NB":float , file[:-4]:float}))

df = pd.merge(xlslist[0] , xlslist[1] , on="NB" , how="outer")
for i in range(2 , len(xlslist)):
    df = pd.merge(df , xlslist[i] , on="NB" , how="outer")

df = df.sort_values(by="NB")
df.plot(x = "NB")
mpl.show()
