import pandas as pd
import matplotlib.pyplot as mpl
import os

###
testlist = os.listdir("N-Gf")
xlslist = []
for file in testlist:
    if file.endswith('xls') and file.find("p,q=1,1") != -1:
        xlslist.append(pd.read_excel(io = "N-Gf/"+file , header=0 , names=["N" , file[3:-4]] , converters={"N":float , file[3:-4]:float}))

df = pd.merge(xlslist[0] , xlslist[1] , on="N" , how="outer")
for i in range(2 , len(xlslist)):
    df = pd.merge(df , xlslist[i] , on="N" , how="outer")
#df = pd.read_excel(io = "N-Gf/anap,q=1,1 NB=256.xls" , header=0 , names=["N" , "p,q=1,1 NB=256"] , converters={"N":float , "p,q=1,1 NB=256":float})

df = df.sort_values(by="N")
df.plot(x = "N")
mpl.show()
