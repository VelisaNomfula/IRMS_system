import xlrd
from bs4 import BeautifulSoup
import requests
from time import sleep

path = "Journals - 20190531.xlsx"

inputWorkbook = xlrd.open_workbook(path)
inputWorksheet = inputWorkbook.sheet_by_index(0)

def DOI(title):
    
    source = requests.get('https://www.researchgate.net/search/publication?q={}'.format(title)).text

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }

    content = BeautifulSoup(source, 'lxml')
    link =  content.findAll('li', class_ = "nova-e-list__item nova-v-publication-item__meta-data-item")[1].span.text
   

    DOI = link[5:]
    tag = link[:3]

    if link[:3] == 'DOI':
        print('Search  on Research gate ')
        return link[5:]
    elif link[:3] != 'DOI':
        print('Not found in Researchgate \n')
        return 'Another Search'



 #print(inputWorksheet.nrows)




for i in range(2, inputWorksheet.nrows-1):
    #print(type(inputWorksheet.cell_value(i, 9)))
    #print(i,"  ", inputWorksheet.cell_value(i, 9))
    if (" " in inputWorksheet.cell_value(i, 9) or inputWorksheet.cell_value(i, 9) == ""):
        print(inputWorksheet.cell_value(i, 3))
        print("DOI: ",i," ",DOI(inputWorksheet.cell_value(i, 3)))
    
    sleep(0.15)





#print(DOI('Early childhood caries and dental treatment need in low socio-economic communities in Cape Town, South Africa'))