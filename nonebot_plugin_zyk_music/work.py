# -*- coding: utf-8 -*-
from httpx import AsyncClient
from os import rename
from os.path import join, abspath, dirname
from random import choice
from re import sub, compile, findall, S
from filetype import guess
from nonebot.adapters.onebot.v11 import Event

try:
    from ujson import load, loads
except ModuleNotFoundError:
    from json import load, loads

kg_api = "http://ovooa.caonm.net/API/kgdg/api.php"
mg_api = "http://ovooa.caonm.net/API/migu/api.php"
qq_vip_api = "http://ovooa.caonm.net/API/QQ_Music"
qq_songlist_api = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_playlist_cp.fcg?cv=10000&ct=19&newsong=1&tpl=wk&id={}&g_tk=5381&platform=mac&g_tk_new_20200303=5381&loginUin=0&hostUin=0&format=json&inCharset=GB2312&outCharset=utf-8&notice=0&platform=jqspaframe.json&needNewCode=0"
qq_api = "http://ovooa.caonm.net/API/qqdg/api.php"
wy_api = "http://ovooa.caonm.net/API/wydg/api.php"

ua_path = join(abspath(dirname(__file__)), "User-Agent.json")
with open(ua_path, "r") as u:
    user_agent_json = load(u)


def get_id(event: Event):
    info = str(event.get_session_id())
    try:
        res = findall(r"group_(?P<group_id>\d+)_(?P<member_id>\d+)", info)[0]
    except IndexError:
        id_ = "private", info
    else:
        id_ = "group", res[0]

    return id_


def set_name(string):
    """剔除字符 /:*?"<>| Windows操作系统下文件或文件夹名字中不允许出现以上字符"""
    pattern = compile(r'[/:*?"<>|]')
    new_string = sub(pattern=pattern, repl="", string=string)

    return new_string


def get_user_agent():
    """获取随机UA"""
    user_agent = choice(choice(list(choice(user_agent_json).values())))
    return user_agent


# 解析歌单
async def import_songlist(info):
    try:
        songlist_id = int(info)
    except ValueError:
        try:
            songlist_id = findall(r'/(\d+)', info)[0]
        except IndexError:
            return False

    headers = {
        "User-Agent": get_user_agent()
    }
    url = qq_songlist_api.format(songlist_id)

    async with AsyncClient(headers=headers, follow_redirects=True, timeout=None) as client:
        resp = await client.get(url=url)
        data = resp.json()["data"]["cdlist"][0]

    song_list = data["songlist"]
    tags = ""
    for i in data["tags"]:
        tags += f":{i['name']}"

    songlist_info = f"歌单名:{data['dissname']}\n" \
                    f"创建者:{data['nickname']}\n" \
                    f"简介:{data['desc']}\n" \
                    f"总歌数:{data['total_song_num']}\n" \
                    f"浏览人数:{data['visitnum']}\n" \
                    f"标签:{tags}"

    return songlist_info, song_list, data["songids"].split(",")


# 酷狗音乐
async def kg_get_music(name):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "sc": 50
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None) as client:
        resp = await client.get(url=kg_api)
        music_info = loads(findall(r'"data": (\[.*\])', resp.text, S)[0])

    choice_list = ""
    for i, music in enumerate(music_info):
        music_name = music["name"]
        singers = music["singer"]

        choose = f"{i+1}.{music_name}-{singers}\n"
        choice_list += choose

    return choice_list, None


async def kg_download(name, n, path):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "n": n,
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None) as client:
        resp = await client.get(url=kg_api)
        try:
            music_info = resp.json() 
        except:
            return False
        else:
            music_info = music_info["data"]

    song = set_name(music_info["song"])
    singer = set_name(music_info["singer"])
    try:
        music = music_info["url"]
    except KeyError:
        return False

    async with AsyncClient(headers=headers, follow_redirects=True, timeout=None) as client:
        resp = await client.get(url=music)
        content = resp.content

    kind = guess(content)
    if kind is None:
        return False

    file_name = join(path, f"{song}-{singer}.{kind.extension}")
    with open(file_name, "wb") as f:
        f.write(content)

    return True, file_name, f"{song}-{singer}.{kind.extension}"


# 咪咕音乐
async def mg_get_music(name):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "sc": 50
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None) as client:
        resp = await client.get(url=mg_api)
        music_info = resp.json()["data"]

    choice_list = ""
    for i, music in enumerate(music_info):
        music_name = music["song"]
        singers = music["singer"]

        choose = f"{i+1}.{music_name}-{singers}\n"
        choice_list += choose

    return choice_list, None


async def mg_download(name, n, path):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "n": n,
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None) as client:
        resp = await client.get(url=mg_api)
        music_info = resp.json()["data"]

    song = set_name(music_info["musicname"])
    singer = set_name(music_info["singer"])
    try:
        music = music_info["musicurl"]
    except KeyError:
        return False

    async with AsyncClient(headers=headers, follow_redirects=True, timeout=None) as client:
        resp = await client.get(url=music)
        content = resp.content

    kind = guess(content)
    if kind is None:
        return False

    file_name = join(path, f"{song}-{singer}.{kind.extension}")
    with open(file_name, "wb") as f:
        f.write(content)

    return True, file_name, f"{song}-{singer}.{kind.extension}"


# QQ音乐VIP
async def vip_qq_get_music(name):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "limit": 50
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None) as client:
        resp = await client.get(url=qq_vip_api)
        music_info = resp.json()["data"]

    choice_list = ""
    songid_list = []
    for i, music in enumerate(music_info):
        music_name = music["song"]
        singers = music["singer"]
        songid = music["songid"]
        songid_list.append(songid)
        choice_list += f"{i+1}.{music_name}-{singers}\n"

    return choice_list, songid_list


async def vip_qq_download(br, path, songid):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "songid": songid,
        "br": br
    }    

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None) as client:
        resp = await client.get(url=qq_vip_api)
        try:
            info = resp.json()
        except:
            return False
    try:
        music_info = info["data"]
    except KeyError:
        return False

    song = set_name(music_info["song"])
    singer = set_name(music_info["singer"])
    music = music_info["music"]

    if br > 2:
        async with AsyncClient(headers=headers, follow_redirects=True, timeout=None) as client:
            resp = await client.get(url=music)
            content = resp.content

        kind = guess(content)
        if kind is None:
            return False

        file_name = join(path, f"{song}-{singer}.{kind.extension}")
        with open(file_name, "wb") as f:
            f.write(content)

    else:
        client = AsyncClient()
        async with client.stream(method="GET", url=music, headers=headers, follow_redirects=True, timeout=None) as r:
            with open(fr"{path}/{song}-{singer}", "wb+") as f:
                async for data in r.aiter_bytes(chunk_size=64*1024):
                    f.write(data)
                kind = guess(f)

            file_name = f"{path}/{song}-{singer}.{kind.extension}"
            rename(f"{path}/{song}-{singer}", file_name)

    return True, file_name, f"{song}-{singer}.{kind.extension}"


# QQ音乐
async def qq_get_music(name):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "sc": 50
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None) as client:
        resp = await client.get(url=qq_api)
        music_info = resp.json()["data"]

    choice_list = ""
    for i, music in enumerate(music_info):
        music_name = music["song"]
        singers = music["singers"]

        choose = f"{i+1}.{music_name}-{singers}\n"
        choice_list += choose

    return choice_list, None


async def qq_download(name, n, path):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "n": n
    }
    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None) as client:
        resp = await client.get(url=qq_api)
        info = resp.json()
    try:
        music_info = info["data"]
    except KeyError:
        return False

    song = set_name(music_info["Music"])
    singer = set_name(music_info["Singer"])
    music = music_info["Url"]

    async with AsyncClient(headers=headers, follow_redirects=True, timeout=None) as client:
        resp = await client.get(url=music)
        content = resp.content

    file_name = join(path, f"{song}-{singer}.mp3")
    with open(file_name, "wb") as f:
        f.write(content)

    return True, file_name, f"{song}-{singer}.mp3"


# 网易云音乐
async def wy_get_music(name):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "sc": 50
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None) as client:
        resp = await client.get(url=wy_api)
        music_info = resp.json()["data"]

    choice_list = ""
    for i, music in enumerate(music_info):
        music_name = music["song"]
        singer_list = music["singers"]
        singer_num = len(singer_list)
        singers = ""
        if singer_num > 1:
            singers = "、".join([f"{singer[s - 1]}" for s, singer in enumerate(singer_list)])
        else:
            singers = singer_list[0]
        choose = f"{i+1}.{music_name}-{singers}\n"
        choice_list += choose

    return choice_list, None


async def wy_download(name, n, path):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "n": n,
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None) as client:
        resp = await client.get(url=wy_api)
        music_info = resp.json()["data"]

    song = set_name(music_info["Music"])
    singer = set_name(music_info["Singer"])
    try:
        music = music_info["Url"]
    except KeyError:
        return False

    async with AsyncClient(headers=headers, follow_redirects=True, timeout=None) as client:
        resp = await client.get(url=music)
        content = resp.content

    kind = guess(content)
    if kind is None:
        return False

    file_name = join(path, f"{song}-{singer}.{kind.extension}")
    with open(file_name, "wb") as f:
        f.write(content)

    return True, file_name, f"{song}-{singer}.{kind.extension}"


# 定义一个字典，存储不同的音乐源和对应的函数
music_sources = {
    "qq": (qq_get_music, qq_download),
    "QQ": (qq_get_music, qq_download),
    "qqvip": (vip_qq_get_music, vip_qq_download),
    "QQVIP": (vip_qq_get_music, vip_qq_download),
    "酷狗": (kg_get_music, kg_download),
    "kg": (kg_get_music, kg_download),
    "网易云": (wy_get_music, wy_download),
    "网易": (wy_get_music, wy_download),
    "wy": (wy_get_music, wy_download),
    "咪咕": (mg_get_music, mg_download),
    "mg": (mg_get_music, mg_download)
}

# 定义一个列表或者集合，存储需要音质参数的音乐源
vip_sources = {"qqvip", "QQVIP"}

async def get_music(source, name=None, songid=None, br=None, path=None, n=None):
    # 从字典中获取对应的函数
    get_data, download_data = music_sources[source]
    
    if (songid is None) and (n is None):
        # 调用下载音乐的函数
        return await get_data(name=name)
    else:
        # 判断是否需要传入音质参数
        if source in vip_sources:
            return await download_data(br, path, songid)
        else:
            return await download_data(name, n, path)