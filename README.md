# :memo: nonebot_plugin_zyk_music

**本插件是我另一个项目改的，有兴趣的话可以去看看[BlackStone_Music_GUI](https://github.com/ZYKsslm/BlackStone_Music_GUI)**

*:page_facing_up: 使用本插件前请仔细阅读README*

## :sparkles: 新版本一览
### :pushpin: version 0.1.6
>都更新了哪些内容？
1. 修复了在默认文件保存路径下找不到文件的BUG
2. 增加导入歌单功能，目前只支持qq音乐的歌单，可直接从歌单点歌


## :cd: 安装方式
- #### 使用pip
```
pip install nonebot_plugin_zyk_music
```
- #### 使用nb-cli
```
nb plugin install nonebot_plugin_zyk_music
```

## :wrench: env配置

|        Name         |      Example       | Type |        Usage         | Required |
|:-------------------:|:------------------:|:----:|:--------------------:|:--------:|
|  music_proxy_port   |       10809        | int  |    本地代理端口，若有代理则需要    |    No    |
|     music_path      | path/to/your/music | str  | 音乐保存路径，默认保存在music目录下 |    No    |
|   music_del_file    |       False        | bool |  是否删除下载的文件，默认为True   |    No    |
| music_retry_songnum |         50         | int  |    歌单发送失败时重新发送的条数    |    No    |


## :bulb: 如何交互

### 点歌
![interaction](interaction.gif)

### 导入歌单
![impt_songlist](impt_songlist.gif)

## :label: 指令
### 支持的平台
- [x] QQ音乐
- [x] 网易云音乐
- [x] 酷狗音乐
- [x] 酷我音乐
- [x] 咪咕音乐


### QQ点歌
```
qq | QQ点歌 name

eg：
    qq点歌 stay
```

### QQVIP点歌
```
qqvip | QQVIP点歌 [母带|无损|HQ|标准音质] name

eg：
    qq点歌 无损音质 one last kiss
```

### 酷狗点歌
```
酷狗 | kg点歌 name

eg：
    kg点歌 stay
```

### 酷我点歌
```
酷我 | kw点歌 name

eg：
    kw点歌 stay
```

### 网易云点歌
```
网易云 | 网易 | wy点歌 name

eg：
    wy点歌 stay
```

### 咪咕点歌
```
咪咕 | mg点歌 name

eg：
    mg点歌 stay
```

### 导入QQ音乐歌单
```
(COMMAND_START)导入歌单 歌单id | 歌单链接

eg:
    /导入歌单 3865449936
```


---
:bug: 如果发现插件有BUG或有建议，欢迎**合理**提*Issue*

:heart: 最后，如果你喜欢本插件，就请给本插件点个:star:吧