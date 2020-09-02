import pandas as pd
import openpyxl as xl
from tinytag import TinyTag

def sortArtist(currentSongLoc):
    wb = xl.load_workbook('test.xlsx')
    sheet = wb.active
    data = sheet.values
    columns = next(data)[0:]
    song_df_1 = pd.DataFrame(data, columns=columns)
    currentArtist = TinyTag.get(currentSongLoc)

    song_categorized = song_df_1.loc[song_df_1['Artist'] == currentArtist.artist]
    print(song_categorized['Artist'])
    # return song_categorized
    
