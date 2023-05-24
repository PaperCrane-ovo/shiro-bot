'''天气功能'''
from pathlib import Path
import gzip
import io
from datetime import date, timedelta
import aiohttp
from graia.saya import Saya, Channel
from graia.ariadne.entry import Ariadne, ListenerSchema, Plain, Group, GroupMessage, Member, Source, Image, MessageChain,DetectPrefix
from graia.scheduler import GraiaScheduler, timers
from graia.scheduler.saya import SchedulerSchema
import json5

channel = Channel.current()
with open(Path(__file__).parent / 'keys.txt', 'r', encoding='utf-8') as file:
    key = file.read()


async def get_location_id(city: str):
    '''获取城市ID'''
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://geoapi.qweather.com/v2/city/lookup?location={city}&key={key}') as response:
            if response.headers.get('Content-Encoding') == 'gzip':
                gzip_data = await response.read()
                gzip_buffer = io.BytesIO(gzip_data)
                gzip_file = gzip.GzipFile(fileobj=gzip_buffer)
                data = gzip_file.read()
                # 处理解压后的数据
                data = json5.loads(data)
            else:
                # 处理未经压缩的数据
                data = await response.text()
                data = json5.loads(data)
            