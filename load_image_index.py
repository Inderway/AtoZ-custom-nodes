"""Load Image (index)

按索引读取指定文件夹内的图片，排序与 Windows 资源管理器按名称排序一致（自然排序）。
例如 2.jpg 排在 10.jpg 前面。索引越界时直接抛出错误。
"""

import os
import re

import numpy as np
import torch
from PIL import Image, ImageOps


def natural_key(name):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', name)]


class LoadImageIndex:
    def __init__(self):
        pass

    CATEGORY = "AtoZ-custom-nodes/image"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "index": ("INT", {"default": 0, "min": 0, "step": 1}),
                "folder": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)

    FUNCTION = "process"

    def process(self, index, folder):
        if not os.path.isdir(folder):
            raise FileNotFoundError(f"文件夹不存在: {folder}")

        valid_extensions = ('.jpg', '.jpeg', '.bmp', '.webp', '.png')
        files = [
            f for f in os.listdir(folder)
            if os.path.splitext(f)[1].lower() in valid_extensions
            and os.path.isfile(os.path.join(folder, f))
        ]
        files = sorted(files, key=natural_key)

        if not files:
            raise FileNotFoundError(f"文件夹中没有找到支持的图片: {folder}")

        if index >= len(files):
            raise ValueError(f"索引 {index} 越界，文件夹内共 {len(files)} 张图片")

        path = os.path.join(folder, files[index])
        i = Image.open(path)
        i = ImageOps.exif_transpose(i)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (image,)


NODE_CLASS_MAPPINGS = {"LoadImageIndex": LoadImageIndex}
NODE_DISPLAY_NAME_MAPPINGS = {"LoadImageIndex": "Load Image (index)"}