#!usr/bin/env python3
# -*- coding: utf-8 -*-
from nonebot.adapters.onebot.v11 import GROUP, PRIVATE_FRIEND, Bot, Message
from nonebot.log import logger
from nonebot import on_regex, on_command
from nonebot.exception import ActionFailed
from nonebot.params import RegexDict, Arg, T_State, CommandArg

from colorama import init, Fore
from os import remove
from .config import path, if_del, song_num
from .work import *

__version__ = "0.1.7"

pattern = "^(?P<source>qq|QQ|qqvip|QQVIP|酷狗|kg|咪咕|mg|网易云|网易|wy)点歌( (?P<br>.*?)音质)? (?P<name>.*)"
music_matcher = on_regex(pattern, priority=5, permission=GROUP | PRIVATE_FRIEND, block=True)
impt_songlist = on_command(cmd="导入歌单", priority=5, permission=GROUP | PRIVATE_FRIEND, block=True)

# 字体样式初始化（自动重设字体样式）
init(autoreset=True)

logger.success(Fore.LIGHTGREEN_EX + f"成功导入本插件，插件版本为{__version__}")


@music_matcher.handle()
async def _(state: T_State, regex: dict = RegexDict()):
    # 保存音乐信息
    source = regex["source"]
    name = regex["name"]
    br = regex["br"]
    if br == "标准":
        br = 4
    elif br == "HQ":
        br = 3
    elif br == "无损":
        br = 2
    elif br == "母带":
        br = 1
    else:
        br = 3

    music_info, songids = await get_music(source=source, name=name)

    state.update(
        {
            "music_source": source,
            "music_name": name,
            "songids": songids,
            "br": br
        }
    )
    
    await music_matcher.send(music_info, at_sender=True)


@music_matcher.got(key="n")
async def _(bot: Bot, event: Event, state: T_State, n: Message = Arg("n")):
    n = str(n)
    try:
        n = int(n)
    except ValueError:
        await music_matcher.finish("已取消点歌", at_sender=True)

    # 获取音乐信息
    songid = state["songids"]
    if songid is not None:
        songid = songid[n-1]
    name = state["music_name"]
    source = state["music_source"]
    br = state["br"]

    # 获取会话信息
    id_ = get_id(event)

    await music_matcher.send("正在努力下载，请稍后......", at_sender=True)
    logger.info(Fore.LIGHTCYAN_EX + f"开始下载'{name}'，音源：{source}，序号：{n}，音质：{br}")
    info = await get_music(source=source, name=name, songid=songid, br=br, path=path, n=n)

    if info is False:
        logger.error(Fore.LIGHTRED_EX + f"'{name}'获取失败")
        await music_matcher.finish(f"'{name}'获取失败", at_sender=True)
    else:
        logger.success(Fore.LIGHTGREEN_EX + f"'{name}'下载成功")
        file = info[1]
        name = info[2]

        # 上传音乐
        try:
            if id_[0] == "group":
                await bot.upload_group_file(group_id=id_[1], file=file, name=name)
            else:
                await bot.upload_private_file(user_id=id_[1], file=file, name=name)
        except ActionFailed:
            await music_matcher.finish("Bot可能被风控或群聊不支持上传文件，请稍后再试")
        finally:
            if if_del is True:
                try:
                    remove(file)
                except Exception as error:
                    logger.warning(Fore.LIGHTYELLOW_EX + f"文件'{file}'删除失败：{error}，可手动删除")


@impt_songlist.handle()
async def _(state: T_State, songlist_info: Message = CommandArg()):
    songlist_info = str(songlist_info)
    data = await import_songlist(songlist_info)

    if data is False:
        await impt_songlist.finish("解析失败，请尝试使用歌单id", at_sender=True)
    info, song_list, songids = data

    song_info = "\n".join([f"{i + 1}{song['name']}-{song['singer'][0]['name']}" for i, song in enumerate(song_list)])

    try:
        await impt_songlist.send(f"导入成功\n{info}\n{song_info}", at_sender=True)
    except ActionFailed:
        await impt_songlist.send(f"发送失败，Bot可能被风控或歌单太长，尝试发送前{song_num}条")
        song_info = "\n".join([f"{i + 1}.{song_list[i]['name']}-{song_list[i]['singer'][0]['name']}" for i in range(song_num)])

        try:
            await impt_songlist.send(f"导入成功\n{info}\n{song_info}", at_sender=True)
        except ActionFailed:
            await impt_songlist.finish("发送失败，Bot可能被风控，请稍后再试")

    state["songids"] = songids


@impt_songlist.got(key="s")
async def _(bot: Bot, state: T_State, event: Event, s: Message = Arg("s")):
    s = str(s)
    try:
        s = int(s)
    except ValueError:
        await music_matcher.finish()

    songids = state["songids"]
    # 获取会话信息
    id_ = get_id(event)

    await music_matcher.send("正在努力下载，请稍后......", at_sender=True)
    info = await vip_qq_download(br=3, path=path, songid=songids[s-1])

    if info is False:
        await music_matcher.finish(f"获取失败", at_sender=True)
    else:
        file = info[1]
        name = info[2]
        # 上传音乐
        try:
            if id_[0] == "group":
                await bot.upload_group_file(group_id=id_[1], file=file, name=name)
            else:
                await bot.upload_private_file(user_id=id_[1], file=file, name=name)
        except ActionFailed:
            await music_matcher.finish("Bot可能被风控或群聊不支持上传文件，请稍后再试")
        finally:
            if if_del is True:
                try:
                    remove(file)
                except Exception as error:
                    logger.warning(Fore.LIGHTYELLOW_EX + f"文件'{file}'删除失败：{error}，可手动删除")
