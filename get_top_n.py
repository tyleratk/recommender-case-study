import pickle
import pandas as pd


# load top_n dict
dct_file = open('top_n.pkl', 'rb')
top_n = pickle.load(dct_file)

# load movie dataframe
movies = pd.read_csv('movies.csv', index_col='id')

# get recommendation for user 601
rec = top_n['601'][0][0]
print('Top recommendation for user 601:')
print(movies.query(rec)[0])



dct_file.close()
