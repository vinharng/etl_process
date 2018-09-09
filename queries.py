import pandas as pd
import numpy as np
import params as params

def get_repeat_artists(df):
	'''
	param df: (pandas dataframe) of the read data
	return: (list) of artists who sold on two separate events
	'''
	count_ev = df.groupby('artist_name').agg({'event':pd.Series.nunique}).reset_index()
	repeat_artists = count_ev[count_ev['event']==2]['artist_name']

	return repeat_artists.tolist()

def get_similar_objects(df,artist,event,threshold=10):
	'''
	param df: (pandas dataframe) of the read data
	param artist: (str) artist_name
	param event: (str) or either 'nov17' or 'mar18'
	param threshold: (int) threshold of size similarity in cm
	return: (list) of similar objects
	'''
	subdf = df[ (df['artist_name']==artist)&(df['event']==event)][['size','title','sold_price']]
	
	groups = []
	
	index_similar = set()

	#parse sub-dataframe into a list of objects for comparisons
	for index,row in subdf.iterrows():
		title = row['title']
		value = row['sold_price']
		size_text = row['size']

		if pd.isnull(size_text):
			size_text = 'object size not parsed'
		else:
			if len(size_text.split('|'))<=2:
				size_cm_text = size_text[size_text.find("(")+1:size_text.find(")")]
				#compare 2D art(painting and drawings)
				if 'x' in size_cm_text:
					size_cm = size_cm_text.replace('cm.','').strip().split(' x ')
					groups.append([title+' '+value+' ' +size_text,size_cm])

				#compare art with only height
				elif 'Height' in size_text:
					size_cm = [size_cm_text.replace('cm.','').strip()]
					groups.append([title+' '+value+' '+size_text,size_cm])	
				
			else:
				#3D art with more than one line of size information
				#did not get to implement
				pass

	#assuming here that objects can repeat and be in more than one group, since it is impossible to create non-overlapping groups applying a single threshold.
	#For example, object A is 5cm, object B is 15cm, object c is 25cm. with a threshold of 10, A and B are similar, B and C are similar, but A and C are not.
	
	#compare the size of each object against every other object
	for i in range(len(groups)):
		for j in range(len(groups)):
			if i!=j:
				size_i = groups[i][-1]
				size_j = groups[j][-1]
				if len(size_i)==len(size_j):
					for size_position in range(len(size_i)):
						if (float(size_i[size_position])-float(size_j[size_position])) <= threshold:
							index_similar.add((i,j))

	similar_groups = []
	for i in range(len(groups)):
		simgroup = [groups[i][0]]
		
		for sim in index_similar:
			if sim[0]==i:
				simgroup.append(groups[sim[1]][0])
		
		similar_groups.append(simgroup)

	return similar_groups

def get_avg_sold_by_event(df,artist,event):
	'''
	param df: (pandas dataframe) of the read data
	param artist: (str) artist_name
	param event: (str) or either 'nov17' or 'mar18'
	return: (int) average value of objects sold in USD
	'''
	raw_prices = df[ (df['artist_name']==artist)&(df['event']==event)] ['sold_price'].tolist()
	if event == 'mar18':
		#converting GBP to USD using exchange rate on Feb28 2018
		prices = [ (float(p.replace('GBP ','').replace(',',''))*params.gbp_usd_exchange_rate) for p in raw_prices]
		
	else:
		prices = [ float(p.replace('USD ','').replace(',','')) for p in raw_prices]
	
	avg_sold = np.average(prices)

	return avg_sold
