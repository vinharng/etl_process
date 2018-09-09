from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium  import webdriver
import params as params

def get_loturls_from_event(event):
	'''
	:params eventurl: (str) url to the auction event
	:return: (list) of urls for each lot  
	'''
	#use selenium to render the JS links 
	driver = webdriver.Chrome(params.chromedriver_path)
	driver.get(params.event_url[event])

	#since the wait time for elememnts to be rendered vary, we need to make sure the ResultContainer can be found by BeautifulSoup to prevent error following this
	load = True
	while load:
		driver.implicitly_wait(30)
		soup_level1 = BeautifulSoup(driver.page_source,'lxml')
		container = soup_level1.find('ul',id='ResultContainer')
		if container is not None:
			load = False
			print('ResultContainer loaded')
	
	all_results = container.findAll('div',{'class':'image-preview-container square center'})
	lot_urls = []

	for res in all_results:
		#use the href tag to retrieve the url to each lot
		lot_url = res.find('a')['href']
		lot_urls.append(lot_url)
	print("Lot URLs for {} retrieved".format(event))
	driver.quit()
	return lot_urls

def parse_artist(artist_born_death):
	'''
	:params artist_born_death: (str) singular text of artist name with born-death
	:return: (dict) organized artist info by name and born-death
	'''
	sub_d = {}
	try:
		sub_d['artist_name'] = artist_born_death.split('(')[0]
		sub_d['born_death'] = artist_born_death.split('(')[1].replace(')','')
	except IndexError:
		sub_d['artist_name'] = 'n/a'
		sub_d['born_death'] = 'n/a'
	return sub_d

def parse_lotdesc(desc):
	'''
	:params desc: (str) raw test description of the lot in lines, including artist, title, signature, medium, size, year of creation
	:return: (dict) organized description of the lot   
	'''
	sub_d = {}
	desc_list = desc.splitlines()
	if desc_list:
		sub_d['signature'] = desc_list[2]
		sub_d['medium'] = desc_list[3]
		year_creation = 'n/a' 
		#parse the size of art from the description
		remain = desc_list[4:]
		size = ''
		#consider 3D art objects, where the size information separated across different lines
		for i, txt in enumerate(remain):
			if 'in.' in txt or 'cm' in txt:
				size+= txt+'|'
			else:
				year_creation = txt
		sub_d['year_creation'] = year_creation
		sub_d['size'] = size
	
	else:
		sub_d = {
		'signature':'n/a'
		,'medium': 'n/a'
		,'year_creation':'n/a'
		,'size':'n/a'
		}
	
	return sub_d

def lot_dictionary_from_url(lot_url):
	'''
	:params eventurl: (str) url to the auction event
	:return: (dict) a dictionary representing each lot with the following keys [lot_number,artist_name,born_death,title,sold_price,estimate,signature,medium,size,year_creation,provenance,image_url]
	'''
	#create a main lot dictionary storing all information about each lot
	lot_dict = {}
	
	driver = webdriver.Chrome(params.chromedriver_path)
	driver.get(lot_url)
	driver.implicitly_wait(15)

	for att in params.attribute_html_id:
		if att == 'image_url':
			#xpath = "//ul[@id='"+attribute_html_id[att]+"'/li[@class='box-link]/a[@class='panzoom--link']'"
			try:
				elem = driver.find_element_by_xpath("//a[@class='panzoom--link']")
				attvalue = elem.get_attribute('href')
			except:
				attvalue = 'n/a'
		else:
			try:
				attvalue = driver.find_element_by_id(params.attribute_html_id[att]).text
				if att == 'description':
					sub_d = parse_lotdesc(attvalue)
					#combine dictionary from art description to main lot dictionary
					lot_dict = {**lot_dict,**sub_d}
				elif att == 'artist_born_death':
					sub_d = parse_artist(attvalue)
					#combine dictionary from artist info to main lot dictionary
					lot_dict = {**lot_dict,**sub_d}
				else:
					lot_dict[att] = attvalue
			except: 
				attvalue = 'n/a'
				print(att+' not found for '+lot_url)
			
	driver.quit()
	return lot_dict



