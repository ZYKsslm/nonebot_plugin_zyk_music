from nonebot import get_driver
from os.path import join, abspath, dirname


# 获取全局配置
# 获取本地代理端口
try:
    port = get_driver().config.music_proxy_port
except AttributeError:
    port = None
    proxies = None
else:
    try:
        int(port)
    except ValueError:
        port = None
        proxies = None
    else:
        proxies = {
            "http://": f"http://127.0.0.1:{port}",
            "https://": f"http://127.0.0.1:{port}"
        }

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