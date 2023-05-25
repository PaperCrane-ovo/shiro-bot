'''天气功能'''
from pathlib import Path
import gzip
import io
from typing import Annotated,List,Dict
from datetime import date, timedelta
import aiohttp
from graia.saya import Saya, Channel
from graia.ariadne.entry import Ariadne, ListenerSchema, Plain, Group, GroupMessage, Member, Source, Image, MessageChain,DetectPrefix
from graia.scheduler import GraiaScheduler, timers
from graia.scheduler.saya import SchedulerSchema
import json5

channel = Channel.current()

class Weather:
    '''一个天气类,用于获取天气信息'''
    def __init__(self,key_file = 'keys.txt'):
        with open(Path(__file__).parent / key_file, 'r', encoding='utf-8') as file:
            self.key = file.read()
        self.api_3d = 'https://devapi.qweather.com/v7/weather/3d'
        self.api_geo = "https://geoapi.qweather.com/v2/city/lookup"
        self.api_now = "https://devapi.qweather.com/v7/weather/now"
    
    async def get_location_id(self,city: str):
        '''
        获取城市ID
        
        Parameters
        ----------
        city : str
            城市名

        Returns
        -------
        str|None
            城市ID
        '''
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.api_geo}?location={city}&key={self.key}&range=cn') as response:
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
        if data['code'] == '200':
            return data['location'][0]['id']
        return None
    async def get_weather_by_location_id(self,location_id: str):
        '''
        通过location_id获取天气信息

        Parameters
        ----------
        location_id : str
            城市ID

        Returns
        -------
        list:dict|None
            最近3天的天气信息
        '''
        if location_id is None:
            return None
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.api_3d}?location={location_id}&key={self.key}') as response:
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
        if data['code'] == '200':
            return data['daily']
        return None

    @channel.use(ListenerSchema(listening_events=[GroupMessage]))
    async def weather(
        self,
        bot:Ariadne,
        group:Group,
        member:Member,
        source:Source,
        message:Annotated[MessageChain,DetectPrefix('天气')]
    ):
        '''
        根据前缀天气查询并发送天气信息
        '''

    async def parse_weather(self,data:List[dict]):
        '''
        根据返回的数据分析天气信息

        Parameters
        ----------
        data : list:dict
            天气信息

        Returns
        -------
        str
            天气信息
        '''
        