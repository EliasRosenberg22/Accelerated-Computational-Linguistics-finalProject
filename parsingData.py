#Author: Elias Rosenberg
#Date: June 2, 2021
#email: elias.k.rosenberg.22@dartmouth.edu
#Purpose: The purpose of this program is to merge two data sets containing data on lyrics and artists, and genre and
#artists, and merging the two into one data set of lyrics with their genre tags. This allows me to create testing
#data that is tagged by genre.
#input: Lyric and artist csv data sets
#Output: lists of songs with genre tags that can be run through Clustering_Algorithm.py to test accuracy.

import csv

#I found most of this code from looking at other projects linked to the data set I found on kaggle.
#This project is trying to do the same thing as me, but with other sorting algorithms. I give full credit to kaggle user
#"NK" for their parsing of the csv table through pandas, which I have never had to do before, and found very useful. Their
#output file is what needed to be parsed from the original data set.
#https://www.kaggle.com/nkode611/lyricsgenreclassifier-datapreprocessing/comments

Rock = [] #lists to contain all the songs of a certain genre.
Pop = []
HipHop = []


with open('DF_3Genres_Lyrics_En.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    with open ('lyrics', 'w') as new_file:
        csv_writer = csv.writer(new_file)
        genre_dict = {} #placing all the songs in a dictionary with their genre tag as the key.

        for line in csv_reader:
            lyrics = line[0]
            genre = None

            if line[1] == "1":
                genre = "HipHop"
                HipHop.append(lyrics)

            if line[2] == "1":
                genre = "Pop"
                Pop.append(lyrics)

            if line[3] == "1":
                genre = "Rock"
                Rock.append(lyrics)

            genre_dict[lyrics] = genre


       #getting subsets of the certain genres to test with
        rockTesting= Rock[0:100]
        popTesting = Pop[0:100]
        rapTesting = HipHop[0:100]

    #writing the lists into text files to for the prediction method.
    test1 = open("rockTest.txt", "w")
    for song in rockTesting:
        test1.write(song)
        test1.write("\n")
    test1.close()

    test2 = open("rapTest.txt", "w")
    for song in rapTesting:
        test2.write(song)
        test2.write("\n")
    test2.close()

    test3 = open("popTest.txt", "w")
    for song in popTesting:
        test3.write(song)
        test3.write("\n")
    test3.close()

    csv_file.close()



