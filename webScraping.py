#Author: Elias Rosenberg
#Date: Jun 7th, 2021
#email: elias.k.rosenberg.22@dartmouth.edu
#Purpose: Scrape the web for song lyrics using the Genius API. Code based on this lovely module. https://pypi.org/project/lyricsgenius/
#input: lists of genres with top artists/bands
#output: a .txt file with relevant song lyrics for a particular genre I'd like to use in clustering, as well as a master file with all lyrics.

import os
import re
import lyricsgenius
from requests.exceptions import Timeout
from nltk.corpus import stopwords
from nltk.tokenize import *



GENIUS_API_TOKEN = 'hZd85OdlIMR8bjL-MCCs57RwOAiK-GB-a8gAm8v3KwptTtMeLpKQtQnZAkZ88_3T' #unique key to access the Genius API
songNumber = 10 #number of songs searched per artist
sortingTitle = "title" #how the songs are presented

#lists of genres, each with ten prominent artists. Will be read through to make scraping easier.
country = ["Brad Paisley", "Carrie Underwood", "Keith Urban", "Johny Cash", "Garth Brooks", "Dolly Parton", "Willie Nelson", "Blake Shelton", "Luke Combs", "Gabby Barrett"]
heavyMetal = ["Black Sabbath", "Slipknot", "Iron Maiden", "Tool", "Avenged Sevenfold", "Rammstein", "Meshuggah"]
rock = ["Led Zeppelin", "Pink Floyd", "The Rolling Stones", "The Who", "AC/DC", "Aerosmith", "Nirvana", "Guns N' Roses", "Red Hot Chili Peppers"]
rap = ["Jay-Z", "Eminem", "Kanye West", "Kendrick Lamar", "Travis Scott", "Future", "2 Chainz"]
pop = ["Ariana Grande", "Katy Perry", "The Weekend", "Justin Bieber", "Beyoncé", "Maroon 5", "Adele", "One Direction", "Rihanna"]
jazz = ["Frank Sinatra", "Louis Armstrong", "Nat 'King' Cole", "Billie Holiday", "Ray Charles", "Sammy Davis Jr.", "Duke Ellington"]


#searhces for lyrics using the genius object. takes a list of artists and their genre. Outputs a file with all their songs.
def findLyrics(artistList, genre):
    lyrics = "" #string to hold all the lyrics
    text_file = open(genre + "_lyrics", "w")  # txt file with all lyrics tagged by genre
    genius = lyricsgenius.Genius(GENIUS_API_TOKEN) #creating the lyricgenius object
    for artistName in artistList:
        try:
            artist = genius.search_artist(artistName, songNumber, sortingTitle)
            lyrics += artist.to_text()
            # remove identifiers like chorus, verse, etc
            lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics) #removes all structure tags ([Chorus], [Verse1], [Hook], etc)
            lyrics = re.sub(r"\'", '', lyrics)
            lyrics = re.sub(r"\’", '', lyrics) #removing both kinds of apostrophes
            # remove empty lines
            lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
            #print(lyrics)
            n = text_file.write(lyrics)
        except TimeoutError: #timeout errors were frequent. Song is skipped if timeout occurs.
            pass
    text_file.close()


#having issues with timeout from Genius API if song number gets too high. Run each genre one at a time by commenting
#out ones who already have .txt files created to get desired lyric files. You can try to run the program all at
#once, but it depends on how good your internet is.
if __name__ == '__main__':
    #findLyrics(country, "country")
    #findLyrics(heavyMetal, "heavyMetal")
    #findLyrics(rap, "rap")
    #findLyrics(rock, "rock")
    #findLyrics(pop, "pop")
    #findLyrics(jazz, "jazz")


    allText = ['pop_lyrics', 'rock_lyrics', 'heavyMetal_lyrics', 'rap_lyrics', 'country_lyrics', 'jazz_lyrics'] #list of all text files
    #allText = ['pop_lyrics(short)', 'rock_lyrics(short)', 'heavyMetal_lyrics(short)', 'rap_lyrics(short)', 'country_lyrics(short)', 'jazz_lyrics(short)']
    #allText = ['country_lyrics(short)test']
    #allText = ['heavyMetal_lyrics', 'rap_lyrics', 'country_lyrics']

    # combining all lyric genre files into one master file
    with open('allLyrics', 'w') as masterFile:
        # Iterate through doc list
        for docs in allText:
            # Open each file in read mode
            with open(docs) as infile:
                masterFile.write(infile.read())
            masterFile.write("newgenrestartshere")
            masterFile.write("\n")
        masterFile.close()

    #further cleaning of the masterFile

    #print(lyrics_without_sw)
    stop_words = set(stopwords.words('english'))
    extraStopWords = ['i','I','id' 'ive', 'yeah', 'ill', 'dont', 'oh', 'ooh', 'oooh', 'oooh', 'ah', 'aah', 'aaah', 'aaaah', 'la', 'laa', 'laaa', 'laaaa', 'da', 'daa', 'daaa', 'daaaa']

    for word in stop_words:
        for char in word:
            char.replace("'", "")
    for word in extraStopWords:
        stop_words.add(word)


    lyrics_without_sw = ""  # string to hold all the lyrics
    cleaning = open("allLyrics", "r")  # txt file with all lyrics tagged by genre
    for line in cleaning:
        lyrics_without_sw += line

    #print(lyrics_without_sw)
    #print(stop_words)

    print("size with stop words:")
    print(len(lyrics_without_sw))
    print("Tokenizing. This can take a bit...")
    text_tokens = word_tokenize(lyrics_without_sw)
    #print(text_tokens)
    print("filtering out stopwords...")
    tokens_without_sw = ""
    for line in text_tokens:
        if line not in stop_words:
            tokens_without_sw += line
            tokens_without_sw += " "
        #else:
            #print(line)

    tokens_without_sw = tokens_without_sw.lower()
    tokens_without_sw = re.sub(r"[^\w\s]", '', tokens_without_sw) #removing punctuation
    tokens_without_sw = re.sub(r"\d", '', tokens_without_sw) #removing digits
    tokens_without_sw = tokens_without_sw.split(" ")

    further_cleaned_tokens = ""
    for word in tokens_without_sw:
        if word not in stop_words:
            further_cleaned_tokens += word
            further_cleaned_tokens += " "

    #print(further_cleaned_tokens)
    print("size without stop words:")
    print(len(tokens_without_sw))
    cleaning.close()

    final = open("allLyricsCleaned", "w") #the final cleaned text file, containing all lyrics, with genres seperated by a boundary string
    for line in further_cleaned_tokens:
        final.write(line)
    final.close()