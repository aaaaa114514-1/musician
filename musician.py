import os
import pathlib
import shutil
import requests
from bs4 import BeautifulSoup
import re
import time
import json
import hashlib
import pygame
import random
import threading
import datetime
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.completion import FuzzyCompleter
from pydub import AudioSegment
from rapidfuzz import process, fuzz

history_data = dict()

class player:
    def __init__(self, playpath, playlist, volume):
        pygame.mixer.init()
        self.playpath = playpath
        self.playlist = playlist
        self.nowplaying = 0
        self.playing_songname = playlist[0]
        pygame.mixer.music.load(os.path.join(self.playpath, self.playing_songname))
        pygame.mixer.music.play()
        pygame.mixer.music.pause()
        self.nowmode = 'stop'
        self.set_volume(volume)
        self.is_single = 0
        self.playtime = 0

    def set_playlist(self, playlist):
        self.playlist = playlist
        if self.playing_songname in self.playlist:
            self.nowplaying = self.playlist.index(self.playing_songname)

    def add_playlist(self, playlist):
        self.playlist.extend(playlist)
        if self.playing_songname in self.playlist:
            self.nowplaying = self.playlist.index(self.playing_songname)

    def set_volume(self, volume: float):
        self.volume = volume
        pygame.mixer.music.set_volume(self.volume)

    def play(self):
        if (self.nowmode != 'playing'):
            self.playtime = int(time.time())
            self.nowmode = 'playing'
        self.playing_songname = self.playlist[self.nowplaying]
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(os.path.join(self.playpath, self.playing_songname))
        pygame.mixer.music.play()
        update_history_song(self.playing_songname)
    
    def next(self):
        self.nowplaying += 1
        if self.nowplaying == len(self.playlist):
            self.nowplaying = 0
        self.play()

    def last(self):
        self.nowplaying -= 1
        if self.nowplaying == -1:
            self.nowplaying = len(self.playlist) - 1
        self.play()

    def check_play(self):
        if self.nowmode == 'playing' and not pygame.mixer.music.get_busy():
            if self.is_single:
                self.play()
            else:
                self.next()

    def pause(self):
        if self.nowmode == 'playing':
            self.nowmode = 'pause'
            pygame.mixer.music.pause()
            update_history_time(int(time.time())-self.playtime)
            self.playtime = int(time.time())

    def unpause(self):
        if self.nowmode == 'stop':
            update_history_song(self.playing_songname)
        if self.nowmode in ['pause', 'stop']:
            self.nowmode = 'playing'
            pygame.mixer.music.unpause()
            self.playtime = int(time.time())
    
    def stop(self):
        if (self.nowmode == 'playing'):
            update_history_time(int(time.time())-self.playtime)
            self.playtime = int(time.time())
        self.nowmode = 'stop'
        pygame.mixer.music.stop()

def keep_checking(player:player, timelimit:list, lock):
    while True:
        time.sleep(0.5)
        player.check_play()
        with lock:
            timelimit0 = timelimit[0]
        # print(time.time(), timelimit0)
        if time.time() > timelimit0:
            bgm.stop()
            timelimit[0] = int(time.time()) + 1e9
            print('Time limit reached!\n>> ',end='')

def fuzzy_match_all(query, string_list, threshold=60):
    matches = process.extract(query, string_list, scorer=fuzz.ratio, score_cutoff=threshold)
    return matches

def signature_generator_1(song_id, s_time,token2):
    str_1 = f"NVPh5oo715z5DIWAeQlhMDsWXXQV4hwtappid=1014clienttime={s_time}clientver=20000dfid=11RUG41l0SmY4ZVgnP0fnD0eencode_album_audio_id={song_id}mid=3bbc1d969ff662635c996e5f73d0a7e1platid=4srcappid=2919token=cc953c223e1dcc686b2dfc1a2465e6de{token2}userid=1501763160uuid=3bbc1d969ff662635c996e5f73d0a7e1NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"
    hashobj = hashlib.md5(str_1.encode("utf-8"))
    return hashobj.hexdigest()

def signature_generator_2(keyword, s_time):
    str_1 = f"NVPh5oo715z5DIWAeQlhMDsWXXQV4hwtappid=1014bitrate=0callback=callback123clienttime={s_time}clientver=1000dfid=1txHuC3KMsDa1MoTkF1HWQUXfilter=10inputtype=0iscorrection=1isfuzzy=0keyword={keyword}mid=5c8dee1cc08f313b60b807d8da2d5fddpage=1pagesize=30platform=WebFilterprivilege_filter=0srcappid=2919token=userid=0uuid=5c8dee1cc08f313b60b807d8da2d5fddNVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"
    hashobj = hashlib.md5(str_1.encode("utf-8"))
    return hashobj.hexdigest()

def kugou_getlist(Keyword):
    Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
    clienttime = str(round(time.time() * 1000))
    signature = signature_generator_2(Keyword, clienttime)
    request_url = f'https://complexsearch.kugou.com/v2/search/song?callback=callback123&srcappid=2919&clientver=1000&clienttime={clienttime}&mid=5c8dee1cc08f313b60b807d8da2d5fdd&uuid=5c8dee1cc08f313b60b807d8da2d5fdd&dfid=1txHuC3KMsDa1MoTkF1HWQUX&keyword={Keyword}&page=1&pagesize=30&bitrate=0&isfuzzy=0&inputtype=0&platform=WebFilter&userid=0&iscorrection=1&privilege_filter=0&filter=10&token=&appid=1014&signature={signature}'
    resp = requests.get(request_url, headers=Headers)
    if resp.text != '':
        resp_js = resp.text[12:(len(resp.text) -2)]
        songlist_dict = json.loads(resp_js)
        if songlist_dict['status'] == 1:
            songlist = songlist_dict['data']['lists']
            file_list = []
            for i in songlist:
                if i['PayType'] != 0:
                    file_list.append([i['FileName'],i['EMixSongID'],'【VIP】'])
                else:
                    file_list.append([i['FileName'],i['EMixSongID'],''])
            return file_list
    return 0

def kugou_download(file_list,inp,savepath,token2):
    encode_album_audio_id = file_list[inp - 1][1]
    clienttime = str(round(time.time() * 1000))
    signature = signature_generator_1(encode_album_audio_id, clienttime,token2)
    Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
    request_url = f'https://wwwapi.kugou.com/play/songinfo?srcappid=2919&clientver=20000&clienttime={clienttime}&mid=3bbc1d969ff662635c996e5f73d0a7e1&uuid=3bbc1d969ff662635c996e5f73d0a7e1&dfid=11RUG41l0SmY4ZVgnP0fnD0e&appid=1014&platid=4&encode_album_audio_id={encode_album_audio_id}&token=cc953c223e1dcc686b2dfc1a2465e6de{token2}&userid=1501763160&signature={signature}'
    resp = requests.get(request_url, headers=Headers)
    if resp.text != '':
        songinfo_dict = json.loads(resp.text)
        if songinfo_dict['status'] == 1:
            play_url = songinfo_dict['data']['play_url']
            song_resp = requests.get(play_url, headers=Headers)
            with open(f'{savepath}\\{sanitize_filename(file_list[inp - 1][0])}.mp3','wb') as f:
                f.write(song_resp.content)
                f.close()
                return 1
    return 0

def convert_to_mp3(input_file, output_file):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="mp3", bitrate="192k")

def get_name(songid):
    Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
    request_url = f'https://music.163.com/song?id={songid}'
    try:
        resp = requests.get(request_url, headers=Headers)
        soup = BeautifulSoup(resp.text, 'html.parser')
        match = re.search(f'{'data-res-name='}(.*?){'data-res-pic='}', str(soup))
        if match:
            name = match.group(1).replace('\"', '')
            return name
        else:
            return 'Unknown'
    except:
        return 'NE'

def sanitize_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def uc_decode(filename:str, savepath:str, temppath:str):
    with open(filename, 'rb') as f:
        data = f.read()

    databyte = bytearray(data)
    for i in range(len(databyte)):
        databyte[i] ^= 163
    song_name = sanitize_filename(str(get_name(filename.split('\\')[-1].split('-')[0])))
    with open(temppath+'\\'+song_name+'.mp3', 'wb') as f:
        f.write(bytes(databyte))
    convert_to_mp3(temppath+'\\'+song_name+'.mp3', savepath+'\\'+song_name+'.mp3')
    os.remove(temppath+'\\'+song_name+'.mp3')


def load_history(history_path):
    if pathlib.Path(history_path).exists():
        with open(history_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("History file is corrupted. Initializing a new history.")
                return {"songs": {}, "total_count": 0}
    else:
        return {"songs": {}, "total_count": 0}
    
def save_history(history_path):
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=4, ensure_ascii=False)

def update_history_time(play_time):
    history_data["total_time"] += play_time

def update_history_song(song_name):
    if song_name not in history_data["songs"]:
        history_data["songs"][song_name] = {"play_count": 0}
    history_data["songs"][song_name]["play_count"] += 1
    history_data["total_count"] += 1

def print_history_summary():
    total_seconds = history_data["total_time"]
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    total_count = history_data["total_count"]
    print(f"You have played your favourite songs {total_count} times for {hours}h {minutes}m {seconds}s!")
    songs = history_data["songs"]
    sorted_songs = sorted(songs.items(), key=lambda x: x[1]["play_count"], reverse=True)
    print("Here are your favourite songs:")
    for song_name, data in sorted_songs:
        print(f"{data['play_count']}:\t{song_name.replace(".mp3","")}")

def handle_help():
    print('''
Command\t\t\tFunction
--------------------------------------------------------------------------
quit/exit/end/:q\tExit the program
check163/:163_cache\tShow 163music cache
decode/:d #\t\tDecode cached songs
clear163/:163_clear\tClear 163music cache
search//s #\t\tSearch in Kugou
download//d #\t\tDownload from Kugou
showlist/:l\t\tShow playlist
play/:p\t\t\tPlay/unpause
play/:p #\t\tPlay specific songs
add/:a #\t\tAdd to playlist
mode/:m #\t\tMode(cycle/single/random)
stop/:st\t\tStop playing
pause/:pa\t\tPause
next/:n\t\t\tNext song
last/previous/:prev\tPrevious song
restart/replay/:r\tRestart
volume/:vol #\t\tSet volume(1-100)
savelist/:sl\t\tShow save list
save/:s lis/bgm\t\tMove songs to library
clear/:cl\t\tClear save list
library/:lib\t\tShow library
lookup #/:lu\t\tSearch in library
timelimit/:tl #\t\tSet play time limit
history/:his\t\tShow history
?/:?\t\t\tCurrent song
--------------------------------------------------------------------------
''')

def handle_quit(bgm, history_directory):
    bgm.stop()
    save_history(history_directory)
    return 0

def handle_check163(cache_directory):
    songnames = []
    files = [os.path.join(cache_directory, f) for f in os.listdir(cache_directory) if f.endswith(".uc")]
    files.sort(key=lambda f: os.path.getctime(f),reverse=True)
    if len(files) == 0:
        print('There is no file in your 163music Cache!')
        return songnames, files
    print(f'There is(are) {len(files)} file(s) here:')
    i = 1
    for file in files:
        name = get_name(file.split('\\')[-1].split('-')[0])
        if name == 'NE':
            print('Network error! Please check your network!')
            break
        else:
            songnames.append(name)
            print(f'{i}.\t{sanitize_filename(str(name))}')
            i += 1
    return songnames, files

def handle_clear163(cache_directory):
    for file in os.listdir(cache_directory):
        file_path = os.path.join(cache_directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print('163music cache list cleared!')

def handle_search(res, threshold):
    try:
        keyword = res.replace('search ','')
        kugou_list = kugou_getlist(keyword)
        if len(kugou_list) == 0:
            print(f'Cannot find any song with keyword {keyword}!')
            return kugou_list
        i = 1
        for kugou_song in kugou_list:
            print(f'{i}.\t'+str(kugou_song[2])+str(kugou_song[0]))
            i += 1
        return kugou_list
    except:
        print('Invalid command!')
        return []

def handle_download(res, kugou_list, save_directory, token2):
    try:
        download_list = list(map(int,res.split()[1:]))
        if len(kugou_list) == 0:
            print('Please search before downloading!')
            return
        elif len(download_list) == 0:
            print('Please key in the number of the song you want to download!')
            return
        print('Start downloading...')
        for i in download_list:
            try:
                result = kugou_download(kugou_list, i,save_directory,token2)
                if result == 1:
                    print(f'Successfully Downloaded: {kugou_list[i-1][0]}')
                else:
                    print(f'Cannot download song {i}: {kugou_list[i-1][0]}')
            except Exception as e:
                if i > len(kugou_list):
                    print(f'Invalid song number:{i}')
                else:
                    print(f'Cannot download song {i}: {kugou_list[i-1][0]}')
                    print(e)
        savelist = [f.name for f in pathlib.Path(save_directory).glob("*.mp3")]
    except:
        print('Invalid command!')

def handle_decode(res, files, songnames, save_directory, temp_directory, playlist):
    try:
        if len(files) == 0:
            print('Please key in \'check163\' before decoding!')
            return
        if len(res.split()) > 1:
            tmp = []
            for part in res.split()[1:]:
                if '-' in part:
                    try:
                        sta, end = map(int, part.split('-'))
                        if sta > end or sta < 1 or end > len(playlist):
                            print(f'Invalid range: {part}')
                        else:
                            tmp.extend(range(sta, end + 1))
                    except ValueError:
                        print(f'Invalid range format: {part}')
                else:
                    try:
                        num = int(part)
                        if num < 1 or num > len(playlist):
                            print(f'Invalid song number: {num}')
                        else:
                            tmp.append(num)
                    except ValueError:
                        print(f'Invalid song number: {part}')
            tmp = sorted(set(tmp))
            if not tmp:
                print('No valid song to decode!')
            else:
                decode_list = tmp
        else:
            print('Invalid input format!')
        if len(decode_list) == 0:
            print('Please key in the number of the song you want to decode!')
            return
        print('Start decoding...')
        for i in decode_list:
            try:
                uc_decode(files[i-1],save_directory,temp_directory)
                print(f'Successfully Decoded: {songnames[i-1]}')
            except:
                if i > len(files):
                    print(f'Invalid song number:{i}')
                else:
                    print(f'Cannot decode song {i}: {songnames[i-1]}')
        savelist = [f.name for f in pathlib.Path(save_directory).glob("*.mp3")]
        print('Mission Accomplished!')
    except:
        print('Invalid command!')

def handle_showlist(playlist):
    if len(playlist) == 0:
        print('There is no song in your playlist!')
    else:
        print('Your playlist:')
        i = 1
        for song in playlist:
            print(f'{i}.\t{song}')
            i += 1

def handle_play(res, bgm, playlist, mode):
    if res == 'play':
        bgm.unpause()
    else:
        try:
            if len(res.split()) > 1:
                tmp = []
                for part in res.split()[1:]:
                    if '-' in part:
                        try:
                            sta, end = map(int, part.split('-'))
                            if sta > end or sta < 1 or end > len(playlist):
                                print(f'Invalid song range: {part}')
                            else:
                                tmp.extend(range(sta, end + 1))
                        except ValueError:
                            print(f'Invalid range format: {part}')
                    else:
                        try:
                            num = int(part)
                            if num < 1 or num > len(playlist):
                                print(f'Invalid song number: {num}')
                            else:
                                tmp.append(num)
                        except ValueError:
                            print(f'Invalid song number: {part}')
                tmp = sorted(set(tmp))
                if not tmp:
                    print('No valid song to play!')
                else:
                    print('Start playing:')
                    for i in tmp:
                        print(f'{i}.\t{playlist[i-1]}')
                    selected_songs = [playlist[i-1] for i in tmp]
                    if mode == 'random':
                        random.shuffle(selected_songs)
                    bgm.set_playlist(selected_songs)
                    if bgm.nowmode in ['stop', 'pause'] or bgm.playing_songname not in bgm.playlist:
                        bgm.stop()
                        bgm.nowplaying = 0
                        bgm.play()
            else:
                print('Invalid input format!')
        except:
            print('Invalid command!')

def handle_mode(res, bgm, mode, playlist, sta, end):
    try:
        if res.split()[1] not in ['cycle','single','random']:
            print('Invalid mode!')
        else:
            if res.split()[1] != mode or res.split()[1] == 'random':
                print(f'Playing mode changed: {mode} -> {res.split()[1]}!')
                mode = res.split()[1]
                if mode == 'random':
                    bgm.is_single = 0
                    tmp = bgm.playlist
                    random.shuffle(tmp)
                    bgm.set_playlist(tmp)
                elif mode == 'single':
                    bgm.is_single = 1
                else:
                    bgm.is_single = 0
                    bgm.set_playlist(playlist[sta-1:end])
            else:
                print(f'Playing mode is already {mode}!')
        return mode
    except:
        print('Invalid command!')
        return mode

def handle_restart(bgm):
    bgm.play()

def handle_volume(res, bgm):
    try:
        volume = float(res.split()[1])
        if volume >= 1 and volume <= 100:
            volume = volume/100
        if volume >= 0 and volume < 1:
            bgm.set_volume(volume)
            print(f'Volume changed to {int(volume*100)}%!')
        else:
            print('Invalid volume!')
    except:
        print('Invalid volume!')

def handle_savelist(save_directory):
    savelist = [f.name for f in pathlib.Path(save_directory).glob("*.mp3")]
    if len(savelist) == 0:
        print('There is no song in your savelist!')
    else:
        print('Your savelist:')
        i = 1
        for song in savelist:
            print(f'{i}.\t{song}')
            i += 1

def handle_save(res, savelist, save_directory, play_directory, library_directory, playlist):
    try:
        if len(savelist) == 0:
            print('There is no song in your savelist!')
        else:
            if res.split()[1] not in ['lis','bgm']:
                print('Invalid save list!')
                print(res.split()[1])
            else:
                if res.split()[1] == 'lis':
                    for song in savelist:
                        if song not in playlist:
                            shutil.copy2(os.path.join(save_directory, song), play_directory)
                            shutil.copy2(os.path.join(save_directory, song), library_directory)
                            playlist.append(song)
                            os.remove(os.path.join(save_directory, song))
                    print('Songs moved to Lis and library!')
                else:
                    for song in savelist:
                        shutil.copy2(os.path.join(save_directory, song), library_directory)
                        os.remove(os.path.join(save_directory, song))
                    print('Songs moved to library!')
                savelist = []
    except:
        print('Invalid command!')
    return savelist

def handle_add(res, bgm, playlist, mode):
    try:
        if len(res.split()) > 1:
            tmp = []
            for part in res.split()[1:]:
                if '-' in part:
                    try:
                        sta, end = map(int, part.split('-'))
                        if sta > end or sta < 1 or end > len(playlist):
                            print(f'Invalid song range: {part}')
                        else:
                            tmp.extend(range(sta, end + 1))
                    except ValueError:
                        print(f'Invalid range format: {part}')
                else:
                    try:
                        num = int(part)
                        if num < 1 or num > len(playlist):
                            print(f'Invalid song number: {num}')
                        else:
                            tmp.append(num)
                    except ValueError:
                        print(f'Invalid song number: {part}')
            tmp = sorted(set(tmp))
            if not tmp:
                print('No valid song to add!')
            else:
                print('Added songs:')
                for i in tmp:
                    print(f'{i}.\t{playlist[i-1]}')
                selected_songs = [playlist[i-1] for i in tmp]
                if mode == 'random':
                    random.shuffle(selected_songs)
                bgm.add_playlist(selected_songs)
                if bgm.nowmode in ['stop', 'pause'] or bgm.playing_songname not in bgm.playlist:
                    bgm.stop()
                    bgm.nowplaying = 0
                    bgm.play()
        else:
            print('Invalid input format!')
    except:
        print('Invalid command!')

def handle_clear(savelist, save_directory):
    for song in savelist:
        os.remove(os.path.join(save_directory, song))
    savelist = []
    print('Save list cleared!')
    return savelist

def handle_stop(bgm):
    bgm.stop()

def handle_pause(bgm):
    bgm.pause()

def handle_next(bgm):
    bgm.next()
    print(f'Now playing:\t{bgm.playing_songname}')

def handle_last(bgm):
    bgm.last()
    print(f'Now playing:\t{bgm.playing_songname}')

def handle_library(library_directory):
    library_files = [f for f in pathlib.Path(library_directory).glob("*.mp3")]
    print('Your library:')
    i = 1
    for song in library_files:
        print(f'{i}.\t{song.name}')
        i += 1

def handle_lookup(res, library_directory, threshold):
    try:
        tolookup = res.split()[1]
        library = [f.name.replace('.mp3','') for f in pathlib.Path(library_directory).glob("*.mp3")]
        matches = fuzzy_match_all(tolookup, library, threshold)
        if matches:
            for match in matches:
                print(f"{match[0]}\t\tSimilarity: {int(match[1])}%")
        else:
            print("No matched song found.")
    except:
        print('Invalid command!')

def handle_timelimit(res, timelimit, lock):
    try:
        timelimit_tmp = int(res.split()[1])
        if timelimit_tmp > 0:
            with lock:
                timelimit[0] = timelimit_tmp*60 + int(time.time())
            # print(timelimit)
            print(f'Set time limit to {timelimit_tmp} minute(s).')
            newtime = datetime.datetime.now() + datetime.timedelta(minutes=timelimit_tmp)
            print(f"Keep playing until {newtime.strftime("%H")}:{newtime.strftime("%M")}:{newtime.strftime("%S")}.")
        else:
            print('Invalid time limit!')
    except:
        print('Invalid time limit!')

def handle_history():
    print_history_summary()

def handle_current_song(bgm):
    print(f'Now playing:\t{bgm.playing_songname}')

if __name__ == '__main__':
    res = ''
    songnames = []
    files = []
    kugou_list = []
    running = 1
    timelimit = [int(time.time()) + 1e9]
    mode = 'cycle'
    commands = [
        'help', ':h',
        'quit', 'exit', 'end', ':q',
        'check163', ':163_cache',
        'decode', ':d',
        'clear163', ':163_clear',
        'search', '/s',
        'download', '/d',
        'showlist', ':l',
        'play', ':p',
        'mode', 'single', 'cycle', 'random', ':m',
        'stop', ':st',
        'pause', ':pa',
        'next', ':n',
        'restart', 'replay', ':r',
        'volume', ':vol',
        'savelist', ':sl',
        'save', 'lis', 'bgm', ':s',
        'add', ':a',
        'clear', ':cl',
        'library', ':lib',
        'lookup', ':lu',
        'timelimit', ':tl',
        'history', ':his',
        '?', ':?',
        'last', 'previous', ':prev']
    completer = FuzzyCompleter(
        WordCompleter(
            commands,
            ignore_case=True,
            match_middle=True,  # 允许中间匹配
            sentence=True       # 按完整单词匹配
        )
    )
    session = PromptSession(completer=completer)
    with open("savedata.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        cache_directory = lines[0].strip()
        save_directory = lines[1].strip()
        temp_directory = lines[2].strip()
        play_directory = lines[3].strip()
        library_directory = lines[4].strip()
        volume = float(lines[5].strip())
        threshold = int(lines[6].strip())
        token2 = lines[7].strip()
        history_directory = lines[8].strip()
    folder = pathlib.Path(play_directory)
    mp3_files = [f for f in folder.glob("*.mp3")]
    sorted_files = sorted(mp3_files, key=lambda f: f.stat().st_mtime)
    playlist = [f.name for f in sorted_files]
    savelist = [f.name for f in pathlib.Path(save_directory).glob("*.mp3")]
    with open(history_directory, "r", encoding="utf-8") as f:
        lines = f.readlines()
        history_data = load_history(history_directory)
    sta = 1
    end = len(playlist)
    bgm = player(play_directory, playlist, volume)
    lock = threading.Lock()
    thread = threading.Thread(target=keep_checking, args=(bgm,timelimit,lock), daemon=True)
    thread.start()
    print('-------------------------------------------------------------------------------------------------')
    print('|Copyright © 2025 aaaaa. All rights reserved.\t\t\t\t\t\t\t|')
    print('|    This software and associated documentation files (the "Software") may not be used, copied,\t|')
    print('|modified, or distributed without prior written permission from the author.\t\t\t|')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome to musician! Please key in your Command. Key in \'help\' to view more information.')

    while running:
        print()
        res = str(session.prompt('>> ')).strip().lower()
        if res in ['help', ':h']:
            handle_help()
        elif res in [':q', 'quit', 'exit', 'end']:
            running = handle_quit(bgm, history_directory)
        elif res in [':163_cache', 'check163']:
            songnames, files = handle_check163(cache_directory)
        elif res == [':163_clear', 'clear163']:
            handle_clear163(cache_directory)
        elif 'search' in res or '/s' in res:
            kugou_list = handle_search(res, threshold)
        elif 'download' in res or '/d' in res:
            handle_download(res, kugou_list, save_directory, token2)
        elif 'decode' in res or ':d' in res:
            handle_decode(res, files, songnames, save_directory, temp_directory, playlist)
        elif res in [':l', 'showlist']:
            handle_showlist(playlist)
        elif 'play' in res or ':p' in res:
            handle_play(res, bgm, playlist, mode)
        elif 'mode' in res or ':m' in res:
            mode = handle_mode(res, bgm, mode, playlist, sta, end)
        elif res in [':r', 'restart', 'replay']:
            handle_restart(bgm)
        elif 'volume' in res or ':vol' in res:
            handle_volume(res, bgm)
        elif res in [':sl' ,'savelist']:
            handle_savelist(save_directory)
        elif 'save' in res or ':s' in res:
            savelist = handle_save(res, savelist, save_directory, play_directory, library_directory, playlist)
        elif 'add' in res or ':a' in res:
            handle_add(res, bgm, playlist, mode)
        elif res in [':cl' ,'clear']:
            savelist = handle_clear(savelist, save_directory)
        elif res in [':st', 'stop']:
            handle_stop(bgm)
        elif res in [':pa','pause']:
            handle_pause(bgm)
        elif res in [':n','next']:
            handle_next(bgm)
        elif res in [':prev', 'last', 'previous']:
            handle_last(bgm)
        elif res in [':lib', 'library']:
            handle_library(library_directory)
        elif 'lookup' in res or ':lu' in res:
            handle_lookup(res, library_directory, threshold)
        elif 'timelimit' in res or ':tl' in res:
            handle_timelimit(res, timelimit, lock)
        elif res in [':his', 'history']:
            handle_history()
        elif res in [':?', '?']:
            handle_current_song(bgm)
        elif res == '':
            continue
        else:
            print(f'\'{res}\': Invalid command!')
        bgm.check_play()