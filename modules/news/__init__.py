'''早报功能'''
from pathlib import Path
from datetime import date,timedelta
import aiohttp
from graia.saya import Saya, Channel
from graia.ariadne.entry import Ariadne, ListenerSchema, Plain, Group, GroupMessage, Member, Source,Image,MessageChain
from graia.scheduler import GraiaScheduler,timers
from graia.scheduler.saya import SchedulerSchema
import json5

channel = Channel.current()

with open(Path('./config.json'), 'r', encoding='utf-8') as f:
    config = json5.load(f)



async def get_news():
    '''通过api获取早报'''
    today = date.today().isoformat()
    if Path(f'./image/{today}.jpg').exists():
        return Image(path = Path(f'./image/{today}.jpg'))


    async with aiohttp.ClientSession() as session:
        async with session.get(config['api']) as resp:
            response = await resp.json()
        if response['code'] == 200 and response['msg'] == 'Success':
            image_addr = response['imageUrl']
            news_time = response['datatime']

            if news_time != today:
                return Image(path=Path(f'./image/{(date.today()-timedelta(days=1)).isoformat()}')),'早报还没出来呢，先看看昨天的吧'

            image = await session.get(image_addr)
            image = await image.read()
            with open(Path(f'./image/{today}'), 'wb') as f:
                f.write(image)
            return Image(data_bytes=image)
        else:
            return '出错啦,稍后再试试吧'


@channel.use(ListenerSchema(listening_events=[GroupMessage],decorators=[Plain('今日早报')]))
async def handle_news(bot: Ariadne, group: Group, member: Member, source: Source):
    '''
    通过群消息请求早报
    '''
    if group.id not in config['groups']:
        await bot.send_group_message(group,MessageChain(['早报功能只在指定群开放哦']),quote=source)
        return
    result = await get_news()
    await bot.send_group_message(group,MessageChain(list(result)),quote=source)
    return

@channel.use(SchedulerSchema(timers.crontabify('* 7 * * * *')))
async def auto_send_news(bot: Ariadne):
    '''
    定时发送早报
    '''
    result = await get_news()
    if isinstance(result,Image):
        for group in config['groups']:
            await bot.send_group_message(group,MessageChain(['早上好~今天的早报来啦~']))
            await bot.send_group_message(group,MessageChain([result]))