import pandas as pd
import matplotlib.pyplot as mpl
import os

testlist = os.listdir("pq-Gf")
xlslist = []
for file in testlist:
    if file.endswith('xls') and file.find("1024") == -1 and file.find("4096") == -1 and file.find("128") == -1 and file.find("512")==-1 and file.find("2048")==-1:
        xlslist.append(pd.read_excel(io = "pq-Gf/"+file , header=0 , names=["p/q" , file[:-4]] , converters={"p/q":float , file[:-4]:float}))

df = pd.merge(xlslist[0] , xlslist[1] , on="p/q" , how="outer")
for i in range(2 , len(xlslist)):
    df = pd.merge(df , xlslist[i] , on="p/q" , how="outer")

df = df.sort_values(by="p/q")
df.plot(x = "p/q")
mpl.show()
