# Musician
## An individual music player with a little bit more functions.

Code by *aaaaa*.  

**Musician** is a music player controlled by the **command line**.  It is designed for **Coders** to **listen to music**, **download** from *Kugou* or *163music* **for free**, **build your own music library** and **record your personalized listening history**.  

Due to the limited code power of the writer, the program is written in **python** and the music-playing part of the program is powered by *pygame*. It may include some bugs, and hopefully you can point them out and I'll fix them as far as I can.  

### Let's have a brief overview over the program!

There are totally 6 files under the path musician: 

```
musician/
├── history.txt
├── Icon.ico
├── musician.exe
├── musician.py
├── README.md
└── savedata.txt
```

As a coder, you may focus on  `musician.py` and `savedata.txt` .

As a user, you can just check your `savedata.txt` **on the first use** and run `musician.exe` to enjoy your time with music!  

### As a user, I should:  

#### Check the `savedata.txt` and modify the path accordingly. 

+ The `savedata.txt` file is as below:  

```
C:\Users\Netease\CloudMusic\Cache\Cache
D:\BGM\Download&Decode
D:\BGM\Download&Decode\temp
D:\BGM\Lis
D:\BGM
0.4
30
1d4e5b7decbe434048e596ae2d597adb
D:\BGM\Settings\history.txt

备注：
网易云音乐缓存目录
音乐下载/解码目录
解码临时目录
听歌目录
曲库目录
默认音量
搜索匹配度下限
酷狗音乐token后32位
history.txt路径(2025.4.24更新)
```

+ For the first line, you can open your **NetEase Cloud Music for desktop** , search for the **Download** part and find the **Cache Path**. Just **copy** it to the first line of the `savedata.txt` and **add an extra '\Cache' at the end of the line** . This will guarantee that the program can catch the cache of 163Music and then decode them into `.mp3` files to save.  

+ For line 2 ~ 5, you can create a folder with your favourite name (here I call it **BGM**) as your **library** and create folders as below:  

  ```
  BGM/
  ├── Download&Decode/
  │   └── temp/
  └── Lis/
  ```

​	Then, just **copy** the path of **Download&Decode**, **temp**, **Lis**, **BGM** into line 2~5 separately.  

​	Your playlist for listening will be saved in **BGM/Lis**, which you will be able to manage both 	automatically and manually. 

​	You may ignore the **Download&Decode** folder, since it is used for save temporary files. Just 	create it for me and I'll handle the rest.  

+ Line 6 and 7 controlled the default volume and the lower limit of search matching degree. You may just keep it unchanged.  

+ Line 8 is the last 32 bits of the token of **Kugou**. Since **Kugou**'s token keeps changing, I leave an interface here for downloading songs from **Kugou**.   

  **You may skip this step if you think it troublesome or difficult, and you will not be able to download songs from Kugou then.**  

  + First, visit [酷狗音乐](https://www.kugou.com/) and log in (or you cannot visit the player page).  
  + Second, search for an arbitrary song and play it.  
  + Then, right click on the webpage and select **'Check'**. Select the **Network** page and use `Ctrl+R` to **refresh the webpage**. Search the request list for `https://wwwapi.kugou.com/play/songinfo?` and select it. You can find the last 32 bits of the token **inside the request URL** such as:  
  + wwwapi.kugou.com/play/songinfo?srcappid=2919&clientver=20000&clienttime=1747819212303&mid=3bbc1d969ff662635c996e5f73d0a7e1&uuid=3bbc1d969ff662635c996e5f73d0a7e1&dfid=11RUG41l0SmY4ZVgnP0fnD0e&appid=1014&platid=4&encode_album_audio_id=7uzljr6e&token=cc953c223e1dcc686b2dfc1a2465e6de**<u>55f2409f72970daa21bdc63acee305db</u>**&userid=1501763160&signature=13c5c92705e9d037fc74bc884d01c846
  + **Copy** it into line 8 of `savedata.txt` and you can search and download songs from **Kugou** by **simply typing in commands** now!  

+ Line 9 (the last line) saves the path of `history.txt`. You can just choose the path you like and save it there. **You may not need to visit `history.txt` from now on** since you can check your history in the program.  
+ **Congratualtions! You have successfully done everything with settings! Enjoy your journey with _musician_ now!** 



#### Master the program commands in minutes!

There are lots of commands supported by the program, but it's quite easy to master. 

You can just key in commands whenever you see `>>` at the very beginning of a new line and then press  Enter. **All commands are case insensitive.**

Let's introduce them one by one! **Follow me and have a try!**  

- `quit`/`exit`/`end`
  Exit the program with any of the commands.

  - **Always exit the program with commands, or the history-recording may make mistakes.**

- `help`

  Print a brief introduction of every command.

- `check163`
  Check and print 163music cache list.

  - If it replies *'Network Error'*, **Check your network connection with [网易云音乐](https://music.163.com/#)**.   
  - **Do not `check163` too frequently or `check163` with too many songs inside your cache list. Otherwise, 163music may ban your IP and refuse to respond to your request!**  

- `decode` *`#`*
  Decode songs in 163music cache list. Such as: `decode 3` or `decode 2 5-9 4`.  

  - **Always `check163` before `decode`! **  

- `clear163`
  Clear the 163music cache list. 

  - **Do not `clear163` while running NetEase Cloud Music or the program may crash!**  

- `search` *`#`*
  Search song in Kugou. Such as: `search 夏の紫苑`

  - If it replies *'Cannot download song'* , **reset** the token in `savedata.txt` and try again.  

- `download` *`#`*
  Download songs from Kugou.

  - Songs marked as `【VIP】` **cannot** be fully downloaded, unless the account you log in with have access to VIP songs.  

- `showlist`
  Show the play list. Those are songs in your `Lis` folder.

- `play`
  Play or unpause the song.

- `play` *`#`*
  Choose songs in `Lis` to play. Such as: `play 5` or `play 4-7 2 3-8`.

  - The program will automatically deduplicate the songs you entered and sort them in ascending order.  

- `add` *`#`*
  Add songs to the play list. Such as: `add 5` or `add 4-7 2 3-8`.

- `mode` *`#`*
  Change the playing mode.

  - There are totally 3 modes to choose from. 
    - `mode single` Single tune circulation.
    - `mode cycle` List loop.
    - `mode random` Play randomly.

- `stop`
  Stop playing.

- `pause`
  Pause the song.

- `last`/`previous`
  Play the previous song.

- `next`
  Play the next song.

- `restart`/`replay`
  Replay the song.

- `volume` *`#`*
  Change the volume.

  - You can change the volume to [1%, 100%]. Both `volume 0.4` and `volume 40` are valid.
  - The default volume is saved in `savedata.txt`, line 6.

- `savelist`
  Show the save list.

  - Save list is where you see your downloaded songs and decoded songs. You can choose to delete them, move them to both `BGM` and `Lis`, or just move them to `BGM`.

- `save` *`#`*
  Move songs in save list to the designated library and clear the save list.

  - `save Lis` Move all songs in save list to both `BGM` and `Lis`.
  - `save BGM` Move all songs in save list to `BGM`.

- `clear`
  Clear the save list.

- `library`
  Show the `BGM` library.

- `lookup` *`#`*
  Lookup a song in the library.

- `timelimit` *`#`*
  Set time limit (minutes) for song playing. Such as: `timelimit 45` for a 45-minute journey with music.

  - Decimals or negative numbers are invalid.

- `history`
  Show your listening history.

- `?`
  Show the current playing song.

#### Enjoy your journey with musician !



### As a coder, I should:  

#### Take a glance of the settings and commands above first.

#### Check the code in `musician.py` then.  

Hopefully you can easily understand it since you are a coder. (●'◡'●)