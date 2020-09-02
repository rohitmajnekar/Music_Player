import pandas as pd
import os
import csv
from tinytag import TinyTag
import LyricsHandler
import random


def addToCSV(songName):
    song =  LyricsHandler.currentSongLoc          # creating CSV for recommendation module
    print(song)
    songData = TinyTag.get(song)
    artist = songData.artist
    album = songData.album
    year = songData.year
    title = songData.title
    
    row = [songName,title,album,artist,year]
    try:
        with open('played_song.csv', 'a+',newline='')  as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)
    except:
        print('Csv Writting error')
        
def populate_recommendation():
    
    df_0 = pd.read_csv('played_song.csv', encoding='latin-1')

    df_7 = pd.read_csv('played_song.csv', encoding='latin-1')


    # removing null values to avoid errors #df_1 = df_1.dropna(inplace = True) #df_1 = df_1.artist_name.drop_duplicates()
    df_1 = df_0['artist_name'].value_counts()   #artist
    #print(type (df_1))
    df_1 = df_1.head(5)
    #print(df_1)
    df_1_1 = df_1.to_frame()
    df_1_1.to_csv('top_listened_artist.csv')
    #print("Done")
    df_top_artist = pd.read_csv('top_listened_artist.csv')
    df_top_artist.columns = ["top_artist", "artist_count"]


    df_3 = df_0['release'].value_counts()      #albhum
    df_3 = df_3.head(5)
    #print(df_3)
    df_3_1 = df_3.to_frame()
    df_3_1.to_csv('top_listened_albhum.csv')
    #print("Done")
    df_top_albhum =  pd.read_csv('top_listened_albhum.csv')
    df_top_albhum.columns = ["top_albhum", "albhum_count"]
    #print(type(df_top_years))
    #print(df_top_albhum)

    df_4 = df_0['year'].value_counts()         #year
    df_4 = df_4.head(5)
    #print(df_4)
    df_4_1 = df_4.to_frame()
    df_4_1.to_csv('top_listened_year.csv')
    #print("Done")
    df_top_years = pd.read_csv('top_listened_year.csv')
    df_top_years.columns = ["top_song_year", "year_count"]



    df_year_listen_final = 0 #years top 5
    x = 0
    temp = df_top_years['top_song_year']
    for i in temp:
        temp1 = df_7.loc[df_7['year'] == i]
        #print(temp1)
        x += 1
        if x == 1:
            temp2 = temp1
        if x > 1:
            new = pd.concat([temp2, temp1])
            temp2 = new
    df_year_listen_final = new

    new = 0
    temp = 0
    temp1 = 0
    temp2 = 0
    x = 0



    df_artist_listen_final = 0    #top 5 artist
    str1 = 'a'
    x = 0
    temp = df_top_artist['top_artist']
    i = 0
    for i in temp:
        str1 = i
        #print(str1)
        temp1 = df_year_listen_final.loc[df_year_listen_final['artist_name'] == str1]
        #print(temp1)
        x += 1
        if x == 1:
            temp2 = temp1
        if x > 1:
            new = pd.concat([temp2, temp1])
            temp2 = new

    df_artist_listen_final = new
    new = 0
    temp = 0
    temp1 = 0
    temp2 = 0
    x = 0


    df_albhum_listen_final = 0    #top 5 albhum
    str1 = 'a'
    x = 0
    temp = df_top_albhum['top_albhum']
    for i in temp:
        str1 = i
        temp1 = df_artist_listen_final.loc[df_artist_listen_final['release'] == str1]
        x += 1
        if x == 1:
            temp2 = temp1
        if x > 1:
            new = pd.concat([temp2, temp1])
            temp2 = new

    df_albhum_listen_final  = new
    df_albhum_listen_final = df_albhum_listen_final.drop_duplicates(subset='name', keep='first')
    list1 =[]

    for i in df_albhum_listen_final['name']:
        list1.append(i)

    random.shuffle(list1)
    return list1
