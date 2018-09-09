import params as params
import pandas as pd
import queries as que
import csv

df = pd.read_csv(params.dataset_path)

#get a list of artist who sold in both auctions
repeat_artist = que.get_repeat_artists(df)

with open(params.final_output_path, 'w', newline='') as f:
	writer = csv.writer(f)
	writer.writerow(['Artist','nov17','mar18','value_growth'])
	for artist in repeat_artist:
		#1 get average value from two events
		avg_nov17 = que.get_avg_sold_by_event(df,artist,'nov17')
		avg_mar18 = que.get_avg_sold_by_event(df,artist,'mar18')
		growth = (avg_mar18-avg_nov17)*100/avg_nov17
		writer.writerow([artist, 'Average Value: '+str(avg_nov17),'Average Value:'+str(avg_mar18),growth])

		writer.writerow([artist, 'Similar Objects','Similar Objects',''])
		#2 get groups of similar objects
		nov17_groups = que.get_similar_objects(df,artist,'nov17',threshold=10)
		mar18_groups = que.get_similar_objects(df,artist,'mar18',threshold=10)
		
		for g in range(max(len(nov17_groups),len(mar18_groups))):
			if (g+1)>len(nov17_groups):
				writer.writerow([artist,'',mar18_groups[g],''])
			elif (g+1)>len(mar18_groups):
				writer.writerow([artist,nov17_groups[g],'',''])
			else:
				writer.writerow([artist,nov17_groups[g],mar18_groups[g],''])


		


