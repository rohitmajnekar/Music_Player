import tkinter as tk
from PyLyrics import *
from tinytag import TinyTag

currentSongLoc = ''
def show_lyrics():
    try:
        tag = TinyTag.get(currentSongLoc)
        print(tag.artist)
        print(tag.title)
        lyrics = PyLyrics.getLyrics(tag.artist,tag.title)   #store the lyrics if song available
    
        root1 = tk.Toplevel()
        root1.geometry('400x300')
        root1.title('Lyrics')
        canvas = tk.Canvas(root1)
        scrolly = tk.Scrollbar(root1, orient='vertical', command=canvas.yview)
        
        # display labels in the canvas
        
        label = tk.Label(canvas, text=lyrics,wraplength=300)
        canvas.create_window(0, 5, anchor='n', window=label)
        canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scrolly.set)
        canvas.pack(fill='both', expand=True, side='left')
        scrolly.pack(fill='y', side='right')
    except:
        print("Lyrics not found")