# :memo: nonebot_plugin_zyk_music

**本插件是我一个音乐下载工具改的，有兴趣的话可以去看看[BlackStone_Music_GUI](https://github.com/ZYKsslm/BlackStone_Music_GUI)**

*:page_facing_up: 使用本插件前请仔细阅读README，文档中写明的问题一律不回答*

## 安装方式
- #### 使用pip
```
pip install nonebot_plugin_zyk_music
```
- #### 使用nb-cli
```
nb plugin install nonebot_plugin_zyk_music
```

## :wrench: env配置
配置项并不多，只有一个，而且是选填

|       Name       |                    Example                    | Type |  Usage   |
|:----------------:|:---------------------------------------------:|:----:|:--------:|
| music_proxy_port |                     10809                     | int  |  本地代理端口  |

当你电脑开了梯子的时候则需要填写代理使用的的本地端口*或使用指令发送给机器人*，并确保开着代理，不然可能发送不了请求 *（报EOF相关的错误）*

如果你使用了我的另一个插件[nonebot_plugin_zyk_novelai](https://github.com/ZYKsslm/nonebot_plugin_zyk_novelai)，并配置了其本地代理端口时，则本插件不需要再另外配置

## :bulb: 如何交互
![interaction](interaction.gif)

## :label: 指令
### 支持的平台
- [x] QQ音乐
- [x] 网易云音乐
- [x] 酷狗音乐
- [x] 酷我音乐
- [x] 咪咕音乐

- #### 设置本地代理端口
```
set_mport:10809
```
>#### :zap:
>#### 附功能
> 无代理模式
> ```
> set_mport:None
> ```
> **注意，None开头为大写**

- #### QQ点歌
```
qq | QQ点歌 name

例：
    qq点歌 stay
```

- #### 酷狗点歌
```
酷狗 | kg点歌 name

例：
    kg点歌 stay
```

- #### 酷我点歌
```
酷我 | kw点歌 name

例：
    kw点歌 stay
```

- #### 网易云点歌
```
网易云 | 网易 | wy点歌 name

例：
    wy点歌 stay
```

- #### 咪咕点歌
```
咪咕 | mg点歌 name

例：
    mg点歌 stay
```



---
:heart: 最后，如果你喜欢本插件，就请给本插件点个:star:吧
