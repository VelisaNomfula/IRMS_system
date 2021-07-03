from bs4 import BeautifulSoup
import requests
import xlrd

import pymongo
from pymongo import MongoClient


class Publication:
    def __init__(self, author = "No Author" , Pub_Year =  "Year Missing", title = "Title missing" , vol = "Volume missing", AuthorCount = "Author count missing", Publisher = "Publisher  not found", IssueNo = "None", DOI  = "None", TypeOfPub = "None"):
        self.author = author
        self.Pub_Year = Pub_Year
        self.title = title
        self.vol = vol
        self.AuthorCount = AuthorCount
        self.Publisher  = Publisher
        self.IssueNo = IssueNo
        self.DOI = DOI
        self.TypeOfPub = TypeOfPub

        

    #Getting attributes
    def getAuthor(self):
        return self.author

    def getPub_year(self):
        return self.Pub_Year

    def getTitle(self):
        return self.title

    def getVolume(self):
        return self.vol

    def getAuthorCount(self):
        return self.NoOfAuthors(self.author)

    def getPublisher(self):
        return self.Publisher

    def getIssueNo(self):
        return self.IssueNo

    def getDOI(self):
        return self.DOI

    def getTypeOfPub(self):
        return self.TypeOfPub

    def NoOfAuthors(self, Strcount):
        return len(Strcount.split(","))


    def Display(self):
        print("Authors: ", self.author)
        print("Year : ", self.Pub_Year)
        print("Title : ", self.title)
        print("Volume : ", self.vol)
        print("Number of Authors : ", self.getAuthorCount())
        print("Publisher : ", self.Publisher)
        print("Issue Number: ", self.IssueNo)
        print("DOI : ", self.DOI)
        print("Type of Publication : ", self.TypeOfPub)

    def data(self):
        data = {
	        "Authors": self.author,
	        "Year": self.Pub_Year,
	        "Title": self.title,
	        "Volume": self.vol,
	        "Number of Authors": self.getAuthorCount(),
	        "Publisher": self.Publisher,
	        "Issue Number": self.IssueNo,
	        "DOI": self.DOI,
	        "Type of Publication": self.TypeOfPub
        }

        return data

    



connection  = pymongo.MongoClient("localhost", 27017)

database = connection['mydb']

collection = database['PublicationsTable']


def GoogleScholar(name):
    #Scraping the first page of the  search results of google scholar 
    source = requests.get('http://scholar.google.se/scholar?hl=en&q={}'.format(name)).text
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    
    content = BeautifulSoup(source, 'lxml')
    link =  content.find('h4', class_ = "gs_rt2")
    #print(link.a.get('href'))
    #print(link.a.b.text)
    source2 = requests.get('https://scholar.google.se/{}'.format(link.a.get('href'))).text

    #Author home page
    content2 = BeautifulSoup(source2, 'lxml')
    publications = content2.find_all('tr', class_="gsc_a_tr")


    
    Pub = Publication()

    for item in publications:
        title = item.a.text
        #print("Title: ", title, '\n')
        
        metadata = item.a.get('data-href')
        source3 = requests.get('https://scholar.google.se/{}'.format(metadata)).text
        content3 = BeautifulSoup(source3, 'lxml')

        data = content3.find_all('div', class_='gsc_vcd_value')

        data2 = content3.find_all('div', class_='gsc_vcd_field')

        Pub.title = title

        count =  0
        for i in data:
            #print(data2[count].text,": ",i.text)

            if(data2[count].text == "Authors"):
                Pub.author = i.text
             #   print("Got Author: ", i.text)
               

            if(data2[count].text == "Publication date"):
               # print("Got the date: ", i.text)
               Pub.Pub_Year =  i.text

            if(data2[count].text == "Conference"):
               # print("Its  a conference")
               Pub.TypeOfPub = data2[count].text
            
            if(data2[count].text == "Journal"):
               # print("Its a journal")
               Pub.TypeOfPub = data2[count].text
            
            if(data2[count].text == "Pages"):
               # print("Got number of pages", i.text)
               pass

            if(data2[count].text == "Publisher"):
                #print("Got the Publisher", i.text)
                Pub.Publisher = i.text

            if(data2[count].text == "Volume"):
                #print("Got the Volume", i.text)
                Pub.vol = i.text
                
        

            count = count+1
            
        Pub.Display()

        #data = Pub.data()

        data = {
            "Author" : name,
	        "Authors": Pub.getAuthor(),
	        "Year": Pub.getPub_year(),
	        "Title": Pub.getTitle(),
	        "Volume": Pub.getVolume(),
	        "NumberOfAuthors": Pub.getAuthorCount(),
	        "Publisher": Pub.getPublisher(),
	        "IssueNumber": Pub.getIssueNo(),
	        "DOI": Pub.getDOI(),
	        "TypeOfPublication": Pub.getTypeOfPub()
        }
        

        collection.insert_one(data)

        

        print("=========================================================================================================")



def IEEE_publication(name):
    pass
def ACM_publication(name):
    pass







#Runnin the functions

#Reading the file staff

def fixString(name):
    return name[:-1]



with open('StaffNames.txt', 'r') as file:
    for line in file:
        
        print("\nStarting the staff metadata for",line , " \n")
        GoogleScholar(fixString(line))
        

#GoogleScholar("Olasupo Ajayi")

