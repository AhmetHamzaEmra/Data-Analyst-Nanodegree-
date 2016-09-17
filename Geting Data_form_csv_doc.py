import unicodecsv
import os
path = 'C:\\Users\\aemra\\Documents\\Python\\Untitled Folder'
os.chdir(path)
enrollments=[]
f=open('enrollments.csv','rb')
reader=unicodecsv.DictReader(f)

for row in reader:
    enrollments.append(row)
    
f.close()

enrollments[0]
