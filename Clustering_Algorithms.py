#Author: Elias Rosenberg
#Date: June 2, 2021
#email: elias.k.rosenberg.22@dartmouth.edu
#Purpose: takes in cleaned files from webScraping.py and uses tfidf and KMeans algorithms to cluster them.
#outputs cluster features for 6 song genres, and takes in user input to predict lyric genre from those clusters.
#Input: .txt lyric files | user input for predictions
#output: cluster features | genre prediction from user input


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from parsingData import rockTesting, popTesting, rapTesting
import numpy as np



textBoundary = 'newgenrestartshere'
print("loading docs...")

lyrics = open('allLyricsCleaned', 'r', encoding="utf8").read() #loading in song lyrics
lyrics = lyrics.split(textBoundary)

genreLabels = ['Pop', 'Jazz', 'Heavy Metal', 'Rap', 'Rock', 'Country'] #the six genres for clustering

lyricsList = []
for line in lyrics:
    lyricsList.append(line)

documents = lyricsList #the documents that will be vectorized.

print("forming tf-idf matrix...")
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)

vectors = vectorizer.fit_transform(documents)

print("forming K-Means clusters...")
true_k = 6
model = KMeans(n_clusters= true_k, init="k-means++" , max_iter=100, n_init=1)
model.fit(vectors)

print("model has been formed...")
names = model.labels_ #getting all the labels
print(names)

#print(model.cluster_centers_)
feature_names = vectorizer.get_feature_names()


print("genres and their word clusters") #sorting the clusters
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
#print(terms)


for i in range(true_k):
    print("Cluster: " + str(i)),
    for ind in order_centroids[i, :10]: #printing out the top 10 features per cluster
        print(' %s' % terms[ind]),
    print()
print("\n")

#prediction method to test 100 songs tagged as rap, pop, or rock
def prediction ():

    print("===================================================================")
    print("please input your lyrics as a string to predict what genre they are")

    test1 = open('rockTest.txt', 'r')
    for song in test1:
        Y = vectorizer.transform([song])
        prediction = model.predict(Y)
        print(prediction)

    print("===================================================================")
    print("please input your lyrics as a string to predict what genre they are")
    test2 = open('rapTest.txt', 'r')
    for song in test2:
        Y = vectorizer.transform([song])
        prediction = model.predict(Y)
        print(prediction)

    print("===================================================================")
    print("please input your lyrics as a string to predict what genre they are")
    test3 = open('popTest.txt', 'r')
    for song in test3:
        Y = vectorizer.transform([song])
        prediction = model.predict(Y)
        print(prediction)

if __name__ == '__main__':
        prediction()

