from surprise import Dataset
import pickle
import pandas as pd

def get_top_n():
    # load top_n dict
    dct_file = open('top_n_1m.pkl', 'rb')
    top_n = pickle.load(dct_file)
    return top_n


def get_top_known(df, user, n):
    group_by = df.groupby('userid')
    top_n = group_by.get_group(user)
    top_n = top_n.sort_values('ratings')[::-1][:n]

    movies = top_n.movieid.values
        
    return movies
    
def get_top_pred(user, n):
    top_n = get_top_n()
    preds = top_n[str(user)][:n]
    
    movies = []
    for pred in preds:
        movies.append(pred[0])
        
    return movies




if __name__ == '__main__':
    

    user = 601
    
    # load movie dataframe
    movies = pd.read_csv('movies_1m.dat', sep='::', names=['id', 'name', 'genre'], 
                         index_col='id', engine='python')
    # load ratings dataframe             
    ratings = pd.read_csv('ratings_1m.dat', sep='::', names=['userid', 'movieid', 
                     'ratings', 'time'], index_col='userid', engine='python')
    
    # get known top n movies for user 
    top_5_known = get_top_known(ratings, user=user, n=5)
    # get top n preds for user NO MORE THAN 10
    top_5_pred = get_top_pred(user=user, n=5)
    
    print('Top known movies for user {}:'.format(user))
    for movie in top_5_known:
        print(movies.query(str(movie))[0], 
              '| Genre:', movies.query(str(movie))[1])
              
    print()
    
    print('Top predictions for user {}:'.format(user))
    for movie in top_5_pred:
        print(movies.query(movie)[0], 
              '| Genre:', movies.query(movie)[1])
    
    


