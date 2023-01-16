# :memo: nonebot_plugin_zyk_music

**本插件是我另一个项目改的，有兴趣的话可以去看看[BlackStone_Music_GUI](https://github.com/ZYKsslm/BlackStone_Music_GUI)**

*:page_facing_up: 使用本插件前请仔细阅读README*

## :sparkles: 新版本一览
### :pushpin: version 0.1.5
>都更新了哪些内容？
1. 代码几乎全部重写  ~~从另一个项目复制的~~，优化代码结构
2. 增加一个音源 *QQVIP*，支持点会员歌曲
3. QQVIP支持选择音质，具体看后文指令
4. 增加了两个env配置项，具体看后文env配置

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

|       Name       |      Example       | Type |        Usage         | Required |
|:----------------:|:------------------:|:----:|:--------------------:|:--------:|
| music_proxy_port |       10809        | int  |    本地代理端口，若有代理则需要    |    No    |
|    music_path    | path/to/your/music | str  | 音乐保存路径，默认保存在music目录下 |    No    |
|  music_del_file  |       False        | bool |  是否删除下载的文件，默认为True   |    No    |


## :bulb: 如何交互
![interaction](interaction.gif)

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

例：
    qq点歌 stay
```

### QQVIP点歌
```
qqvip | QQVIP点歌 [母带|无损|HQ|标准音质] name

例：
    qq点歌 无损音质 one last kiss
```

### 酷狗点歌
```
酷狗 | kg点歌 name

例：
    kg点歌 stay
```

### 酷我点歌
```
酷我 | kw点歌 name

例：
    kw点歌 stay
```

### 网易云点歌
```
网易云 | 网易 | wy点歌 name

例：
    wy点歌 stay
```

### 咪咕点歌
```
咪咕 | mg点歌 name

例：
    mg点歌 stay
```



---
:bug: 如果发现插件有BUG或有建议，欢迎**合理**提*Issue*

:heart: 最后，如果你喜欢本插件，就请给本插件点个:star:吧