from pytube import YouTube
from youtubesearchpython import VideosSearch

import os
import subprocess
import threading
import time

threads = list()

youtubePath = 'https://www.youtube.com/watch?v='

def convert_to_wav(file_name):
    command = ['ffmpeg', '-i', file_name, file_name + '.wav']
    subprocess.run(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
    os.remove(file_name)

def download_video(url, aca, ins, out_path = 'Downloaded', file_name=''):
    yt = YouTube(url)

    if file_name == '':
        file_name = yt.title \
        .replace('/', '') \
        .replace('[', '').replace(']', '') \
        .replace('(', '').replace(')', '') \
        .replace('Video', '') \
        .replace('Music', '') \
        .replace('Official', '') \
        .replace('MV', '') \
        .replace('HD', '') \
        .replace(':', '') \
        .replace('’', "'") \
        .strip()

    if (aca == True):
        acapella_search = VideosSearch(file_name + ' studio acapella', limit = 1)
        acapella_url = youtubePath + acapella_search.result()['result'][0]['id']

        print("Downloading Acapella ->", acapella_url)
        acapella_name = file_name + ' - Acapella'
        acapella_path = out_path + '/Acapella'
        thread = threading.Thread(target=download_video, args=(acapella_url, False, False, acapella_path, acapella_name))
        threads.append(thread)
        thread.start()

    if (ins == True):
        instrumental_search = VideosSearch(file_name + ' official instrumental', limit = 1)
        instrumental_url = youtubePath + instrumental_search.result()['result'][0]['id']

        print("Downloading Instrumental ->", instrumental_url)
        instrumental_name = file_name + ' - Instrumental'
        instrumental_path = out_path + '/Instrumental' 
        thread = threading.Thread(target=download_video, args=(instrumental_url, False, False, instrumental_path, instrumental_name))
        threads.append(thread)
        thread.start()

    out_name = out_path + '/' + file_name
    yt.streams.filter(only_audio=True).order_by('abr').desc()[0].download(output_path=out_path, filename=file_name)
    convert_to_wav(out_name)
    
    print("Done ->", url) 

def download_playlist(playlist, aca = False, ins = False):
    for url in playlist.video_urls:
        print("Downloading ->", url)
        thread = threading.Thread(target=download_video, args=(url, aca, ins,))
        threads.append(thread)
        thread.start()

    for index, thread in enumerate(threads): # close threads
        thread.join()

    time.sleep(2)

