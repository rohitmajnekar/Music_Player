import pandas as pd
from tkinter import END
from tkinter import ACTIVE
import json
import tkinter as tk
from tkinter import *
# from main.py import listbox_playlist as listbox5

isPlaylistOped = False
currentPlaylist = ''
def click(listbox,listbox2):
    # print(listbox.index(ACTIVE))
    # print(listbox.get(1, last = None))
    list2 = listbox.curselection()
    list1 = []
    for i in list2:
        list1.append(listbox.get(i))
    try:
        with open('playlist.json', 'r') as jfile:
            playlists = json.load(jfile)
            no_of_playlist = len(playlists.keys())
            # print(no_of_playlist)
            newdic = {'Playlist     '+str(no_of_playlist+1):list1}
            playlists.update(newdic)
        with open ('playlist.json', 'w') as jfile:
            json.dump(playlists,jfile,indent=4)
            # json.dump(playlists, jfile)
            # print('correct')
    except:
        dic = {'playlist1': list1}
        with open('playlist.json', 'w') as jfile:
            json.dump(dic, jfile,indent=4)
        print('error')
    update_list(listbox2)

        
def delete(listbox):
    if len(listbox.curselection())> 0:
        global isPlaylistOped
        if isPlaylistOped == False:
            try:
                with open('playlist.json', 'r') as jfile:
                    playlists = json.load(jfile)
                with open ('playlist.json', 'w') as jfile:
                    playlists.pop(listbox.get(ACTIVE))
                    json.dump(playlists,jfile,indent=4)
            except:
                print("del error")
            update_list(listbox)
        else:
            try:
                with open('playlist.json', 'r') as jfile:
                    playlists = json.load(jfile)
                    
                with open ('playlist.json', 'w') as jfile:
                    song = listbox.get(ACTIVE)
                    playlists[currentPlaylist].remove(song)
                    json.dump(playlists,jfile,indent=4)
            except:
                print("del error")   
            listbox.delete(0, END)
            with open('playlist.json', 'r') as jfile:
                plist_songs = json.load(jfile)
                song_playlist = plist_songs[currentPlaylist]
                for i in song_playlist:
                    listbox.insert(END, i)
                listbox.insert(END, "<----- Go Back")
    
def rename(listbox):
    currentPlaylist = listbox.get(ACTIVE)
    def getText():
        text = l.get()
        # try:
        with open('playlist.json', 'r') as jfile:
            playlists = json.load(jfile)
        with open ('playlist.json', 'w') as jfile:
            playlists[text] = playlists.pop(currentPlaylist)
            json.dump(playlists,jfile,indent=4)
        # except:
            # print('rename error')
        win.destroy()
        update_list(listbox)
        
    win = tk.Toplevel()
    win.geometry("250x50+300+300")
    win.wm_title("Window")
    l = tk.Entry(win, text="Input")
    l.pack()
    b = tk.Button(win, text="Okay", command=getText)
    b.pack()
    
    
    
        
def update_list(listbox):
    listbox.delete(0, END)
    try:
        with open('playlist.json', 'r')as jfile:
            plist = json.load(jfile)
            for i in plist.keys():
                listbox.insert(END, i)
    except:
        print("uppdate error")
    

