from httpx import AsyncClient
from aiohttp import ClientSession
from fake_useragent import UserAgent
from re import findall

headers = {
    "User-Agent": UserAgent().random
}


def get_userid(event):
    """获取用户ID"""
    info = str(event.get_session_id())
    try:
        res = findall(r"group_(?P<group_id>\d+)_(?P<member_id>\d+)", info)[0]
    except IndexError:
        data = "private", info
    else:
        data = "group", res[0]

    return data


# 酷我音乐
async def kw_get_music(name, n=None, proxies=None):
    params = {
        "msg": name,
    }

    if n is not None:
        params.update(
            {
                "n": n
            }
        )

    async with AsyncClient(headers=headers, params=params, proxies=proxies) as client:
        try:
            resp = await client.get(url="http://ovooa.com/API/kwdg/api.php")
            music_info = resp.json()["data"]
        except Exception as error:
            return False, error

    if n is not None:
        url = music_info["musicurl"]
        music_name = music_info["musicname"]
        return True, url, music_name

    else:
        music_list = "请选择："
        num = 0
        for i in music_info:
            num += 1
            music_name = i["song"]
            singers = i["singer"]

            music_list += f"\n{num}.{music_name}-{singers}"

        return True, music_list


# QQ音乐
async def qq_get_music(name, n=None, proxies=None):
    if proxies is None:
        proxy = None
    else:
        proxy = proxies["http//"]

    params = {
        "msg": name,
    }
    if n is not None:
        params.update(
            {
                "n": n
            }
        )

    async with ClientSession(headers=headers) as client:
        try:
            async with client.get(url="http://ovooa.com/API/QQ_Music", params=params, proxy=proxy) as resp:
                music_info = (await resp.json())["data"]
        except Exception as error:
            return False, error

    if n is not None:
        url = music_info["music"]
        music_name = music_info["song"]
        return True, url, music_name

    else:
        music_list = "请选择："
        num = 0
        for i in music_info:
            num += 1
            music_name = i["song"]
            singers = i["singers"]

            music_list += f"\n{num}.{music_name}-{singers}"

        return True, music_list


# 酷狗音乐
async def kg_get_music(name, n=None, proxies=None):
    params = {
        "msg": name,
    }

    if n is not None:
        params.update(
            {
                "n": n
            }
        )

    async with AsyncClient(headers=headers, params=params, proxies=proxies) as client:
        try:
            resp = await client.get(url="http://ovooa.com/API/kgdg/api.php")
            music_info = resp.json()["data"]
        except Exception as error:
            return False, error

    if n is not None:
        url = music_info["url"]
        music_name = music_info["song"]
        return True, url, music_name

    else:
        music_list = "请选择："
        num = 0
        for i in music_info:
            num += 1
            music_name = i["name"]
            singers = i["singer"]

            music_list += f"\n{num}.{music_name}-{singers}"

        return True, music_list


# 咪咕音乐
async def mg_get_music(name, n=None, proxies=None):
    params = {
        "msg": name,
    }

    if n is not None:
        params.update(
            {
                "n": n
            }
        )

    async with AsyncClient(headers=headers, params=params, proxies=proxies) as client:
        try:
            resp = await client.get(url="http://ovooa.com/API/migu/api.php")
            music_info = resp.json()["data"]
        except Exception as error:
            return False, error

    if n is not None:
        url = music_info["musicurl"]
        music_name = music_info["musicname"]
        return True, url, music_name

    else:
        music_list = "请选择："
        num = 0
        for i in music_info:
            num += 1
            music_name = i["song"]
            singers = i["singer"]

            music_list += f"\n{num}.{music_name}-{singers}"

        return True, music_list


# 网易云音乐
async def wy_get_music(name, n=None, proxies=None):
    params = {
        "msg": name,
    }

    if n is not None:
        params.update(
            {
                "n": n
            }
        )

    async with AsyncClient(headers=headers, params=params, proxies=proxies) as client:
        try:
            resp = await client.get(url="http://ovooa.com/API/wydg/api.php")
            music_info = resp.json()["data"]
        except Exception as error:
            return False, error

    if n is not None:
        url = music_info["dataUrl"]
        music_name = music_info["Music"]
        return True, url, music_name

    else:
        music_list = "请选择："
        num = 0
        for i in music_info:
            num += 1
            music_name = i["song"]
            singers = i["singers"]

            music_list += f"\n{num}.{music_name}-{singers}"

        return True, music_list


async def get_music(source, name, mode, n=None, proxies=None):
    if source == "酷我" or "kw":
        if mode == "list":
            return await kw_get_music(name=name, proxies=proxies)
        else:
            return await kw_get_music(name=name, n=n, proxies=proxies)

    elif source == "qq" or "QQ":
        if mode == "list":
            return await qq_get_music(name=name, proxies=proxies)
        else:
            return await qq_get_music(name=name, n=n, proxies=proxies)

    elif source == "酷狗" or "kg":
        if mode == "list":
            return await kg_get_music(name=name, proxies=proxies)
        else:
            return await kg_get_music(name=name, n=n, proxies=proxies)

    elif source == "网易云" or "网易" or "wy":
        if mode == "list":
            return await wy_get_music(name=name, proxies=proxies)
        else:
            return await wy_get_music(name=name, n=n, proxies=proxies)

    elif source == "咪咕" or "mg":
        if mode == "list":
            return await mg_get_music(name=name, proxies=proxies)
        else:
            return await mg_get_music(name=name, n=n, proxies=proxies)
