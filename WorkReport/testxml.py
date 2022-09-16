import xml.etree.ElementTree as ET
import xlrd
import xlwt

xl_read = xlrd.open_workbook("/home/minami/Download/包列表.xls")
xl_write = xlwt.Workbook(encoding="UTF-8")
tree = ET.parse('/home/minami/Download/fedora38.xml')
root = tree.getroot()
groups = root.findall('group')
libs = {}
worksheet = xl_read.sheet_by_index(0)
sheet = xl_write.add_sheet(sheetname="test1" , cell_overwrite_ok=True)
line = 0
r=0
for item in worksheet.row(0):
    sheet.write(0 , line , item.value)
    line+=1
for item in worksheet.col(0):
    sheet.write(r , 0 , item.value)
    r+=1
temp = [set() for i in range(worksheet.nrows)]


for group in groups:
    packlistName = group.find('_name').text
    for p in group.find("packagelist").findall("packagereq"):
        packname = p.text
        libs[packlistName] = libs.get(packlistName , set())
        libs[packlistName].add(packname)
        head = packname.split('-')[0]
        libs[packlistName].add(head)
        for i in range(1 , worksheet.nrows):
            if worksheet.cell_value(i , 0) in libs[packlistName]:
                temp[i].add(packlistName)

for i in range(1 , worksheet.nrows):
    res = "\n".join(list(temp[i]))
    sheet.write(i , 1 , res)

xl_write.save("/home/minami/Download/test.xls")