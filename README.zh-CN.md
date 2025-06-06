# **Musician**

## **一个拥有曲库管理功能的命令行音乐播放器**

**代码 _aaaaa_**

**Musician** 是一个**命令行控制的音乐播放器**，专为**程序员音乐爱好者**设计，支持：

- 听歌
- 从**酷狗音乐**或**网易云音乐**免费下载歌曲
- 建立个人曲库
- 记录播放历史

程序使用 **Python** 编写，播放功能基于 **pygame**。由于作者编程水平有限，可能存在一些 Bug——欢迎反馈，我会尽力修复！

------

## **程序概览**

`musician` 目录包含以下文件：

```
musician/
├── BGM          	   # 默认的曲库目录  
├── Old_versions       # Musician的历史版本  
├── history.txt        # 播放历史记录  
├── Icon.ico           # 程序图标  
├── musician.exe       # 可执行文件（用户使用）  
├── musician.py        # 源代码（开发者查看）  
├── README.md          # 英文说明文档  
├── README.zh-CN.md    # 中文说明文档  
└── savedata.txt       # 配置文件  
```

- **用户**：修改 `savedata.txt`（仅首次配置），然后运行 `musician.exe`。
- **开发者**：可查看 `musician.py` 和 `savedata.txt`。

------

## **用户指南**

### **1. 配置 `savedata.txt`**

该文件定义了路径和设置：

```
C:\Users\Netease\CloudMusic\Cache\Cache   # 网易云音乐缓存路径  
BGM\Download&Decode                   	  # 下载/解码目录  
BGM\Download&Decode\temp                  # 临时文件存放  
BGM\Lis                                   # 播放列表文件夹  
BGM                                       # 主音乐库  
0.4                                       # 默认音量（0–1）  
30                                        # 搜索匹配阈值（%）  
1d4e5b7decbe434048e596ae2d597adb          # 酷狗 token（后32位）  
BGM\Settings\history.txt                  # 历史记录文件路径  
```

#### **配置步骤**

1. **网易云缓存路径（必要）**

   - 打开 **网易云音乐桌面端** → 设置 → 下载 → **复制缓存路径**。
   - 在路径末尾手动添加 `\Cache`（如 `C:\...\Cache\Cache`）。

2. **音乐库文件夹【若不修改，则使用musician目录下的默认位置】**
   创建以下目录（示例名称）：

   ```
   BGM/  
   ├── Download&Decode/  # 用于下载/解码  
   │   └── temp/         # 临时文件  
   └── Lis/              # 播放列表存放  
   ```

   将它们的路径填入 `savedata.txt` 的第 2–5 行。

3. **酷狗 Token（可选）**

   - 登录 酷狗音乐官网。
   - 播放任意歌曲 → 按 **F12** 打开开发者工具 → **Network（网络）** 标签。
   - 找到 `https://wwwapi.kugou.com/play/songinfo?` 的请求。
   - 复制 `token` 参数的**最后32位字符**，即在`...5e6de`之后的部分（如 `55f2409f72970daa21bdc63acee305db`）。
   - 粘贴到 `savedata.txt` 第 8 行。
   - *如果不需要使用酷狗下载音乐，可跳过此步。*

4. **历史记录文件【若不修改，则使用musician目录下的默认位置】**
   指定 `history.txt` 的路径（第 9 行）**并将给出的 `history.txt` 文件移到指定路径下**，程序会自动管理该文件。

------

### **2. 命令速查**

在 `>>` 后输入命令（不区分大小写，支持通过 `/` 或 `:` 简写命令）。

#### **基础操作**

|        命令         | 简写 |                     功能                      |
| :-----------------: | :--: | :-------------------------------------------: |
| `quit`/`exit`/`end` | `:q` | 退出程序（*尽可能不要用右上角的×退出程序*）。 |
|       `help`        | `:h` |                显示所有命令。                 |

#### **网易云音乐**

|      命令       |     简写     |                      功能                       |
| :-------------: | :----------: | :---------------------------------------------: |
|   `check163`    | `:163_cache` |    列出缓存歌曲（若报错，请检查网络连接）。     |
| `decode <编号>` | `:d <编号>`  | 解码歌曲（如 `decode 3` 或 `decode 2 5-9 4`）。 |
|   `clear163`    | `:163_clear` |      清空缓存（*先关闭网易云桌面端！*）。       |

#### **酷狗音乐**

|       命令        |    简写     |                  功能                   |
| :---------------: | :---------: | :-------------------------------------: |
|  `search <歌名>`  | `/s <歌名>` |     搜索（如 `search 夏の紫苑`）。      |
| `download <编号>` | `/d <编号>` | 下载（*VIP 歌曲需先登录酷狗VIP账号*）。 |

#### **播放控制**

|             命令             |     简写      |                   功能                   |
| :--------------------------: | :-----------: | :--------------------------------------: |
|        `play`/`pause`        |  `:p`/`:pa`   |               播放/暂停。                |
|        `play <编号>`         |  `:p <编号>`  |    播放指定歌曲（如 `play 1-3 5`）。     |
|         `add <编号>`         |  `:a <编号>`  |             添加到播放列表。             |
| `mode <single/cycle/random>` |  `:m <模式>`  | 设置播放模式（单曲循环/列表循环/随机）。 |
|            `stop`            |     `:st`     |                停止播放。                |
|      `last`/`previous`       |    `:prev`    |                 上一首。                 |
|            `next`            |     `:n`      |                 下一首。                 |
|      `restart`/`replay`      |     `:r`      |            重新播放当前歌曲。            |
|       `volume <数值>`        | `:vol <数值>` |   调整音量（0–100%，如 `volume 40`）。   |

#### **音乐库 & 历史**

|        命令        |     简写     |                             功能                             |
| :----------------: | :----------: | :----------------------------------------------------------: |
|     `savelist`     |    `:sl`     |                       显示已下载歌曲。                       |
|  `save <Lis/BGM>`  | `:s <目录>`  | 将歌曲移至 `Lis`（播放列表）与 `BGM`（音乐库）/仅移至`BGM`。 |
|      `clear`       |    `:cl`     |                        清空下载列表。                        |
|     `library`      |    `:lib`    |                         浏览音乐库。                         |
|  `lookup <歌名>`   | `:lu <歌名>` |                         搜索音乐库。                         |
| `timelimit <分钟>` | `:tl <分钟>` |           设置最长播放时间（如 `timelimit 45`）。            |
|     `history`      |    `:his`    |                        查看播放历史。                        |
|        `?`         |     `:?`     |                     显示当前播放的歌曲。                     |


---

**曲库以mp3格式为默认存储格式，其他格式的音频将无法播放。你可以将原本的个人曲库直接迁移到 `BGM` 和 `Lis` 列表下。**

**请务必在 `BGM` 和 `Lis` 列表下分别存放至少1个mp3文件，否则曲库会崩溃！** 

------

## **开发者说明**

1. 先阅读**用户指南**了解功能逻辑。
2. 查看 `musician.py`——代码应该还算易懂（大概）。😊
3. 在终端用指令 `pyinstaller --onefile musician.py -i Icon.ico` 来将 `.py` 文件打包成 `.exe` 文件。

------

**祝你在 Musician 的陪伴下享受音乐！** 🎵