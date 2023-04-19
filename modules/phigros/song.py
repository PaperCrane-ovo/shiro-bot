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

    @classmethod
    def dump2json(cls, file_path):
        '''将所有实例转换为json'''
        song_dict = {'songs': []}
        for _, song in cls.instances.items():
            song_dict['songs'].append(song.__dict__)
        with open(file_path, 'w', encoding='utf-8') as f:
            json5.dump(song_dict, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    Song.read_songs_from_file(os.path.join(
        os.path.dirname(__file__), 'data', 'song.json'))
    Song.handle_songs()
    with open(os.path.join(os.path.dirname(__file__), 'data', 'alias.txt'), 'r', encoding='utf-8') as f:
        for line in f.readlines():
            alias, songid = line.split()
            Song.instances[songid].alias.append(alias)
    Song.dump2json(os.path.join(
        os.path.dirname(__file__), 'data', 'song.json'))
