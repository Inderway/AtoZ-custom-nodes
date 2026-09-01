"""Count Files

统计指定文件夹下的文件数量（不包含子文件夹及子文件夹中的文件）。
"""

import os


class CountFiles:
    def __init__(self):
        pass

    CATEGORY = "AtoZ-custom-nodes/file"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("count",)

    FUNCTION = "process"

    def process(self, folder):
        if not os.path.isdir(folder):
            raise FileNotFoundError(f"文件夹不存在: {folder}")

        count = sum(
            1 for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f))
        )

        return (count,)


NODE_CLASS_MAPPINGS = {"CountFiles": CountFiles}
NODE_DISPLAY_NAME_MAPPINGS = {"CountFiles": "Count Files"}
