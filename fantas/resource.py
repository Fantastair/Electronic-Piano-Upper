# 用于加载、保存、整合资源文件（包括网络文件）的模块

import io
import pickle
from pathlib import Path
# from tempfile import TemporaryFile

import pygame
import pygame.freetype as freetype
freetype.init()

__all__ = ['load', 'dump', 'load_resource', 'load_bytes_resource', 'load_res_group', 'load_merged_res', 'merge_res', 'merge_res_group']


def load(file):
    # 从二进制文件加载 python 对象（解密）
    if not isinstance(file, Path):
        file = Path(file)
    with file.open('rb') as f:
        return pickle.loads(f.read()[-2:0:-1])

def dump(data, file):
    # 将 python 对象存储为二进制文件（加密）
    if not isinstance(file, Path):
        file = Path(file)
    with file.open('wb') as f:
        f.write(b'1' + pickle.dumps(data)[::-1] + b'1')


_font = lambda p: freetype.Font(p)
_image = lambda p: pygame.image.load(p).convert_alpha()
_sound = lambda p: pygame.mixer.Sound(p)
_color = lambda p: pickle.load(p)

load_method = {
    '.ttf': _font,
    '.otf': _font,
    '.png': _image,
    '.jpg': _image,
    '.gif': _image,
    '.mp3': _sound,
    '.ogg': _sound,
    '.wav': _sound,
    '.aac': _sound,
    '.color': _color,
}
def load_resource(path):
    # 从文件加载单个资源
    return load_method[path.suffix](path)

def load_bytes_resource(suffix, data: bytes):
    # 从二进制数据加载单个资源
    return load_method[suffix](io.BytesIO(data))

def load_res_group(path_group) -> dict:
    # 加载多个资源
    # path_group 里面的路径是<Path>对象
    return {i.stem: load_resource(i) for i in path_group}

def load_merged_res(file):
    # 从整合后的文件加载资源
    # 如果是分组的资源，在加载时会返回一个元组，用多个变量接受
    file = load(file)
    if isinstance(file, dict):
        return {i: load_bytes_resource(*file[i]) for i in file}
    else:
        return tuple(({j: load_bytes_resource(*i[j]) for j in i} for i in file))

def merge_res(path_group):
    # 将多个资源文件整合为一个
    # path_group 里面的路径是<Path>对象
    data = {}
    for i in path_group:
        with i.open('rb') as f:
            data[i.stem] = (i.suffix, f.read())
    return data

def merge_res_group(path_group):
    # 将多个资源文件分组后整合为一个
    # path_group 里面用列表存放每个组的<Path>路径
    return tuple((merge_res(i) for i in path_group))
