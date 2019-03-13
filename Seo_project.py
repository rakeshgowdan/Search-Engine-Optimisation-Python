import pyexcel as pe
import sqlite3
import pandas as pa
import matplotlib.pyplot as plot
from bs4 import BeautifulSoup
import requests
conn = sqlite3.connect("Seo_DataBase123.db")
def read_from_pyexcel():
    print("excel called")
    Source_sheet = pe.get_sheet(sheet_number=0, file_name="C:\\Users\\Raksh\\PycharmProjects\\Data_Analysis\\Reader.xlsx")
    url = Source_sheet.column_at(0).__getitem__(0)
    keywords = Source_sheet.column[1]
    return keywords, url

def read_from_web_page(keywords, url):
    print("web called")
    req = requests.get(url, data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)AppleWebKit/537.36(KHTML,like Gecko)Chrome/35.0.1916.47 Safari/537.36'})
    soup = BeautifulSoup(req.content, 'lxml')
    for content in soup.select("[id^='content-body-'] p"):
        content_in_Text = content.text
    lines = (line.strip()
             for line in content_in_Text.splitlines(True))
    list_after_scrap= []
    current_list = []
    for line in lines:
        list_after_scrap = line.split()
        print(list_after_scrap)
    for word in list_after_scrap:
        if word in keywords:
            current_list.append(word)
    lengthoflist = len(list_after_scrap)
    return (current_list, lengthoflist)

def insert(current_list, lengthoflist):
    print("databse called")
    ctr = 0
    li = []
    D = {}
    density = 0
    setofwords = set(current_list)
    listofwords = list(setofwords)
    for word in listofwords:
        ctr = current_list.count(word)
        D[word] = ctr
        density = (D[word] / lengthoflist) * 100
        li.append(density)
    dictlist = list(D.keys())
    print(dictlist)
    print(li)
    conn.execute("create table Scrap(name text,density int)")
    for x in zip(dictlist, li):
        conn.execute("insert into Scrap(name,density) values(?,?)", x)
    conn.commit()

def graph():
    print("graph called")
    query = "SELECT * FROM Scrap;"
    df = pa.read_sql_query(query, conn)
    df.plot(kind='bar', x='name', y='density')
    plot.show()
    plot.savefig('output.png')
    conn.close()

data_text,link = read_from_pyexcel()
print(data_text,link)
text,count= read_from_web_page(data_text,link)
print(text,count)
insert(text,count)
graph()