from pytube import Playlist

import os
import threading
import math

from bpm_detector import get_bpm
from key_finder import get_key
from playlist_downloader import download_playlist

downloaded_path = os.curdir + '/Downloaded'

playlistLink = 'https://www.youtube.com/playlist?list=PLHsUZjFcs-UoYd0jSbUbkrRAhQOZe8m11'
playlist = Playlist(playlistLink)

def prep_wav(file):
    file_path = os.path.join(downloaded_path, file)
    file_no_ext = file.split('.wav')[0]

    if 'BPM' not in file_no_ext: 
        bpm = math.floor(get_bpm(file_path))
        key = get_key(file_path)
        
        new_name = "{key} - {bpm} BPM - {file}".format(key = key, bpm = bpm, file = file_no_ext)
        os.rename(file_path, os.path.join(downloaded_path, new_name + '.wav'))
        print(new_name)
    else:
        print(file_no_ext)

def prep_wavs():
    threads = list()
    files = os.listdir(downloaded_path)
    
    print("\nSongs: ")
    #for video in playlist.videos:
    #    print(video.title)

    for file in files:
        if file.endswith('.wav'):
            thread = threading.Thread(target=prep_wav, args=(file,))
            threads.append(thread)
            thread.start()

    for index, thread in enumerate(threads): # close threads
        thread.join()

if __name__ == '__main__':
    download_playlist(playlist, True, True)
    prep_wavs()
