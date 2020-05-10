# #!/usr/bin/env python
# # coding: utf-8

# # In[129]:


#import package 
from bs4 import BeautifulSoup
from datetime import timedelta
from time import sleep
from peewee import DoesNotExist
import requests
import requests_cache

# requests_cache.install_cache(
#     'cache',
#     expire_after=timedelta(hours=24),
#     allowable_methods=('GET', 'POST')
# )

from urllib.parse import parse_qs, urlparse


SEARCH_URL = 'https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.R00040s?run=2&R001=&R002=&ID=3641&hover_redir=&width=950'

def get_detail_list():
    
    r = requests.get(SEARCH_URL)
    
    soup = BeautifulSoup(r.content, 'lxml')

    divisions = soup.find('div', id = 'content')

    each_detainee = divisions.find_all('div')

    details_result = []

    for div in divisions:
        id = div.attrs['id']
        details_result.append(id)

    return details_result



def extract_detainee_name(name):

    soup = BeautifulSoup(name, lxml)
    
    detainee_names = set() #empty list for details

    table = soup.find_all('div', class_='detaineeInfo')

    name_all = table.find_all('div', class_="inmateName")

    for na in name_all:
        detainee_names.add(na)

    return detainee_names
   


def extract_detainee_info():

    soup = BeautifulSoup(info, lxml)

    detainee_info = []

    tables = soup.find('table', class_="collapse centered_table shadow")

    td_all = tables.find_all('td', class_='two td_left')

    url = 'https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.R00040s?run=2&R001=&R002=&ID=3641&hover_redir=&width=950'

query_str = urlparse(url).query

    info = detainee_info.create(
        id = parse_qs(query_str)['ID'][0].strip(),
        height = td_all[0].text.strip(),
        weight = td_all[1].text.strip(),
        sex = td_all[2].text.strip(),
        eyes = td_all[3].text.strip(),
        hair = td_all[4].text.strip(),
        race = td_all[5].text.strip(),
        age = td_all[6].text.strip(),
        city = td_all[7].text.strip(),
        state = td_all[8].text.strip(),
        )

    print(info)
    print(type(info))



def main():
    details_result = get_detail_list()

    detainee_names = extract_detainee_name(name)
    # urls = extract_td(search_results)

    #     for url in urls:
    #         print('extract_td' % url)
    #         details = get detail(url)


    sleep(3)

if __name__ == '__main__':
    main()










# # In[135]:


# with open ('homepage.html','w') as f:
#     f.write(r.text)


# # In[136]:


# soup = BeautifulSoup(r.text)


# # In[137]:


# type(soup)


# # In[138]:


# dir(soup)


# # In[139]:


# table = soup.find('table', class_="collapse data-table shadow responsive")


# # In[140]:


# type(table)


# # In[141]:


# dir(table)


# # In[142]:


# table.find('tr',class_="table-header").find_all('th')


# # In[143]:


# th_all = table.find('tr',class_="table-header").find_all('th')


# # In[144]:


# for th in th_all:
#     print(th.text)


# # In[145]:


# headers = []


# # In[146]:


# for th in th_all:
#     header = th.text.strip().replace(' ', '_').lower()
#     headers.append(header)


# # In[147]:


# headers


# # In[148]:


# tr_all = table.find_all('tr')[2:190]


# # In[149]:


# len(tr_all)


# # In[150]:


# for tr in tr_all:
#     for td in tr.find_all('td'):
#         print(td.text.strip())
#     print('---------------')


# # In[151]:


# def clean_row(tds):
#     row = {
#         'last_name':tds[0].text.strip(),
#         'first_name':tds[1].text.strip(),
#         'middle_name':tds[2].text.strip(),
#         'suffix':tds[3].text.strip(),
#         'sex':tds[4].text.strip(),
#         'race':tds[5].text.strip(),
#         'age':int(tds[6].text.strip()),
#         'city':tds[7].text.strip(),
#         'state':tds[8].text.strip(),
#         'detail_url': tds[9].find('a').attrs['href']
#     }
#     return row
    


# # In[152]:


# rows = []


# # In[153]:


# for tr in tr_all:
#     tds = tr.find_all('td')
#     row = clean_row(tds)
#     rows.append(row)


# # In[156]:


# len(rows) 


# # In[157]:


# import csv


# # In[159]:


# rows[0].keys()


# # In[160]:


# with open('jail.csv', 'w', newline='') as f:
#     writer = csv.DictWriter(
#         f, fieldnames=rows[0].keys()
#     )
    
#     writer.writeheader()
#     for row in rows:
#         writer.writerow(row)








