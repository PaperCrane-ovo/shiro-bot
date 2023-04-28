'''目前暂时用作更新曲目信息'''
import os
import json5
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.entry import DetectPrefix, Ariadne, FriendMessage, Friend
from .song import Song


channel = Channel.current()
admin = json5.load(open(os.path.dirname(__file__)+'/config/admins.json',
                   encoding='utf-8'))['superadmin']  # type: ignore


@channel.use(ListenerSchema(listening_events=[FriendMessage], decorators=[DetectPrefix('更新曲目')]))
async def update_song_list(bot: Ariadne, friend: Friend):
    '''接收超级管理员消息并从github更新曲目信息'''
    if friend.id not in admin:
        return

    with open(os.path.join(os.path.dirname(__file__), 'data', 'Modified_Gameinfo.json'), encoding='utf-8') as file:
        data = json5.load(file)
    await bot.send_friend_message(friend, '正在更新曲目信息')
    new_song_num = len(data['allSongs'])
    if new_song_num == len(Song.instances_list):
        await bot.send_friend_message(friend, '曲目信息已是最新')
        return
    song_number = len(Song.instances_list)
    for song in Song.instances_list:
        if song.song_id in data['allSongs']:
            data['allSongs'].remove(song.song_id)
    for song_id in data['allSongs']:
        new_song = data['regularSongs'][song_id]
        chart_detail = new_song['chartDetail']

        level_list = chart_detail['level_list']
        difficulty_list = []
        charter_list = []

        for level in chart_detail['level_list']:
            difficulty_list.append(chart_detail[level]['rating'])
            charter_list.append(chart_detail[level]['charter'])

        if len(level_list) == 3:
            level_list.append('AT')
            difficulty_list.append(0.0)
            charter_list.append('')

        Song(song_number, song_id, new_song['songsName'],
             difficulty_list, level_list, new_song['composer'], new_song['illustrator'], charter_list, [])
        song_number += 1
    Song.dump2json(os.path.join(
        os.path.dirname(__file__), 'data', 'song.json'))
    await bot.send_friend_message(friend, '更新成功')
