'''用于生成图片的模块'''
import os
from typing import List
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import base64

# template:1146*1989
# player:(480,156,576,51)
# rks:(551,209,207,41)
# illus:(61,330) (232,232)
# stride: (264,328)
# difficulty: (253,494,56,22)
# level: (271,529,37,18)
# name: (106,568,190,25)
# acc: (107,594,190,25)
# rks_single: (159,622,83,19)


class SingleAchievement:
    '''单曲成绩,包含了绘图所有需要的信息'''

    def __init__(self, name: str, difficulty: float, level: str, acc: float, rks: float, illus_path: str):
        self.name = name
        self.difficulty = difficulty
        self.level = level
        self.acc = acc
        self.rks = rks
        self.illus_path = illus_path


class B19Template:
    '''b19模板的一些参数'''
    size = (1146, 1989)
    player = (480, 148)
    rks = (551, 200)
    illus_start = (61, 330)
    illus_size = (232, 232)
    stride = (264, 328)
    difficulty_start = (255, 494)
    difficulty_size = (56, 22)
    level_start = (275, 527)
    level_size = (37, 18)
    name_start = (112, 566)
    name_size = (190, 25)
    name_width = 179
    acc_start = (106, 594)
    acc_size = (190, 25)
    rks_single_start = (136, 620)
    rks_single_size = (83, 19)
    img = cv2.imread(os.path.join(os.path.dirname(__file__),
                     'data', 'b19_template.png'), cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)


class B19Image:
    '''b19图片类'''

    # 字体
    font = os.path.join(os.path.dirname(__file__), 'data',
                        'SourceHanSansSC-Heavy.otf')
    # 字体颜色
    color = (100, 102, 136)

    def __init__(self, player, rks, achievements: List[SingleAchievement]):
        '''初始化b19图片类并读取所有成绩的图片'''
        # TODO: 优化IO

        self.achievements = achievements
        self.player = player
        self.rks = rks
        self.illus = []
        rect = (484, 1564)
        for achievement in self.achievements:
            illus = cv2.imread(os.path.join(
                os.path.dirname(__file__), 'assets', achievement.illus_path))
            illus = cv2.cvtColor(illus, cv2.COLOR_BGR2RGB)
            illus = illus[:, rect[0]:rect[1], :]
            illus = cv2.resize(illus, B19Template.illus_size)
            self.illus.append(illus)

    async def b19_image(self):
        '''绘制b19图片,返回base64编码的图片用于消息元素构建.'''
        # 生成底板
        bg = np.zeros(B19Template.size, dtype=np.uint8).T
        bg = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)

        # 先将所有图片绘制到底板上
        for i, illus in enumerate(self.illus):
            index = (i % 4, i//4)
            start_x = B19Template.illus_start[1] + \
                index[1] * B19Template.stride[1]
            start_y = B19Template.illus_start[0] + \
                index[0] * B19Template.stride[0]
            bg[start_x:start_x+B19Template.illus_size[1],
                start_y:start_y+B19Template.illus_size[0], :] = illus
        alpha = B19Template.img[:, :, 3].copy()
        template = B19Template.img[:, :, :3].copy()
        bg[alpha >= 230] = template[alpha >= 230]

        b19_img = Image.fromarray(bg)
        # 绘制玩家名和rks
        face = ImageFont.truetype(B19Image.font, 36)
        draw = ImageDraw.Draw(b19_img)
        draw.text(B19Template.player, self.player, B19Image.color, font=face)
        draw.text(B19Template.rks, str("%.3f" %
                  self.rks), B19Image.color, font=face)
        # 绘制单曲成绩

        face = ImageFont.truetype(B19Image.font, 20)
        for i, achievement in enumerate(self.achievements):
            index = (i % 4, i//4)

            def func(x): return (
                x[0] + index[0] * B19Template.stride[0], x[1] + index[1] * B19Template.stride[1]-5)

            w, _ = face.getsize(achievement.name)
            if w > B19Template.name_width:
                # 把超过长度的部分用...代替
                max_len = int(B19Template.name_width/w*len(achievement.name))
                achievement.name = achievement.name[:max_len-3] + '...'

            draw.text(func(B19Template.name_start),
                      achievement.name, B19Image.color, font=face)
            draw.text(func(B19Template.difficulty_start),
                      str(achievement.difficulty), B19Image.color, font=face)
            draw.text(func(B19Template.level_start),
                      achievement.level, B19Image.color, font=face)
            draw.text(func(B19Template.acc_start),
                      str("%.3f" % achievement.acc), B19Image.color, font=face)
            draw.text(func(B19Template.rks_single_start),
                      str("%.3f" % achievement.rks), B19Image.color, font=face)

        result = np.array(b19_img)
        result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
        data = cv2.imencode('.png', result)[1]
        data_bytes = data.tobytes()
        data_base64 = base64.b64encode(data_bytes).decode('utf-8')
        return data_base64
