#!usr/bin/env python3
# -*- coding: utf-8 -*-
from nonebot.adapters.onebot.v11 import GROUP, PRIVATE_FRIEND, Event, Bot, Message
from nonebot.log import logger
from nonebot.permission import SUPERUSER
from nonebot import on_regex, get_driver
from nonebot.params import RegexDict, Arg, T_State, RegexGroup

from fake_useragent import UserAgent
from colorama import init, Fore
from os import remove
from .work import get_music, get_userid

__version__ = "0.1.0"

pattern = r"^(?P<source>qq|QQ|酷狗|kg|酷我|kw|咪咕|mg|网易云|网易|wy)点歌 (?P<name>.*)"
music_matcher = on_regex(pattern, priority=5, permission=GROUP | PRIVATE_FRIEND, block=True)
set_mport = on_regex(pattern=r'set_mport:(?P<port>.*)', permission=SUPERUSER, priority=5, block=True)

# 字体样式初始化（自动重设字体样式）
init(autoreset=True)

# 获取全局配置
try:
    port = get_driver().config.music_port
    proxies = {
        "http://": f"http://127.0.0.1:{port}",
        "https://": f"http://127.0.0.1:{port}"
    }
except AttributeError:
    try:
        # 尝试导入我另一个插件的配置
        port = get_driver().config.novelai_proxy_port
    except AttributeError:
        proxies = None
    else:
        proxies = {
            "http://": f"http://127.0.0.1:{port}",
            "https://": f"http://127.0.0.1:{port}"
        }

logger.success(Fore.LIGHTGREEN_EX + f"成功导入本插件，插件版本为{__version__}")


# 设置本地端口
@set_mport.handle()
async def _(regex: tuple = RegexGroup()):
    global port, proxies
    pt = regex[0]

    # 判断是否为数字
    try:
        int(pt)
    except ValueError:
        # 取消代理模式
        if pt == "None":
            port = pt
            proxies = None
            logger.success(Fore.LIGHTCYAN_EX + "成功取消代理模式")
            await set_mport.finish("成功取消代理模式")
        else:
            await set_mport.finish("请输入有效参数！")
    else:
        port = pt
        proxies = {
            "http://": f"http://127.0.0.1:{port}",
            "https://": f"http://127.0.0.1:{port}"
        }
        logger.success(Fore.LIGHTCYAN_EX + f"当前本地代理端口：{port}")

        await set_mport.finish("本地代理端口设置成功，设置将在下一次请求时启用")


@music_matcher.handle()
async def _(state: T_State, regex: dict = RegexDict()):
    source = regex["source"]
    name = regex["name"]
    state["music_source"] = source
    state["music_name"] = name

    music_info = await get_music(source=source, name=name, mode="list", proxies=proxies)
    if music_info[0] is False:
        logger.error(f"'{name}'获取失败：{music_info[1]}")
        await music_matcher.finish(f"'{name}'获取失败")

    await music_matcher.send(music_info[1])


@music_matcher.got(key="n")
async def _(bot: Bot, event: Event, state: T_State, n: Message = Arg("n")):
    name = state["music_name"]
    source = state["music_source"]
    data = get_userid(event)

    info = await get_music(source=source, name=name, n=int(str(n)), mode="download", proxies=proxies)

    if info[0] is False:
        logger.error(f"'{name}'获取失败：{info[1]}")
        await music_matcher.finish(f"'{name}'获取失败")

    name = info[2]

    # 下载音乐
    music_headers = [f"User-Agent={UserAgent().random}"]
    logger.info(Fore.LIGHTCYAN_EX + f"开始下载'{name}'")
    try:
        file = (await bot.download_file(url=info[1], headers=music_headers, thread_count=30))["file"]
    except Exception as error:
        logger.error(f"'{name}'获取失败：{error}")
        await music_matcher.finish(f"'{name}'获取失败")
    else:
        logger.success(Fore.LIGHTGREEN_EX + f"'{name}'下载成功")
        # 上传音乐
        if data[0] == "group":
            await bot.upload_group_file(group_id=data[1], file=file, name=f"{name}.mp3")
        else:
            await bot.upload_private_file(user_id=data[1], file=file, name=f"{name}.mp3")
        try:
            # 删除缓存文件
            remove(file)
        except Exception as error:
            logger.warning(Fore.LIGHTYELLOW_EX + f"缓存文件删除失败：{error}，可手动删除")