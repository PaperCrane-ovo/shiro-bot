'''phigros 歌曲类'''
import json5
import os


class Song:
    '''歌曲类,包含歌曲的所有信息以及难度谱师等等.'''

    song_info: dict
    instances: dict = {}

    @classmethod
    def read_songs_from_file(cls, file_path: str):
        '''从文件中读取歌曲信息'''
        with open(file_path, 'r', encoding='utf-8') as f:
            cls.song_info = json5.load(f)['song']  # type: ignore

    @classmethod
    def handle_songs(cls):
        '''处理歌曲信息'''
        cnt = 1
        for _, songs in cls.song_info.items():
            for song in songs:
                cls(song['songsId'], cnt, song['songsName'], song['difficulty'],
                    song['levels'], song['composer'], song['illustrator'], song['charter'],
                    song['alias'])
                cnt += 1

    def __init__(self,
                 song_id,
                 song_number,
                 song_name,
                 difficulty,
                 level,
                 composer,
                 illustrator,
                 charter,
                 alias):
        '''初始化歌曲类'''
        self.song_number = song_number
        self.song_id = song_id
        self.song_name = song_name
        self.difficulty = difficulty
        self.level = level
        self.composer = composer
        self.illustrator = illustrator
        self.chapter = charter
        self.img_path = f'{str(song_number)+"_"+song_name.replace(" ", "")}.png'
        self.alias = alias
        Song.instances[song_id] = self

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
    illus_dir = os.path.dirname(__file__)+"/phigros曲绘"
    with open(os.path.dirname(__file__)+'/song.json', 'r', encoding='utf-8') as f:
        song_info = json5.load(f)['songs']  # type: ignore
    for song in song_info:
        if not os.path.exists(illus_dir+'/'+song['img_path']):
            print(song['img_path'])
