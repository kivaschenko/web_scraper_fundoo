#!/usr/bin/env python3
# to contact write: teodorathome@yahoo.com
""" 1. Get list of IT companies 
    2. name, sub industry, company type, location 
	The first part goes previuos round and scrapes urls to pages where are the company details """

import requests 
from bs4 import BeautifulSoup
import csv

def get_html(url):
    responce = requests.get(url)
    html = responce.text
    return html

def write_csv(data):
    with open('fundit1.csv', 'a') as fundit1:
        writer = csv.writer(fundit1)
        writer.writerow((data['company'],
                         data['sub_industry'],
                         data['type_company'],
                         data['location'],
                         data['url_details']))

def get_total_pages(html):
    bsoup = BeautifulSoup(html, 'lxml')
    pages = bsoup.find('div', class_='search-page-heading').text.split(':')[-1].strip()
    pages = int(round(int(pages) / 20))
    return pages

def get_page_data(html):
    bsoup = BeautifulSoup(html, 'lxml')
    items = bsoup.find_all('div', class_='search-result-left')
    for item in items:
        try:
            company = str(item.find('a').get('href')).split('/')[1]
        except:
            company = ''
        try:
            url_details = 'https://www.fundoodata.com/' + item.find('a').get('href')
        except:
            url_details = ''
        try:
            sub_industry = item.find('div', class_="normal-detail").find_all('tr')[1].text.split(':')[1]
        except:
            sub_industry = ''
        try:
            type_company = item.find('div', class_="normal-detail").find_all('tr')[2].text.split(':')[1]
        except:
            type_company = ''
        try:
            location = item.find('div', class_="normal-detail").find_all('tr')[4].text.split(':')[1]
        except:
            location = ''

        data = {'company': company, 'sub_industry': sub_industry, 'type_company': type_company,
                'location': location, 'url_details': url_details1}
        write_csv(data)


def main():
    #      https://www.fundoodata.com/companies-in/pharmaceuticals-labs-i24?&pageno=2&tot_rows=2874&total_results=2874&no_of_offices=0
    url = 'https://www.fundoodata.com/companies-in/information-technology-(it)-i19?'
    base_url = 'https://www.fundoodata.com/companies-in/information-technology-(it)-i19?'
    query_part = '&tot_rows=9686&total_results=9686&no_of_offices=0?'
    page_part = '&pageno='
    pages = get_total_pages(get_html(url))
    for page in range(1, pages):
        print('Parsing %d%%' % (page / pages * 100))
        url = base_url + query_part + page_part + str(page)
        #  https://www.fundoodata.com/companies-in/information-technology-(it)-i19?&tot_rows=9686&total_results=9686&no_of_offices=0&pageno=1
        html = get_html(url)
        get_page_data(html)

if __name__ == '__main__':
    main()