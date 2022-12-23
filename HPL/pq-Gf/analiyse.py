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
                n = datalist[1]
                pq = float(datalist[3])/float(datalist[4])
                sheet[datalist[1]] = sheet.get(datalist[1] , {})
                sheet[n][datalist[2]] = sheet[n].get(datalist[2] , {})
                sheet[n][datalist[2]][pq] = sheet[n][datalist[2]].get(datalist[3]+'/'+datalist[4] , [0.0 , 0])
                sheet[n][datalist[2]][pq][0] += float(datalist[6])
                sheet[n][datalist[2]][pq][1] += 1
            conut += 1
        for n , sheet1 in sheet.items():
            for (key , val) in sheet1.items():
                workbook =  xlwt.Workbook()
                work_sheet = workbook.add_sheet("N="+n+" "+"NB="+key)
                work_sheet.write(0 , 0 , "p/q")
                work_sheet.write(0 , 1 , "Gflops")
                i = 1
                for pq , Gf in val.items():
                    work_sheet.write(i , 0 , str(pq))
                    work_sheet.write(i , 1 , str(Gf[0]/Gf[1]))
                    i += 1
                workbook.save("pq-Gf/ana"+"N="+n+" "+"NB="+key+".xls")
