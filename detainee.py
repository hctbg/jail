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


requests_cache.install_cache(
	'cache',
	expire_after=timedelta(hours=24),
	allowable_methods=('GET')
)

url = 'https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.R00040s?run=2&R001=&R002=&ID=3641&hover_redir=&width=950'

r = requests.get(url, headers={'user-agent': "I'm good people!!!"})

soup = BeautifulSoup(r.content, "lxml")


divs = soup.find_all('div', class_='mugshotDiv')
	


#all IDs (keys)

def get_detainee_ids(div):

	detainee_ID = div.attrs['id'].lstrip('mugshot')

	return detainee_ID


#for all names
def get_detainee_names(div):
	name = div.find('div', class_="inmateName").text.strip()
	return name


#ecreate detainee info table

def create_info_table(div):
	detainee_ID = div.get('id').lstrip('mugshot')
	detainee_name = div.find('div', class_="inmateName").text.strip()

	info_table = div.find('table', class_="collapse centered_table shadow")
	
	trs = info_table.find_all('tr')
	
	#data is a dictionary
	data = {'height': "N/A", 'weight': "N/A", 'sex': "N/A",
			'eyes': "N/A", 'hair': "N/A", 'race': "N/A", 
			'age': "N/A", 'city': "N/A", 'state': "N/A", }

	for tr in trs:
		tds = tr.find_all('td')
		key = tds[0].text.lower().strip()
		value = tds[1].text.strip()
		data[key] = value
	

	detainee_info.create(
		detainee_id = detainee_ID,
		name = detainee_name,
		height = data['height'],
		weight = data['weight'],
		sex = data['sex'],
		eyes = data['eyes'],
		hair = data['hair'],
		race = data['race'],
		age = data['age'],
		city = data['city'],
		state = data['state'],
	)
 

#case number 
def get_case_nums(div):

	case_nums = div.find_all('td', attrs={"data-th": "Case #"})

	return case_nums
    

#extract charge table

def create_charge_table(div,soup):

	detainee_ID = div.get('id').lstrip('mugshot')
	data = {}

	charges = soup.find_all('table', class_="collapse centered_table shadow responsive")
	for trs in charges:
		tds = trs.find_all('td')
		for td in tds:
			key = td.attrs['data-th'].lower().strip()
			value = td.text.strip()
			data[key] = value

	charge.create(
		detainee_id= detainee_ID,
		case_num= data['case #'],
		description= data['charge description'],
		status= data['charge status'],
		bail_amount= data['bail amount'],
		bond_type= data['bond type'],
		court_date= data['court date'],
		court_time= data['court time'],
		jurisdiction= data ['court of jurisdiction']
		)



def main():
	print('executing scraper')
	divs = soup.find_all('div', class_='mugshotDiv')

	for div in divs:
		detainee_ID = get_detainee_ids(div)
		name = get_detainee_names(div)
		case_nums = get_case_nums(div)

		print('checking %s information' % name)

		try:
			detainee_info.get(detainee_id=detainee_ID)
		except DoesNotExist:
			create_info_table(div)
			print('adding %s info' % name)
			print('done')
		else:
			print('%s already exists' % name)

		print("checking %s charge_information" %name)
		for element in case_nums:
			case_num = element.text.lower().strip()
			try:
				create_charge_table(div, soup)
				print('adding Case# %s' % case_num)
			except DoesNotExist:
				print('%s already exists' % case_num)
		print("finished with detainee %s" % name)
		sleep(1.5)

	print('HAHA!!Finally Ready To Go!!')

if __name__=='__main__':
	main()
