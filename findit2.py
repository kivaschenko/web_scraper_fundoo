#!usr/bin/env python3

import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup

filename = 'findit1.csv'
names = ['company', 'sub_industry', 'type_company','location', 'url_details']
df = pd.read_csv(filename, header=None, names=names, encoding='utf-8')
df = df.dropna()
print(df.head())
df['url_details'][0] = 'https://www.fundoodata.com/companies-detail/Hexagon-Infosoft-Solutions-Pvt-Ltd/115328.html?&pageno=1'
url_list = df['url_details'][:]

def write_csv(data):
    with open('findit2.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['details']))

def get_details(url):
    responce = requests.get(url)
    html = responce.text
    html_soup = BeautifulSoup(html, 'lxml')
    # try:
    #     company = html_soup.find('div', class_='search-page-right-pannel').text.split('\n')[2]
    # except:
    #     company = ''
    try:
        details = html_soup.find('div', class_='search-page-right-pannel').text.split('\n')[1:7]
    except:
        details = ''
    data = {'details': details}  
    write_csv(data)

def main():
    for url in url_list:
        get_details(url)

if __name__ == '__main__':
    main()