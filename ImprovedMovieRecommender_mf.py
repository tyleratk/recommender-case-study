#!/usr/bin/env python

"""
http://surprise.readthedocs.io/en/stable/building_custom_algo.html
"""
import time
import sys
import numpy as np
from surprise import AlgoBase, Dataset, evaluate, SVD, SVDpp

class GlobalMean(AlgoBase):
    def train(self, trainset):

        # Here again: call base method before doing anything.
        AlgoBase.train(self, trainset)

        # Compute the average rating
        self.the_mean = np.mean([r for (_, _, r) in self.trainset.all_ratings()])

    def estimate(self, u, i):

        return self.the_mean


class MeanofMeans(AlgoBase):
    def train(self, trainset):

        # Here again: call base method before doing anything.
        AlgoBase.train(self, trainset)

        users = np.array([u for (u, _, _) in self.trainset.all_ratings()])
        items = np.array([i for (_, i, _) in self.trainset.all_ratings()])
        ratings = np.array([r for (_, _, r) in self.trainset.all_ratings()])

        user_means,item_means = {},{}
        for user in np.unique(users):
            user_means[user] = ratings[users==user].mean()
        for item in np.unique(items):
            item_means[item] = ratings[items==item].mean()

        self.global_mean = ratings.mean()
        self.user_means = user_means
        self.item_means = item_means

    def estimate(self, u, i):
        """
        return the mean of means estimate
        """

        if u not in self.user_means:
            return(np.mean([self.global_mean,
                            self.item_means[i]]))

        if i not in self.item_means:
            return(np.mean([self.global_mean,
                            self.user_means[u]]))

        return(np.mean([self.global_mean,
                        self.user_means[u],
                        self.item_means[i]]))


if __name__ == "__main__":

    data = Dataset.load_builtin('ml-1m')
    # print("\nGlobal Mean...")
    # algo = GlobalMean()
    # evaluate(algo, data)

    print("\nMeanOfMeans... 100k = 1.0171")
    start = time.time()
    algo = MeanofMeans()
    evaluate(algo, data)
    print('\n Time: {} s'.format(time.time()-start))

    print("\nSVD...0.9358")
    # n_factors=200 #no real improvements
    # n_epochs=100 #Worse
    # biased = False #slightly worse
    # init_mean = 1, 2.5 and 5 all worse
    #
    start = time.time()
    algo = SVD()
    evaluate(algo, data)
    print('\n Time: {} s'.format(time.time()-start))
