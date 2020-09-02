from tkinter import *
from tkinter import filedialog
from os import listdir
import os
import glob
import tkinter.messagebox
from PIL import Image, ImageTk
from pygame import mixer
import openpyxl as xl
from tinytag import TinyTag
import pandas as pd
import csv
import ast
import populatesRecommendation as popRec
import PlaylistHandler
import json
import LyricsHandler as lyrical
import TopSongHandler

root = Tk()
root.title('PyMusic')
root.configure(bg = '#413C3C')
mixer.init()
isPlaying = False

menubar = Menu(root)
root.config(menu = menubar)


leftFrame = Frame(root, bd = 0,bg = '#413C3C',borderwidth = 0)
leftFrame.grid(row=1, column=0)
playlistFrame = Frame(root, bd = 0,bg = '#413C3C',borderwidth = 0)
playlistFrame.grid(row=1, column=1,sticky=N)
rightFrame = Frame(root, bd = 0, bg = '#413C3C')
rightFrame.grid(row=2, column=0, sticky = W)
headFrame  = Frame(rightFrame, bg = '#413C3C')
buttonFrame = Frame(rightFrame, bg = '#413C3C')
bottomFrame = Frame(leftFrame, bg = '#413C3C')
dunk = Frame(root)
dunk.grid(row=3, column=0,sticky=NSEW)
recommendedFrame = Frame(bottomFrame, bg = '#413C3C')

statusbar = Label(dunk, text = "Welcome")
statusbar.pack()
headtext = Label(bottomFrame, text = "Let's Rock!")
headtext.pack(fill= X)
recomendText = Label(recommendedFrame, text = "Recommended Music", bg = '#413C3C', fg = 'white')
getLyrics = Button(recommendedFrame, text = "Get Lyrics",command = lyrical.show_lyrics, bg = '#F5F2D0',borderwidth = 0, fg = 'black')

scrollbar = Scrollbar(bottomFrame, bg = '#413C3C')
scrollbar.pack(side=RIGHT, fill=Y)
listbox = Listbox(bottomFrame,height = 20, width = 80,  yscrollcommand=scrollbar.set, selectmode=EXTENDED, bg = '#413C3C', fg = 'white' )
listbox_playlist = Listbox(playlistFrame,height = 20, width = 40,  yscrollcommand=scrollbar.set, selectmode=SINGLE, bg = '#413C3C', fg = 'white' )
listbox1 = Listbox(bottomFrame,height = 5, width = 80, yscrollcommand=scrollbar.set, selectmode=SINGLE, bg = '#413C3C', fg = 'white' )
scrollbar.config(command=listbox.yview)
# Functions
def onMouseWheel(event):
    scrollbar.config(command = listbox1.yview)
    
def open_playlist(event):
    global RenamePlaylistBtn
    # global PlaylistHandler.isPlaylistOped
    PlaylistHandler.currentPlaylist = listbox_playlist.get(ACTIVE)
    if PlaylistHandler.currentPlaylist == "<----- Go Back":                    # Throws back to playlist
        RenamePlaylistBtn.config(state='normal')
        PlaylistHandler.isPlaylistOped = False
        PlaylistHandler.update_list(listbox_playlist)
        return
    if PlaylistHandler.isPlaylistOped == True:         # Play Song if playlist is opend else open playlist
        p.play_music()
        return
    RenamePlaylistBtn.config(state='disable')           #Doesn't allow rename of Songs
    listbox_playlist.delete(0, END)
    PlaylistHandler.isPlaylistOped = True
    with open('playlist.json', 'r') as jfile:           # Feeds songs in listbox of playlist
        plist_songs = json.load(jfile)
        song_playlist = plist_songs[PlaylistHandler.currentPlaylist]
        for i in song_playlist:
            listbox_playlist.insert(END, i)
        listbox_playlist.insert(END, "<----- Go Back")
        
class workbook:
    def __init__(self,p):
        self.p = p
        try:
            self.add_artist()  
        except:
            print('Workbook error')
        
    def add_artist(self):
        if os.path.isfile(self.p.loc):
            print('it exitst')
            return
        point = 2
        wb = xl.Workbook()
        sheet = wb.active
        sheet.title = 'sheet 1'
        sheet['A1'] = 'Artist'
        sheet['B1'] = 'Album'
        sheet['C1'] = 'Genre'
        sheet['D1'] = 'Title'
        sheet['E1'] = 'Count'
        for i in self.p.fileList:
            try:
                x = str(point)
                song = TinyTag.get(i)
                artist = song.artist
                album = song.album
                genre = song.genre
                title = song.title
                sheet['A'+ x] = artist
                sheet['B'+ x] = album
                sheet['C'+ x] = genre
                sheet['D'+ x] = title
            except:
                print('error')
            point += 1
        wb.save('C:/Users/Mr. Roo/Documents/MCA Stuff/Projects/Music Player/test.xlsx')
            

class Play:
    
    def __init__(self, listbox, listbox2,listbox3):
        self.loc = "C:/Users/Mr. Roo/Documents/MCA Stuff/Projects/Music Player/test.xlsx"
        self.currentSongIndex = 0
        self.listbox = listbox
        self.listbox3 = listbox3
        self.paused = FALSE
        self.xx = 1
        self.prevSong = ""
        self.mydic = {}
        self.open_list()
        self.open_csv()
        self.listbox2 = listbox2
        self.alreadyPlayed = []
        self.currentPlaylist = 0
        
    def Recommend(self, currentPlaylist, playedTimes = 1000):
        max = 0
        keys = ""
        if len(self.alreadyPlayed) > 5:
            self.alreadyPlayed = []
        try:
            for key, val in self.mydic[currentPlaylist].items():
                for i in self.alreadyPlayed:                #if song is already played it won't recommend again
                    if i == key:
                        continue
                    keys = key
                    max = val
                    if val >= max and val < playedTimes:
                            max = val
                            keys = key
            self.listbox2.delete(0, END)
            if (keys != ""):
                self.listbox2.insert(END,keys)
                
            topSong = TopSongHandler.populate_recommendation()
            for key in topSong:
                self.listbox2.insert(END,key)
        except:
           print('Recommend error')
        
    def open_csv(self):
        if os.path.exists('data.csv'):
            with open('data.csv', 'r+') as csvfile:
                    reader = csv.reader(csvfile)
                    for key, value in reader:
                            self.mydic[key] = ast.literal_eval(value)
                    print(self.mydic)
        if os.path.exists('played_song.csv'):
            print('')
        else:
            label = ['name','title','release','artist_name','year']
            with open('played_song.csv', 'w',newline='')  as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(label)
            
        
    def open_folder(self):
        folderName = filedialog.askdirectory()
        try:
            folderList = open('folders.txt', 'r')
            
            for loc in folderList:                      #checks for dublicate
                if folderName == loc.strip():
                    print('Dublicate')
                    folderList.close()
                    return
        except:
            print('error2')
            
        folderList = open('folders.txt', 'a')
        folderList.write(folderName + '\n')
        folderList.close()
        
        exist = False
        if exist == True:
            fileList = glob.glob(folderName + '/*.mp3').sort()
            self.fileList.extend(fileList)
        else:
            fileList = glob.glob(folderName + '/*.mp3').sort()
            self.fileList = fileList
            exist = True
        for i in range(len(fileList)):
            self.listbox.insert(END, os.path.basename(fileList[i]))
            
    def open_list(self):
        try:
            folderList = open('folders.txt', 'r')
            exist = False
            for loc in folderList:
                fileList = glob.glob(loc.strip() + '/*.mp3')
                if exist == True:
                    self.fileList.extend(fileList)
                else:
                    self.fileList = fileList
                exist = True
                for i in range(len(fileList)):
                    self.listbox.insert(END, os.path.basename(fileList[i]))
        except:
            print('error')
            
    def getActiveIndex(self):
        if len(self.listbox2.curselection())>0:
            songName = self.listbox2.get(ACTIVE)
        else:
            songName = self.listbox3.get(ACTIVE)
        return self.listbox.get(0,'end').index(songName)
        
    def play_music(self):
        if self.paused == FALSE:
            try:  
                if  len(self.listbox2.curselection())>0:
                    self.currentSongIndex = int(self.getActiveIndex())   
                elif len(self.listbox3.curselection())>0:
                    self.currentSongIndex = int(self.getActiveIndex())
                else:            
                    self.currentSongIndex = int (self.listbox.index(ACTIVE))
                lyrical.currentSongLoc = self.fileList[self.currentSongIndex]
                mixer.music.load(self.fileList[self.currentSongIndex])
                mixer.music.play()
                playButton.grid_forget()
                pauseButton.grid(row = 0, column = 2, padx = 20)
                statusbar['text'] = 'Now Playing ' + os.path.basename(self.fileList[self.currentSongIndex])
                currentSong = os.path.basename(self.fileList[self.currentSongIndex])
                TopSongHandler.addToCSV(currentSong)
                global root
                if self.prevSong == "":
                    self.prevSong = currentSong
                    self.Recommend(currentSong)
                else:
                    self.ordered_list(self.prevSong, currentSong)
                    self.prevSong = currentSong
                self.alreadyPlayed.append(currentSong)
            except:
                print("Playerror")
        else:
            mixer.music.unpause()
            playButton.grid_forget()
            pauseButton.grid(row = 0, column = 2, padx = 20)
            statusbar['text'] = 'Now Playing ' + os.path.basename(self.fileList[self.currentSongIndex])
        
    def play_music1(self,event):
        if self.paused == FALSE:
            try: 
                if  len(self.listbox2.curselection())>0:
                    self.currentSongIndex = int(self.getActiveIndex())   
                elif len(self.listbox3.curselection())>0:
                    self.currentSongIndex = int(self.getActiveIndex())
                else:            
                    self.currentSongIndex = int (self.listbox.index(ACTIVE))
                # self.currentSongLoc = self.fileList[self.currentSongIndex]
                lyrical.currentSongLoc = self.fileList[self.currentSongIndex]
                mixer.music.load(self.fileList[self.currentSongIndex])
                mixer.music.play()
                playButton.grid_forget()
                pauseButton.grid(row = 0, column = 2, padx = 20)
                statusbar['text'] = 'Now Playing ' + os.path.basename(self.fileList[self.currentSongIndex])
                currentSong = os.path.basename(self.fileList[self.currentSongIndex])
                TopSongHandler.addToCSV(currentSong)
                global root
                if self.prevSong == "":
                    self.prevSong = currentSong
                else:
                    self.ordered_list(self.prevSong, currentSong)
                    self.prevSong = currentSong
                self.alreadyPlayed.append(currentSong)
            except:
                print("Playerror")
        else:
            mixer.music.unpause()
            playButton.grid_forget()
            pauseButton.grid(row = 0, column = 2, padx = 20)
            statusbar['text'] = 'Now Playing ' + os.path.basename(self.fileList[self.currentSongIndex])
    
        
    def ordered_list(self, prevSong,currentPlaylist):
        if prevSong in self.mydic:
            if currentPlaylist in self.mydic[prevSong]:
                self.mydic[prevSong][currentPlaylist] = self.mydic[prevSong][currentPlaylist]+1  #increases count
            else:
                self.mydic[prevSong][currentPlaylist] = 0                                     #add new current songs to existing dict
        else:
            tempdic = {prevSong:{currentPlaylist:0}}                                        #add new prev and current song
            self.mydic.update(tempdic)
            
        self.Recommend(currentPlaylist)
        
        # print(self.mydic)                                                      #Converting DictToCSV
        with open('data.csv', 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
            for key in self.mydic.items():
                writer.writerow(key)
            
            
    def prev_music(self):
        if self.currentSongIndex == 0:
            print("Limit exceed")
        else:
            mixer.music.stop()
            self.currentSongIndex -=1
            mixer.music.load(self.fileList[self.currentSongIndex])
            mixer.music.play()
            playButton.grid_forget()
            pauseButton.grid(row = 0, column = 2, padx = 20)
            statusbar['text'] = 'Now Playing ' + os.path.basename(self.fileList[self.currentSongIndex])
            
    def next_music(self):
        if self.currentSongIndex >=  self.listbox.size()-1:
            print("Limit exceed")
        else:
            mixer.music.stop()
            self.currentSongIndex +=1
            mixer.music.load(self.fileList[self.currentSongIndex])
            mixer.music.play()
            playButton.grid_forget()
            pauseButton.grid(row = 0, column = 2, padx = 20)
            statusbar['text'] = 'Now Playing ' + os.path.basename(self.fileList[self.currentSongIndex])
    def pause_music(self):
        self.paused = True
        mixer.music.pause()
        pauseButton.grid_forget()
        playButton.grid(row = 0, column = 2,padx = 20)
        statusbar['text'] = 'Pause ' + os.path.basename(self.fileList[self.currentSongIndex])
    def stop_music(self):
        mixer.music.stop()
        pauseButton.grid_forget()
        playButton.grid(row = 0, column = 2,padx = 20)
        self.paused = FALSE
        statusbar['text'] = 'Music Stopped'
    def set_volume(self,val):
        volume = int(val)/100
        mixer.music.set_volume(volume)

            

    
    

#end Functions

#code starts here

p = Play(listbox,listbox1,listbox_playlist)
w = workbook(p)


createPlaylistButton = Button(playlistFrame, text = "Create Playlist", command =lambda:PlaylistHandler.click(listbox,listbox_playlist) , bg = '#b19cd9', fg = 'white',borderwidth =0)
deletePlaylistBtn = Button(playlistFrame, text = "Delete",command = lambda:PlaylistHandler.delete(listbox_playlist), bg = "#F67280", fg = 'white', borderwidth = 0, width =16) 
RenamePlaylistBtn = Button(playlistFrame, text = "Rename",command = lambda:PlaylistHandler.rename(listbox_playlist), bg = "#F8B195", fg = 'white', borderwidth = 0, width =16) 

listbox.bind('<Double-1>',p.play_music1 )
listbox_playlist.bind('<Double-1>',open_playlist)
listbox1.bind('<Double-1>',p.play_music1)
listbox1.bind('<MouseWheel>', onMouseWheel)

createPlaylistButton.pack(fill= X)

listbox_playlist.pack()
listbox.pack()

deletePlaylistBtn.pack(side = LEFT)
RenamePlaylistBtn.pack(side = RIGHT)
recommendedFrame.pack(fill = X)
recomendText.pack(side = LEFT,padx = 150)
getLyrics.pack(side = RIGHT)
# recomendText.grid(row = 0,column = 0)
# getLyrics.grid(row = 0,column = 1, sticky = E)

listbox1.pack()

PlaylistHandler.update_list(listbox_playlist)

# wb = xl.load_work book('test.xlsx')
# sheet = wb.active
# data = sheet.values
# columns = next(data)[0:]
# song_df_1 = pd.DataFrame(data, columns=columns)
# #print(song_df_1.head())

# # print(dataframe.loc[dataframe['column_name'] == 'Key_va'])
# song_categorized = song_df_1.loc[song_df_1['Artist'] == 'Eminem']
# print(song_categorized)


# TaskBar
submenu = Menu(menubar,tearoff = 0)
menubar.add_cascade(label = 'File', menu = submenu)
submenu.add_command(label = 'Open Folder', command = p.open_folder)
submenu.add_command(label = 'Open')
submenu.add_command(label = 'Close', command = root.destroy)

#play
play = Image.open('Assets/play.png')
play = play.resize((70,70), Image.ANTIALIAS)
play1 = ImageTk.PhotoImage(play)
playButton = Button(buttonFrame, image = play1,command = p.play_music, bg = '#413C3C', width = 40, height = 50, bd = 0)
playButton.grid(row = 0, column = 2,padx = 20)
#stop
stop = Image.open('Assets/stop.png')
stop = stop.resize((70,70), Image.ANTIALIAS)
stop1 = ImageTk.PhotoImage(stop)
stopButton = Button(buttonFrame, image = stop1,command = p.stop_music, bg = '#413C3C', width = 50, height = 50, bd = 0)
stopButton.grid(row = 0, column = 1,padx = 20)
#pause
pause = Image.open('Assets/pause.png')
pause = pause.resize((70,70), Image.ANTIALIAS)
pause1 = ImageTk.PhotoImage(pause)
pauseButton = Button(buttonFrame, image = pause1,command = p.pause_music, bg = '#413C3C', width = 40, height = 50, bd = 0)
#prev
prev = Image.open('Assets/prev.png')
prev = prev.resize((70,70), Image.ANTIALIAS)
prev1 = ImageTk.PhotoImage(prev)
prevButton = Button(buttonFrame, image = prev1,command = p.prev_music, bg = '#413C3C', width = 40, height = 50, bd = 0)
prevButton.grid(row=0, column = 0)
#next
nex = Image.open('Assets/next.png')
nex = prev.resize((70,70), Image.ANTIALIAS)
nex1 = ImageTk.PhotoImage(nex)
nexButton = Button(buttonFrame, image = nex1,command = p.next_music, bg = '#413C3C', width = 40, height = 50, bd = 0)
nexButton.grid(row=0, column = 4, padx = 10)




scale = Scale(rightFrame, from_ = 0,width =10, to = 100,fg= "#fff", bg = '#413C3C', orient = HORIZONTAL, command = p.set_volume)
scale.set(70)
scale.grid(row = 0, column = 1,padx = 10,ipadx = 50, sticky = E)

# headFrame.grid(row = 0, column = 0)
buttonFrame.grid(row = 0, column = 0, sticky = W)
bottomFrame.grid(row = 1, column = 0)

root.mainloop()


