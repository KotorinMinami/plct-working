import os
import xlwt

logs = os.listdir("logs")

for log in logs:
    with open("logs/"+log , "r") as f:
        sheet = {}
        conut = 3
        for line in f.readlines():
            if line.find("Gflops") != -1:
                if line.find("T/V") != -1:
                    conut = 0
            if conut == 2:
                datalist = [ data.strip() for data in line.split()]
                pq = datalist[3]+'/'+datalist[4]
                sheet[pq] = sheet.get(pq , {})
                sheet[pq][datalist[2]] = sheet[pq].get(datalist[2] , {})
                sheet[pq][datalist[2]][datalist[1]] = sheet[pq][datalist[2]].get(datalist[1] , [0.0 , 0])
                sheet[pq][datalist[2]][datalist[1]][0] += float(datalist[6])
                sheet[pq][datalist[2]][datalist[1]][1] += 1
            conut += 1
        for pq , sheet1 in sheet.items():
            for (key , val) in sheet1.items():
                workbook =  xlwt.Workbook()
                work_sheet = workbook.add_sheet("p,q="+pq[0]+","+pq[2]+" "+"NB="+key)
                work_sheet.write(0 , 0 , "N")
                work_sheet.write(0 , 1 , "Gflops")
                i = 1
                for nb , Gf in val.items():
                    work_sheet.write(i , 0 , nb)
                    work_sheet.write(i , 1 , str(Gf[0]/Gf[1]))
                    i += 1
                workbook.save("N-Gf/ana"+"p,q="+pq[0]+","+pq[2]+" "+"NB="+key+".xls")