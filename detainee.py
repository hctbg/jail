#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
from datetime import timedelta
import requests
import requests_cache
from time import sleep
from models import detainee_info, charge
from peewee import DoesNotExist
from urllib.parse import parse_qs, urlparse




r = requests.get(
    'https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.R00040s?run=2&R001=&R002=&ID=3641&hover_redir=&width=950',
    headers={'user-agent': "I'm good people!!!"})

soup = BeautifulSoup(r.text, features = "lxml")

tables = soup.find('div', id = 'content')


td_all = tables.find_all('td', class_='two td_left') #td means all detail infos and element 

#all division (each detainee with charge and info)

def get_detail_table():

    r = requests.get(
    'https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.R00040s?run=2&R001=&R002=&ID=3641&hover_redir=&width=950',
    headers={'user-agent': "I'm good people!!!"})

    search_results = []

    soup = BeautifulSoup(r.text, features = "lxml")

    body = soup.find('div', id = 'content')
    
    for div in body:

        divs = soup.find_all('div', class_= 'mugshotDiv')

        search_results.append(divs)

    return search_results


#all IDs (keys)

def extract_detainee_ids():

    # r = requests.get(
    # 'https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.R00040s?run=2&R001=&R002=&ID=3641&hover_redir=&width=950',
    # headers={'user-agent': "I'm good people!!!"}
    # )

    # soup = BeautifulSoup(r.text, features = "lxml")

    # tables = soup.find('div', id = 'content')

    url = soup.select("div#content > div",recursive=False)

    detainee_ids = set()

    for tag in url:
        div_ID = tag.get('id')
        detainee_id = div_ID.lstrip('mugshot')
        detainee_ids.add(detainee_id)
    
    return detainee_ids

#define a function that enable me to get the result once I type in the ID

def get_detainee_detail(detainee_id):

    url = 'https://www.mshp.dps.missouri.gov/HP68/AccidentDetailsAction'

    div = soup.find('div', id = detainee_id)

    return div.content

#for all names
def get_detainee_names(detainee_id):

    soup =  BeautifulSoup(r.text, features = "lxml")

    all_names = soup.find_all('div', class_="inmateName")

    for name in all_names:
        name = name.text.strip()
    
    return name

#for all detainee personal info table

def get_info_tables(detainee_id):

    soup = BeautifulSoup(info_table, features = "lxml")

    tables = soup.find('div', id = 'content')

    all_info_tables = tables.find_all('table', class_="collapse centered_table shadow")
    
    return all_info_tables


#extract detainee info table

def extract_detainee_info(detainee_name, info_table):
    # name cells 
    all_names = soup.find_all('div', class_="inmateName")
    # for name in all_names:
    #     name = 

    #info cells 
    all_info_tables = tables.find_all('table', class_="collapse centered_table shadow")

    info_cells = all_info_tables.find_all('td',class_='two td_left')

    #detainee_id cells 
    url = soup.select("div#content > div",recursive=False)
    
    # for tag in url:
    #     div_ID = tag.get('id')
    #     detainee_id = div_ID.lstrip('mugshot')
    i = int(0)

    for ID, name in detainee_id, all_names:
        print(ID)

        detainee_info.create(
            detainee_id  = ID,
            name = names,
            height = info_cells[i].text.strip(),
            
            # weight = info_cells[i++].text.strip(),
        #     sex = info_cells[i++].text.strip(),
        #     eyes = info_cells[i++].text.strip(),
        #     hair = info_cells[i++].text.strip(),
        #     race = info_cells[i++].text.strip(),
        #     age = info_cells[i++].text.strip(),
        #     city = info_cells[i++].text.strip(),
        #     state = info_cells[i++].text.strip(),
        )
        i = i+1
    print(detainee_info)


#extract charge table

def extract_charge_info(detainee_id, table):

    all_charge_info = tables.find_all('table', class_="collapse centered_table shadow responsive")

    for ct in all_charge_info:

        charge_table = ct.find_all('tr')

        charge_cells = charge_table.find_all('td',class_='two td_left')

    charge.create(
        detainee_id = detainee_id,
        case_num = charge_cells[0].text.strip(),
        description = charge_cells[1].text.strip(),
        status = charge_cells[2].text.strip(),
        bail_amount = charge_cells[3].text.strip(),
        bond_type = charge_cells[4].text.strip(),
        court_date = charge_cells[5].text.strip(),
        court_time = charge_cells[6].text.strip(),
        jurisdiction = charge_cells[7].text.strip(),
        )




def main():
        url = soup.select("div#content > div",recursive=False)

        detainee_ids = []

        for tag in url:
            div_ID = tag.get('id')
            detainee_id = div_ID.lstrip('mugshot')
            detainee_ids.append(detainee_id)
            all_names = soup.find_all('div', class_="inmateName")
        # for name in all_names:
        #     name = 

        #info cells 
        all_info_tables = tables.find_all('table', class_="collapse centered_table shadow")

        # info_cells = all_info_tables.find_all('td',class_='two td_left')

        #detainee_id cells 
        url = soup.select("div#content > div",recursive=False)
        
        # for tag in url:
        #     div_ID = tag.get('id')
        #     detainee_id = div_ID.lstrip('mugshot')
        i = int(0)
        print(detainee_ids)
        print('----------------')
        print(all_names)
        for ID in detainee_ids:
            print(ID)

            detainee_info.create(
                detainee_id  = ID
                # name = names,
                # height = info_cells[i].text.strip(),
                
                # weight = info_cells[i++].text.strip(),
            #     sex = info_cells[i++].text.strip(),
            #     eyes = info_cells[i++].text.strip(),
            #     hair = info_cells[i++].text.strip(),
            #     race = info_cells[i++].text.strip(),
            #     age = info_cells[i++].text.strip(),
            #     city = info_cells[i++].text.strip(),
            #     state = info_cells[i++].text.strip(),
            )
            i = i+1
        print(detainee_info)

    # for search_results in get_detail_table():
    #     detainee_ids = extract_detainee_ids(detail_results)
    #     all_info_tables = get_info_tables(detainee_id)


        # for detainee_id in detainee_ids:
        #     print('checking for %s' % detainee_id)

    #         try:
    #             detainee_info.get(detainee_id=detainee_id)


    #         except DoesNotExist:
    #             print('extracting data for %s' % detainee_id)
                
    #             divs = get_detail_table()
    #             extract_detainee_info(all_names.text.strip(),all_info_tables.find_all('td',class_='two td_left'))
    #             extract_charge_info(detainee_id, charge_table.find_all('td',class_='two td_left'))
    #             print('done')
    #             sleep(3)
    #         else:
    #             print('%s already exists' % incident_num)

        # sleep(3)
        # # TODO: don't sleep if prev request came from cache


if __name__ == '__main__':
    main()



#for all charge details

##table data in detail information e.g. 4ft5ich 

# for td in all_detail_info:
#     for td in td.find_all('td',class_='two td_left'):
#         print(td.text.strip())
#     print('---------------')




