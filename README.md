# **Musician**

## A Command-Line Music Player with Extra Features

**Code by _aaaaa_**

**Musician** is a **command-line-controlled music player** designed for **coders** who want to:

- Listen to music
- Download songs for free from **Kugou** or **163music**
- Build a personal music library
- Track listening history

The program is written in **Python**, with music playback powered by **pygame**. Due to the author's limited coding expertise, there may be bugs—feel free to report them, and I'll fix them as best I can!

------

## **Program Overview**

The `musician` directory contains the following files:

```
musician/
├── history.txt        # Listening history log  
├── Icon.ico           # Program icon  
├── musician.exe       # Executable (for users)  
├── musician.py        # Source code (for developers)  
├── README.md          # Documentation  
└── savedata.txt       # Configuration file  
```

- **For users**: Modify `savedata.txt` (first-time setup) and run `musician.exe`.
- **For coders**: Inspect `musician.py` and `savedata.txt`.

------

## **User Guide**

### **1. Configure `savedata.txt`**

The file defines paths and settings:

```
C:\Users\Netease\CloudMusic\Cache\Cache   # NetEase Cloud Music cache path  
D:\BGM\Download&Decode                    # Download/decode directory  
D:\BGM\Download&Decode\temp               # Temporary files  
D:\BGM\Lis                                # Playlist folder  
D:\BGM                                    # Main library  
0.4                                       # Default volume (0–1)  
30                                        # Search match threshold (%)  
1d4e5b7decbe434048e596ae2d597adb          # Kugou token (last 32 chars)  
D:\BGM\Settings\history.txt               # History file path  
```

#### **Setup Instructions**

1. **NetEase Cache Path**

   - Open **NetEase Cloud Music Desktop** → Settings → Download → **Copy Cache Path**.
   - Append `\Cache` to the path (e.g., `C:\...\Cache\Cache`).

2. **Library Folders**
    Create these directories (example names):

   ```
   BGM/  
   ├── Download&Decode/  # For downloads/decoding  
   │   └── temp/         # Temporary files  
   └── Lis/              # Playlist storage  
   ```

   Update lines 2–5 in `savedata.txt` with their paths.

3. **Kugou Token (Optional)**

   - Log in to Kugou Music.
   - Play any song → Open **Browser DevTools (F12)** → **Network** tab.
   - Find a request to `https://wwwapi.kugou.com/play/songinfo?`.
   - Copy the **last 32 characters** of the `token` parameter after `...5e6de` (e.g., `55f2409f72970daa21bdc63acee305db`).
   - Paste into line 8 of `savedata.txt`.
   - *Skip if you don’t need Kugou downloads.*

4. **History File**
    Specify a path for `history.txt` (line 9) and **move the `history.txt` file to the path** . Then, the program will manage this file automatically.

------

### **2. Command Reference**

Type commands after `>>` (case-insensitive).

#### **Basic Controls**

| Command             | Action                                 |
| ------------------- | -------------------------------------- |
| `quit`/`exit`/`end` | Exit the program (*always use this!*). |
| `help`              | Show all commands.                     |

#### **NetEase 163music**

| Command      | Action                                                       |
| ------------ | ------------------------------------------------------------ |
| `check163`   | List cached songs. (*Check network if "Network Error" occurs.*) |
| `decode <#>` | Decode songs (e.g., `decode 3` or `decode 2 5-9 4`).         |
| `clear163`   | Clear cache (*close NetEase first!*).                        |

#### **Kugou Music**

| Command         | Action                                                  |
| --------------- | ------------------------------------------------------- |
| `search <song>` | Search (e.g., `search 夏の紫苑`).                       |
| `download <#>`  | Download. (*VIP songs require login with VIP account.*) |

#### **Playback**

| Command                      | Action                                                  |
| ---------------------------- | ------------------------------------------------------- |
| `play`/`pause`               | Play/pause.                                             |
| `play <#>`                   | Play specific songs (e.g., `play 1-3 5`).               |
| `add <#>`                    | Add to playlist.                                        |
| `mode <single/cycle/random>` | Set playback mode.                                      |
| `stop`                       | Stop playback.                                          |
| `last`/`previous`            | Play the previous song.                                 |
| `next`                       | Play the next song.                                     |
| `restart`/`replay`           | Replay current song.                                    |
| `volume <#>`                 | Set volume (0–100%, e.g., `volume 40` or `volume 0.4`). |

#### **Library & History**

| Command               | Action                                             |
| --------------------- | -------------------------------------------------- |
| `savelist`            | Show downloaded songs.                             |
| `save <Lis/BGM>`      | Move songs to `Lis` (playlist) or `BGM` (library). |
| `clear`               | Clear savelist.                                    |
| `library`             | Browse library.                                    |
| `lookup <song>`       | Search library.                                    |
| `timelimit <minutes>` | Set max playtime (e.g., `timelimit 45`).           |
| `history`             | Show listening history.                            |
| `?`                   | Show currently playing song.                       |

---

**_Musician_ uses `.mp3` to store all the music, and music in other formats is not supported for playback. You can also add your original music library into folder `BGM` and `Lis` .**

**Please add at least one `.mp3` file in folder `BGM` and `Lis` , or the _musician_ may crash !**

------

## **For Coders**

1. Review the **User Guide** above for context.
2. Inspect `musician.py`—the code is straightforward (hopefully)! 😊
3. Use `pyinstaller --onefile musician.py -i Icon.ico` to pack up the `.py` code into a `.exe` file.

------

**Enjoy your music journey with Musician!** 🎵