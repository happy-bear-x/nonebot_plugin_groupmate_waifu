from nonebot import require, logger
from nonebot.permission import SUPERUSER
from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11 import (
    GROUP,
    Bot,
    GroupMessageEvent,
    Message,
    MessageSegment,
)

import nonebot
import os
import random
import asyncio
import time

from pathlib import Path

try:
    import ujson as json
except ModuleNotFoundError:
    import json

from .utils import *
from .config import Config

# 加载全局配置
global_config = nonebot.get_driver().config
waifu_config = Config.parse_obj(global_config.dict())

waifu_cd_bye = waifu_config.waifu_cd_bye

waifu_save = waifu_config.waifu_save

waifu_reset = waifu_config.waifu_reset

HE = waifu_config.waifu_he
BE = HE + waifu_config.waifu_be
NTR = waifu_config.waifu_ntr

yinpa_HE = waifu_config.yinpa_he
yinpa_BE = yinpa_HE + waifu_config.yinpa_be
yinpa_CP = waifu_config.yinpa_cp
yinpa_CP = yinpa_HE if yinpa_CP == 0 else yinpa_CP

waifu_file = Path() / "data" / "waifu"

if not waifu_file.exists():
    os.makedirs(waifu_file)

record_waifu_file = waifu_file / "record_waifu"
record_be_file = waifu_file / "record_be"
record_yinpa1_file = waifu_file / "record_yinpa1"
record_yinpa2_file = waifu_file / "record_yinpa2"

# 分手记录
record_be = {}
if record_be_file.exists():
    with open(record_be_file, 'r') as f:
        line = f.read()
        record_be = eval(line)

if waifu_save:
    def save(file, data):
        with open(file, "w", encoding="utf8") as f:
            f.write(str(data))
else:
    def save(file, data):
        pass

scheduler = require("nonebot_plugin_apscheduler").scheduler

if waifu_reset:

    # 判断文件时效
    timestr = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    timeArray = time.strptime(timestr, '%Y-%m-%d')
    Zero_today = time.mktime(timeArray)

    if record_waifu_file.exists() and os.path.getmtime(record_waifu_file) > Zero_today:
        with open(record_waifu_file, 'r') as f:
            line = f.read()
            record_waifu = eval(line)
    else:
        record_waifu = {}

    if record_yinpa1_file.exists() and os.path.getmtime(record_yinpa1_file) > Zero_today:
        with open(record_yinpa1_file, 'r') as f:
            line = f.read()
            record_yinpa1 = eval(line)
    else:
        record_yinpa1 = {}

    if record_yinpa2_file.exists() and os.path.getmtime(record_yinpa2_file) > Zero_today:
        with open(record_yinpa2_file, 'r') as f:
            line = f.read()
            record_yinpa2 = eval(line)
    else:
        record_yinpa2 = {}


    # 重置记录

    @scheduler.scheduled_job("cron", hour=0)
    def _():
        global record_waifu, record_yinpa1, record_yinpa2
        record_waifu = {}
        record_yinpa1 = {}
        record_yinpa2 = {}
else:

    if record_waifu_file.exists():
        with open(record_waifu_file, 'r') as f:
            line = f.read()
            record_waifu = eval(line)
    else:
        record_waifu = {}

    if record_yinpa1_file.exists():
        with open(record_yinpa1_file, 'r') as f:
            line = f.read()
            record_yinpa1 = eval(line)
    else:
        record_yinpa1 = {}

    if record_yinpa2_file.exists():
        with open(record_yinpa2_file, 'r') as f:
            line = f.read()
            record_yinpa2 = eval(line)
    else:
        record_yinpa2 = {}


    # 重置记录
    @scheduler.scheduled_job("cron", hour=0)
    def _():
        global record_yinpa1, record_yinpa2
        record_yinpa1 = {}
        record_yinpa2 = {}

# 娶群友

waifu = on_command("娶群友", aliases={'娶老婆', '找对象'}, permission=GROUP, priority=90, block=True)

no_waifu = [
    "你没有娶到群友，强者注定孤独，加油！",
    "找不到对象.jpg",
    "恭喜你没有娶到老婆~",
    "さんが群友で結婚するであろうヒロインは、\n『自分の左手』です！"
]
happy_end = [
    "好耶~",
    "需要咱主持婚礼吗qwq",
    "不许秀恩爱！",
    "(响起婚礼进行曲♪)",
    "祝你们生八个。"
]


@waifu.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id
    user_id = event.user_id
    global record_waifu_file, record_waifu
    record_waifu.setdefault(group_id, {})
    at = get_message_at(event.json())
    if at and at[0] != user_id:
        at = at[0]
        if record_waifu[group_id].get(user_id, 0) == 0:
            if record_waifu[group_id].get(at, 0) in (0, at):
                X = random.randint(1, 100)
                if 0 < X <= HE:
                    record_waifu[group_id].update(
                        {
                            user_id: at,
                            at: user_id
                        }
                    )
                    await waifu.send("恭喜你娶到了群友" + MessageSegment.at(at), at_sender=True)
                    await asyncio.sleep(1)
                elif HE < X <= BE:
                    pass  # record_waifu[group_id][user_id] = user_id
                else:
                    pass
            else:
                try:
                    member = await bot.get_group_member_info(group_id=group_id, user_id=record_waifu[group_id][at])
                except:
                    member = None
                if random.randint(1, 100) <= NTR:  # 彩蛋
                    record_waifu[group_id].pop(record_waifu[group_id][at])
                    record_waifu[group_id].update(
                        {
                            user_id: at,
                            at: user_id
                        }
                    )
                    await waifu.send(
                        "人家已经名花有主了~" +
                        MessageSegment.image(file=await user_img(record_waifu[group_id][at])) +
                        "ta的CP：" + (member['card'] or member['nickname']) + '\n'
                                                                            "但是...",
                        at_sender=True
                    )
                else:
                    await waifu.send(
                        "人家已经名花有主啦！" +
                        MessageSegment.image(file=await user_img(record_waifu[group_id][at])) +
                        "ta的CP：" + (member['card'] or member['nickname']),
                        at_sender=True
                    )
                await asyncio.sleep(1)
        elif record_waifu[group_id][user_id] == at:
            await waifu.finish(
                "这是你的CP！" + MessageSegment.at(record_waifu[group_id][user_id]) + '\n' +
                random.choice(happy_end) +
                MessageSegment.image(file=await user_img(record_waifu[group_id][user_id])),
                at_sender=True
            )
        elif record_waifu[group_id][user_id] == user_id:
            pass
        else:
            try:
                member = await bot.get_group_member_info(group_id=group_id, user_id=record_waifu[group_id][user_id])
            except:
                member = None
            if member:
                await waifu.finish(
                    "你已经有CP了，不许花心哦~" +
                    MessageSegment.image(file=await user_img(record_waifu[group_id][user_id])) +
                    "你的CP：" + (member['card'] or member['nickname']),
                    at_sender=True
                )
            else:
                pass  # record_waifu[group_id][user_id] = user_id

    if record_waifu[group_id].get(user_id, 0) == 0:
        member_list = await bot.get_group_member_list(group_id=event.group_id)
        i = 0
        while i < len(member_list):
            if member_list[i]['user_id'] in record_waifu[group_id].keys():
                del member_list[i]
            else:
                i += 1
        else:
            if member_list:
                member_list.sort(key=lambda x: x["last_sent_time"], reverse=True)
                member = random.choice(member_list[:80])
                record_waifu[group_id].update(
                    {
                        user_id: member['user_id'],
                        member['user_id']: user_id
                    }
                )
                nickname = member['card'] or member['nickname']
                if record_waifu[group_id][user_id] == user_id:
                    msg = random.choice(no_waifu)
                else:
                    msg = (
                        "的群友結婚对象是、\n",
                        MessageSegment.image(file=await user_img(record_waifu[group_id][user_id])),
                        f"『{nickname}』！"
                    )
            else:
                record_waifu[group_id][user_id] = 1
                msg = "群友已经被娶光了、\n" + random.choice(no_waifu)
    else:
        if record_waifu[group_id][user_id] == event.user_id:
            msg = random.choice(no_waifu)
        elif record_waifu[group_id][user_id] == 1:
            msg = "群友已经被娶光了、\n" + random.choice(no_waifu)
        else:
            try:
                member = await bot.get_group_member_info(group_id=group_id, user_id=record_waifu[group_id][user_id])
            except:
                member = None
            if member:
                nickname = member['card'] or member['nickname']
                msg = (
                    "的群友結婚对象是、\n",
                    MessageSegment.image(file=await user_img(record_waifu[group_id][user_id])),
                    f"『{nickname}』！"
                )
            else:
                msg = random.choice(no_waifu)

    save(record_waifu_file, record_waifu)
    await waifu.finish(msg, at_sender=True)


# 分手

global cd_bye
cd_bye = {}

bye = on_command("离婚", aliases={"分手"}, permission=GROUP, priority=90, block=True)

bye_msg = [
    "行吧~",
    "行吧，没良心的家伙。",
    "好吧，无情的家伙。",
    "好吧，祝你幸福。",
    "好吧，如你所愿。",
    "嗯。",
    "好。"
]


@bye.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    global record_waifu_file, record_waifu, cd_bye
    user_id = event.user_id
    group_id = event.group_id
    record_waifu.setdefault(group_id, {})
    group_wife = record_waifu[group_id]
    if user_id not in group_wife.keys():
        await bye.finish("单身狗干啥呢？", at_sender=True)
        return
    wife = int(record_waifu[group_id][user_id])
    if user_id == wife:
        await bye.finish("恭喜从注孤生出列", at_sender=True)
        del record_waifu[group_id][user_id]
        save(record_waifu_file, record_waifu)
        return
    cd_bye.setdefault(group_id, {})
    flag = cd_bye[group_id].setdefault(user_id, [0, 0])
    Now = time.time()
    cd = flag[0] - Now
    if cd <= 0:
        cd_bye[group_id][user_id][0] = Now + waifu_cd_bye
        cd_bye[group_id][user_id][1] = 0
        del group_wife[user_id]
        del group_wife[wife]
        save(record_waifu_file, record_waifu)
        # 记录分手次数
        group_be = record_be.setdefault(group_id, {})
        group_be[user_id] = group_be.setdefault(user_id, 0) + 1
        save(record_be_file, record_be)
        msg_len = len(bye_msg)
        rand_idx = random.randint(0, msg_len)
        if rand_idx == msg_len:
            await bye.finish(Message(f'[CQ:poke,qq={event.user_id}]'))
        else:
            await bye.finish(bye_msg[rand_idx], at_sender=True)
    else:
        flag[1] += 1
        if flag[1] == 1:
            await bye.finish(f"你的cd还有{round(cd / 60, 1)}分钟。", at_sender=True)
        elif flag[1] <= 3:
            await bye.finish(f"你已经问过了哦~ 你的cd还有{round(cd / 60, 1)}分钟。", at_sender=True)
        elif flag[1] <= 10:
            t = random.randint(flag[1], 3 * flag[1])
            flag[0] += t * 60
            await bye.finish(f"还问！罚时！你的cd还有{round(cd / 60, 1)}+{t}分钟。", at_sender=True)
        else:
            if random.randint(1, 6) == 6:
                await bye.finish("哼！")


# 强制离婚
force_bye = on_command("强制离婚", aliases={"强制分手", "管理分手"}, permission=SUPERUSER, priority=90, block=True)


@force_bye.handle()
async def force_bye_hand(event: GroupMessageEvent):
    global record_waifu_file, record_waifu
    at = event.user_id
    at_arr = get_message_at(event.json())
    if len(at_arr) > 0:
        at = at_arr[0]
    A = at
    B = int(record_waifu[event.group_id][at])
    del record_waifu[event.group_id][A]
    if A != B:
        del record_waifu[event.group_id][B]
    else:
        await force_bye.send("帮助脱离注孤生")
    save(record_waifu_file, record_waifu)
    await force_bye.finish("离婚操作完成。")


# 清除cd
clear_cd = on_command("清除离婚cd", aliases={"清除分手cd"}, permission=SUPERUSER, priority=90, block=True)


@clear_cd.handle()
async def clear_cd_hand(event: GroupMessageEvent):
    global cd_bye
    cd_bye.setdefault(event.group_id, {})
    at_arr = get_message_at(event.json())
    at = event.user_id
    if len(at_arr) > 0:
        at = at_arr[0]
    flag = cd_bye[event.group_id].setdefault(at, [0, 0])
    flag[0] = time.time()
    flag[1] = 0
    await clear_cd.finish("清除分手cd完成")


# 查看娶群友卡池

waifu_list = on_command("查看群友卡池", aliases={"群友卡池"}, permission=GROUP, priority=90, block=True)


@waifu_list.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    member_list = await bot.get_group_member_list(group_id=event.group_id)
    i = 0
    while i < len(member_list):
        if member_list[i]['user_id'] in record_waifu.setdefault(event.group_id, {}).keys():
            del member_list[i]
        else:
            i += 1
    else:
        if member_list:
            member_list.sort(key=lambda x: x["last_sent_time"], reverse=True)
            msg = "卡池：\n——————————————\n"
            for member in member_list[:80]:
                nickname = member['card'] or member['nickname']
                msg += f"{nickname}\n"
            else:
                output = text_to_png(msg[:-1])
                await waifu_list.finish(MessageSegment.image(output))
        else:
            await waifu_list.finish("群友已经被娶光了。")


# 查看本群CP

cp_list = on_command("本群CP", aliases={"本群cp"}, permission=GROUP, priority=90, block=True)


@cp_list.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id
    global record_waifu
    record_waifu.setdefault(group_id, {})
    lst = record_waifu[group_id].keys()
    if lst:
        listA = []
        listB = []
        for A in lst:
            listA.append(A)
            B = record_waifu[group_id][A]
            if B not in listA and B != A:
                listB.append(B)

        msg = ""
        for user_id in listB:
            try:
                member = await bot.get_group_member_info(group_id=group_id, user_id=record_waifu[group_id][user_id])
                niknameA = member['card'] or member['nickname']
            except:
                niknameA = ""
            try:
                member = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
                niknameB = member['card'] or member['nickname']
            except:
                niknameB = ""
            msg += f"♥ {niknameA} | {niknameB}\n"
        if msg:
            output = text_to_png("本群CP：\n——————————————\n" + msg[:-1])
            await cp_list.finish(MessageSegment.image(output))

    await cp_list.finish("本群暂无cp哦~")


# 分手榜单（渣榜）

be_list = on_command("分手榜单", aliases={"离婚榜单"}, permission=GROUP, priority=90, block=True)


@be_list.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id
    record_be.setdefault(group_id, {})
    group_dict = record_be[group_id]
    if group_dict:
        sorted_dict_list = sorted(group_dict.items(), key=lambda item: item[1], reverse=True)
        msg = ""
        for idx in range(len(sorted_dict_list)):
            # user_cnt : [qq , count]
            user_cnt = sorted_dict_list[idx]
            try:
                member = await bot.get_group_member_info(group_id=group_id, user_id=user_cnt[0])
                nickname = member['card'] or member['nickname']
            except:
                nickname = ""
            msg += f"NO·{idx+1}：{nickname}\n"
        if msg:
            output = text_to_png("分手榜单：\n——————————————\n" + msg[:-1])
            await be_list.finish(MessageSegment.image(output))

    await be_list.finish("本群暂无分手记录~")


# 透群友

yinpa = on_command("透群友", permission=GROUP, priority=90, block=True)


@yinpa.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id
    user_id = event.user_id
    global record_yinpa1, record_yinpa2
    at = get_message_at(event.json())
    msg = ""
    if at:
        if at[0] == user_id:
            pass
        elif at[0] == record_waifu[group_id].get(user_id, 0):
            X = random.randint(1, 100)
            if 0 < X <= yinpa_CP:
                member = await bot.get_group_member_info(group_id=group_id, user_id=at[0])
                nickname = member['card'] or member['nickname']
                record_yinpa1.setdefault(user_id, 0)
                record_yinpa1[user_id] += 1
                record_yinpa2.setdefault(member['user_id'], 0)
                record_yinpa2[member['user_id']] += 1
                msg = (
                    f"恭喜你涩到了你的老婆\n",
                    MessageSegment.image(file=await user_img(member["user_id"])),
                    f"『{nickname}』！"
                )
            else:
                msg = "你的老婆拒绝和你涩涩！"
        else:
            X = random.randint(1, 100)
            if 0 < X <= yinpa_HE:
                member = await bot.get_group_member_info(group_id=group_id, user_id=at[0])
                nickname = member['card'] or member['nickname']
                record_yinpa1.setdefault(user_id, 0)
                record_yinpa1[user_id] += 1
                record_yinpa2.setdefault(member['user_id'], 0)
                record_yinpa2[member['user_id']] += 1
                msg = (
                    f"恭喜你涩到了群友\n",
                    MessageSegment.image(file=await user_img(member["user_id"])),
                    f"『{nickname}』！"
                )
            elif yinpa_HE < X < yinpa_BE:
                msg = "不可以涩涩！"
            else:
                pass
    if not msg:
        member_list = await bot.get_group_member_list(group_id=event.group_id)
        member_list.sort(key=lambda x: x["last_sent_time"], reverse=True)
        member = random.choice(member_list[:80])
        if member["user_id"] == event.user_id:
            msg = "不可以涩涩！"
        else:
            nickname = member['card'] or member['nickname']
            record_yinpa1.setdefault(user_id, 0)
            record_yinpa1[user_id] += 1
            record_yinpa2.setdefault(member['user_id'], 0)
            record_yinpa2[member['user_id']] += 1
            msg = (
                "的涩涩对象是、\n",
                MessageSegment.image(file=await user_img(member["user_id"])),
                f"『{nickname}』！"
            )

    save(record_yinpa1_file, record_yinpa1)
    save(record_yinpa2_file, record_yinpa2)
    await yinpa.finish(msg, at_sender=True)


# 查看涩涩记录

yinpa_list = on_command("涩涩记录", aliases={"色色记录"}, permission=GROUP, priority=90, block=True)


@yinpa_list.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    global record_yinpa1, record_yinpa2

    msg_list = []

    # 输出卡池
    member_list = await bot.get_group_member_list(group_id=event.group_id)
    member_list.sort(key=lambda x: x["last_sent_time"], reverse=True)

    msg = "卡池：\n——————————————\n"
    for member in member_list[:80]:
        nickname = member['card'] or member['nickname']
        msg += f"{nickname}\n"

    output = text_to_png(msg[:-1])
    msg_list.append(
        {
            "type": "node",
            "data": {
                "name": "卡池",
                "uin": event.self_id,
                "content": MessageSegment.image(output)
            }
        }
    )

    # 输出透群友记录

    record = []
    for member in member_list:
        nickname = member['card'] or member['nickname']
        times = record_yinpa1.get(member['user_id'], 0)
        if times:
            record.append([nickname, times])

    record.sort(key=lambda x: x[1], reverse=True)

    msg = "涩涩记录①：\n——————————————\n"
    for info in record:
        msg += f"[align=left]{info[0]}[/align][align=right]今日透群友 {info[1]} 次[/align]\n"
    else:
        if msg:
            output = bbcode_to_png(msg[:-1])
            msg_list.append(
                {
                    "type": "node",
                    "data": {
                        "name": "记录①",
                        "uin": event.self_id,
                        "content": MessageSegment.image(output)
                    }
                }
            )
        else:
            pass

    # 输出被透记录

    record = []
    for member in member_list:
        nickname = member['card'] or member['nickname']
        times = record_yinpa2.get(member['user_id'], 0)
        if times:
            record.append([nickname, times])

    record.sort(key=lambda x: x[1], reverse=True)

    msg = "涩涩记录②：\n——————————————\n"
    for info in record:
        msg += f"[align=left]{info[0]}[/align][align=right]今日被透 {info[1]} 次[/align]\n"
    else:
        if msg:
            output = bbcode_to_png(msg[:-1])
            msg_list.append(
                {
                    "type": "node",
                    "data": {
                        "name": "记录②",
                        "uin": event.self_id,
                        "content": MessageSegment.image(output)
                    }
                }
            )
        else:
            pass
    await bot.send_group_forward_msg(group_id=event.group_id, messages=msg_list)
    await yinpa_list.finish()
