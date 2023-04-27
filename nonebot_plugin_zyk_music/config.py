from nonebot import get_driver
from os.path import join, abspath, dirname


# 获取全局配置

# 获取文件路径
try:
    path = get_driver().config.music_path
except AttributeError:
    path = join(abspath(dirname(__file__)), "music")


# 是否删除文件
try:
    if_del = get_driver().config.music_del_file
except AttributeError:
    if_del = True
else:
    if if_del == "True":
        if_del = True
    else:
        if_del = False

# 歌单发送失败时发送的条数
try:
    song_num = get_driver().config.music_retry_songnum
except AttributeError:
    song_num = 50
else:
    try:
        song_num = int(song_num)
    except ValueError:
        song_num = 50
