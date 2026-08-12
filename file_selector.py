"""File Selector

按索引读取指定文件夹内指定格式的文件路径并输出完整绝对路径，排序与 Windows 资源管理器按名称排序一致（自然排序）。
format 支持逗号分隔多格式（如 "mp4,jpg"），空字符串表示不过滤。
索引越界时直接抛出错误。
"""

import os

from .utils import natural_key


class FileSelector:
    def __init__(self):
        pass

    CATEGORY = "AtoZ-custom-nodes/file"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "index": ("INT", {"default": 0, "min": 0, "step": 1}),
                "folder": ("STRING", {"default": ""}),
                "format": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("path",)

    FUNCTION = "process"

    def process(self, index, folder, format):
        if not os.path.isdir(folder):
            raise FileNotFoundError(f"文件夹不存在: {folder}")

        if format.strip():
            extensions = tuple(
                f".{e.strip().lstrip('.')}" for e in format.split(',') if e.strip()
            )
        else:
            extensions = None

        files = [
            f for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f))
            and (extensions is None or os.path.splitext(f)[1].lower() in extensions)
        ]
        files = sorted(files, key=natural_key)

        if not files:
            raise FileNotFoundError(f"文件夹中没有找到匹配的文件: {folder}")

        if index >= len(files):
            raise ValueError(f"索引 {index} 越界，文件夹内共 {len(files)} 个匹配文件")

        path = os.path.abspath(os.path.join(folder, files[index]))

        return (path,)


NODE_CLASS_MAPPINGS = {"FileSelector": FileSelector}
NODE_DISPLAY_NAME_MAPPINGS = {"FileSelector": "File Selector"}