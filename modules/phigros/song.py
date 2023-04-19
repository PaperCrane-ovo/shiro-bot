'''phigros 歌曲类'''
import json5
import os


class Song:
    '''歌曲类,包含歌曲的所有信息以及难度谱师等等.'''

    song_info: list[dict]
    instances: dict = {}
    instances_list: list = []
    song_list: list[str]

    @classmethod
    def read_songs_from_file(cls, file_path: str):
        '''从文件中读取歌曲信息'''
        with open(file_path, 'r', encoding='utf-8') as f:
            cls.song_info = json5.load(f)['songs']  # type: ignore
        cls.song_list = [
            f"{song['song_number']}.{song['song_name']} ({song['composer']})" for song in cls.song_info]

    @classmethod
    def handle_songs(cls):
        '''处理歌曲信息'''
        for song in cls.song_info:
            cls(song['song_number'], song['song_id'], song['song_name'], song['difficulty'],
                song['level'], song['composer'], song['illustrator'], song['charter'], song['alias'])

    def __init__(self,
                 song_number,
                 song_id,
                 song_name,
                 difficulty,
                 level,
                 composer,
                 illustrator,
                 charter,
                 alias: list[str]):
        '''初始化歌曲类'''
        self.song_number = song_number
        self.song_id = song_id
        self.song_name = song_name
        self.difficulty = difficulty
        self.level = level
        self.composer = composer
        self.illustrator = illustrator
        self.charter = charter
        self.alias = alias
        self.img_path = f'{str(song_number)+"_"+song_name.replace(" ", "")}.png'
        Song.instances[song_id] = self
        Song.instances_list.append(self)

    def __str__(self):
        '''返回歌曲信息'''
        song_str = f'''{self.song_number}.{self.song_name}:曲师:{self.composer},插画:{self.illustrator}\n'''
        for i in range(3):
            song_str += f'''{self.level[i]}:{self.difficulty[i]},charter:{self.charter[i]}\n'''
        if self.difficulty[3] != 0.0:
            song_str += f'''{self.level[3]}:{self.difficulty[3]},charter:{self.charter[3]}\n'''
        return song_str

    @property
    def song_intro(self):
        '''返回歌曲简介'''
        return f'{self.song_number}.{self.song_name}({self.composer})'

    @property
    def song_inform(self):
        '''返回歌曲信息'''
        song_str = f'''{self.song_number}.{self.song_name}:曲师:{self.composer},插画:{self.illustrator}\n'''
        for i in range(3):
            song_str += f'''{self.level[i]}:{self.difficulty[i]},charter:{self.charter[i]}\n'''
        if self.difficulty[3] != 0.0:
            song_str += f'''{self.level[3]}:{self.difficulty[3]},charter:{self.charter[3]}\n'''
        return song_str

    @classmethod
    def dump2json(cls, file_path):
        '''将所有实例转换为json'''
        song_dict = {'songs': []}
        for _, song in cls.instances.items():
            song_dict['songs'].append(song.__dict__)
        with open(file_path, 'w', encoding='utf-8') as f:
            json5.dump(song_dict, f, indent=4, ensure_ascii=False)

    @classmethod
    def search_song_by_alias(cls, name: str):
        '''通过别名和本名搜索歌曲'''
        name = name.lower().replace(' ', '')

        for _, song in cls.instances.items():
            if name in song.alias:
                return song

        result = []

        for _, song in cls.instances.items():
            if name in song.song_id.split('.')[0].lower():
                result.append(song)
        if len(result) == 1:
            return result[0]
        elif len(result) > 1:
            return result
        else:
            # TODO: 模糊匹配
            return None

    @classmethod
    def search_song_by_number(cls, number: int):
        '''通过歌曲编号搜索歌曲'''

        return cls.instances_list[number-1]


if __name__ == '__main__':
    Song.read_songs_from_file(os.path.join(
        os.path.dirname(__file__), 'data', 'song.json'))
    Song.handle_songs()
    for _, song in Song.instances.items():
        song.alias = list({alias.lower() for alias in song.alias})

    Song.dump2json(os.path.join(
        os.path.dirname(__file__), 'data', 'song.json'))
