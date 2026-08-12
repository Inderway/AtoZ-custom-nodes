"""Prompt Selector

按索引读取指定文件夹内的 txt 文件并输出文本，排序与 Windows 资源管理器按名称排序一致（自然排序）。
txt 编码优先 UTF-8，失败时回退 GBK。索引越界时直接抛出错误。
"""

import os

from .utils import natural_key


class PromptSelector:
    def __init__(self):
        pass

    CATEGORY = "AtoZ-custom-nodes/text"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "index": ("INT", {"default": 0, "min": 0, "step": 1}),
                "folder": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    FUNCTION = "process"

    def process(self, index, folder):
        if not os.path.isdir(folder):
            raise FileNotFoundError(f"文件夹不存在: {folder}")

        files = [
            f for f in os.listdir(folder)
            if os.path.splitext(f)[1].lower() == '.txt'
            and os.path.isfile(os.path.join(folder, f))
        ]
        files = sorted(files, key=natural_key)

        if not files:
            raise FileNotFoundError(f"文件夹中没有找到 txt 文件: {folder}")

        if index >= len(files):
            raise ValueError(f"索引 {index} 越界，文件夹内共 {len(files)} 个 txt 文件")

        path = os.path.join(folder, files[index])
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(path, 'r', encoding='gbk') as f:
                text = f.read()

        return (text,)


NODE_CLASS_MAPPINGS = {"PromptSelector": PromptSelector}
NODE_DISPLAY_NAME_MAPPINGS = {"PromptSelector": "Prompt Selector"}