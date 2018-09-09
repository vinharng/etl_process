import scrape_functions as sf
import params as params
import pandas as pd
from tqdm import tqdm


if __name__=='__main__':

	#create a list to store all the dictionaries, later turning into a dataframe
	output = []
	for event in params.event_url:
		#get all the urls for a given even
		loturls = sf.get_loturls_from_event(event)
		for lot in tqdm(loturls):
			#retrieve data for each lot and transform into a dictionary	
			lot_dictionary = sf.lot_dictionary_from_url(lot)
			output_dictionary = { 'event': event }
			output_dictionary = { **output_dictionary,**lot_dictionary}
			output.append(output_dictionary)
	
	df = pd.DataFrame(output)
	df.to_csv(params.dataset_path)


