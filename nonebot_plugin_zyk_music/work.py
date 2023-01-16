# -*- coding: utf-8 -*-
from httpx import AsyncClient
from os import rename
from os.path import join, abspath, dirname
from random import choice
from re import sub, compile, findall
from filetype import guess
from nonebot.adapters.onebot.v11 import Event

try:
    from ujson import load, dump
except ModuleNotFoundError:
    from json import load, dump

kw_api = "http://ovooa.com/API/kwdg/api.php"
kg_api = "http://ovooa.com/API/kgdg/api.php"
mg_api = "http://ovooa.com/API/migu/api.php"
qq_vip_api = "http://ovooa.com/API/QQ_Music"
qq_api = "http://ovooa.com/API/qqdg/api.php"
wy_api = "http://ovooa.com/API/wydg/api.php"

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


async def get_music(mode, source, name, proxies, br=None, path=None, n=None):
    if source == "酷我" or source == "kw":
        if mode == "list":
            return await kw_get_music(name=name, proxies=proxies)
        else:
            return await kw_download(name, n, path, proxies)

    elif source == "qq" or source == "QQ":
        if mode == "list":
            return await qq_get_music(name=name, proxies=proxies)
        else:
            return await qq_download(name, n, path, proxies)

    elif source == "qqvip" or source == "QQVIP":
        if mode == "list":
            return await vip_qq_get_music(name=name, proxies=proxies)
        else:
            return await vip_qq_download(name, n, br, path, proxies)

    elif source == "酷狗" or source == "kg":
        if mode == "list":
            return await kg_get_music(name=name, proxies=proxies)
        else:
            return await kg_download(name, n, path, proxies)

    elif source == "网易云" or source == "网易" or source == "wy":
        if mode == "list":
            return await wy_get_music(name=name, proxies=proxies)
        else:
            return await wy_download(name, n, path, proxies)

    elif source == "咪咕" or source == "mg":
        if mode == "list":
            return await mg_get_music(name=name, proxies=proxies)
        else:
            return await mg_download(name, n, path, proxies)


# 酷我音乐
async def kw_get_music(name, proxies):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "sc": 50
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None, proxies=proxies) as client:
        resp = await client.get(url=kw_api)
        music_info = resp.json()["data"]

    choice_list = ""
    for i in range(len(music_info)):
        music_name = music_info[i]["song"]
        singers = music_info[i]["singer"]

        choose = f"{i+1}.{music_name}-{singers}\n"
        choice_list += choose

    return choice_list


async def kw_download(name, n, path, proxies):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "n": n,
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None, proxies=proxies) as client:
        resp = await client.get(url=kw_api)
        music_info = resp.json()["data"]

    song = set_name(music_info["musicname"])
    singer = set_name(music_info["singer"])

    try:
        music = music_info["musicurl"]
    except KeyError:
        return False

    async with AsyncClient(headers=headers, follow_redirects=True, timeout=None, proxies=proxies) as client:
        resp = await client.get(url=music)
        content = resp.content

    kind = guess(content)
    if kind is None:
        return False

    file_name = join(path, f"{song}-{singer}.{kind.extension}")
    with open(file_name, "wb") as f:
        f.write(content)

    return True, file_name, f"{song}-{singer}.{kind.extension}"


# 酷狗音乐
async def kg_get_music(name, proxies):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "sc": 50
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None, proxies=proxies) as client:
        resp = await client.get(url=kg_api)
        music_info = resp.json()["data"]

    choice_list = ""
    for i in range(len(music_info)):
        music_name = music_info[i]["name"]
        singers = music_info[i]["singer"]

        choose = f"{i+1}.{music_name}-{singers}\n"
        choice_list += choose

    return choice_list


async def kg_download(name, n, path, proxies):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "n": n,
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None, proxies=proxies) as client:
        resp = await client.get(url=kg_api)
        try:
            music_info = resp.json()["data"]
        except KeyError:
            return False

    song = set_name(music_info["song"])
    singer = set_name(music_info["singer"])
    try:
        music = music_info["url"]
    except KeyError:
        return False

    async with AsyncClient(headers=headers, follow_redirects=True, timeout=None, proxies=proxies) as client:
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
async def mg_get_music(name, proxies):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "sc": 50
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None, proxies=proxies) as client:
        resp = await client.get(url=mg_api)
        music_info = resp.json()["data"]

    choice_list = ""
    for i in range(len(music_info)):
        music_name = music_info[i]["song"]
        singers = music_info[i]["singer"]

        choose = f"{i+1}.{music_name}-{singers}\n"
        choice_list += choose

    return choice_list


async def mg_download(name, n, path, proxies):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "n": n,
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None, proxies=proxies) as client:
        resp = await client.get(url=mg_api)
        music_info = resp.json()["data"]

    song = set_name(music_info["musicname"])
    singer = set_name(music_info["singer"])
    try:
        music = music_info["musicurl"]
    except KeyError:
        return False

    async with AsyncClient(headers=headers, follow_redirects=True, timeout=None, proxies=proxies) as client:
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
async def vip_qq_get_music(name, proxies):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "limit": 50
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None, proxies=proxies) as client:
        resp = await client.get(url=qq_vip_api)
        music_info = resp.json()["data"]

    choice_list = ""
    for i in range(len(music_info)):
        music_name = music_info[i]["song"]
        singer_list = music_info[i]["singers"]
        singer_num = len(singer_list)
        singers = ""
        if singer_num > 1:
            for s in range(singer_num):
                s += 1
                if s == singer_num:
                    singers += f"{singer_list[s - 1]}"
                else:
                    singers += f"{singer_list[s - 1]}、"
        else:
            singers = singer_list[0]
        choose = f"{i+1}.{music_name}-{singers}\n"
        choice_list += choose

    return choice_list


async def vip_qq_download(name, n, br, path, proxies):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "n": n,
        "br": br
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None, proxies=proxies) as client:
        resp = await client.get(url=qq_vip_api)
        info = resp.json()
    try:
        music_info = info["data"]
    except KeyError:
        return False

    song = set_name(music_info["song"])
    singer = set_name(music_info["singer"])
    music = music_info["music"]

    if br > 2:
        async with AsyncClient(headers=headers, follow_redirects=True, timeout=None, proxies=proxies) as client:
            resp = await client.get(url=music)
            content = resp.content

        kind = guess(content)
        if kind is None:
            return False

        file_name = join(path, f"{song}-{singer}.{kind.extension}")
        with open(file_name, "wb") as f:
            f.write(content)

    else:
        client = AsyncClient(proxies=proxies)
        async with client.stream(method="GET", url=music, headers=headers, follow_redirects=True, timeout=None) as r:
            with open(fr"{path}/{song}-{singer}", "wb+") as f:
                async for data in r.aiter_bytes(chunk_size=64*1024):
                    f.write(data)
                kind = guess(f)

            file_name = f"{path}/{song}-{singer}.{kind.extension}"
            rename(f"{path}/{song}-{singer}", file_name)

    return True, file_name, f"{song}-{singer}.{kind.extension}"


# QQ音乐
async def qq_get_music(name, proxies):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "sc": 50
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None, proxies=proxies) as client:
        resp = await client.get(url=qq_api)
        music_info = resp.json()["data"]

    choice_list = ""
    for i in range(len(music_info)):
        music_name = music_info[i]["song"]
        singers = music_info[i]["singers"]

        choose = f"{i+1}.{music_name}-{singers}\n"
        choice_list += choose

    return choice_list


async def qq_download(name, n, path, proxies):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "n": n
    }
    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None, proxies=proxies) as client:
        resp = await client.get(url=qq_api)
        info = resp.json()
    try:
        music_info = info["data"]
    except KeyError:
        return False

    song = set_name(music_info["Music"])
    singer = set_name(music_info["Singer"])
    music = music_info["Url"]

    async with AsyncClient(headers=headers, follow_redirects=True, timeout=None, proxies=proxies) as client:
        resp = await client.get(url=music)
        content = resp.content

    kind = guess(content)
    if kind is None:
        return False

    file_name = join(path, f"{song}-{singer}.{kind.extension}")
    with open(file_name, "wb") as f:
        f.write(content)

    return True, file_name, f"{song}-{singer}.{kind.extension}"


# 网易云音乐
async def wy_get_music(name, proxies):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "sc": 50
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None, proxies=proxies) as client:
        resp = await client.get(url=wy_api)
        music_info = resp.json()["data"]

    choice_list = ""
    for i in music_info:
        music_name = i["song"]
        singer_list = i["singers"]
        singer_num = len(singer_list)
        singers = ""
        if singer_num > 1:
            for s in range(singer_num):
                s += 1
                if s == singer_num:
                    singers += f"{singer_list[s - 1]}"
                else:
                    singers += f"{singer_list[s - 1]}、"
        else:
            singers = singer_list[0]
        choose = f"{i+1}{music_name}-{singers}\n"
        choice_list += choose

    return choice_list


async def wy_download(name, n, path, proxies):
    headers = {
        "User-Agent": get_user_agent()
    }

    data = {
        "msg": name,
        "n": n,
    }

    async with AsyncClient(headers=headers, params=data, follow_redirects=True, timeout=None, proxies=proxies) as client:
        resp = await client.get(url=wy_api)
        music_info = resp.json()["data"]

    song = set_name(music_info["Music"])
    singer = set_name(music_info["Singer"])
    try:
        music = music_info["dataUrl"]
    except KeyError:
        return False

    async with AsyncClient(headers=headers, follow_redirects=True, timeout=None, proxies=proxies) as client:
        resp = await client.get(url=music)
        content = resp.content

    kind = guess(content)
    if kind is None:
        return False

    file_name = join(path, f"{song}-{singer}.{kind.extension}")
    with open(file_name, "wb") as f:
        f.write(content)

    return True, file_name, f"{song}-{singer}.{kind.extension}"
