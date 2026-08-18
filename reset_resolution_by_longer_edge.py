"""Reset Resolution by Longer Edge

根据输入图片的宽高朝向，重置给定的宽高分配：
图片为竖图（高 > 宽）时，将给定的 width、height 互换后输出；
图片为横图（宽 >= 高）时，按给定的 width、height 原样输出。

例：给定 width=800, height=600；图片实际 60x80（竖图），则输出 600, 800；
图片实际 90x70（横图），则输出 800, 600。
"""


class ResetResolutionByLongerEdge:
    def __init__(self):
        pass

    CATEGORY = "AtoZ-custom-nodes/image"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 1024, "min": 16, "max": 16384, "step": 8}),
                "height": ("INT", {"default": 1024, "min": 16, "max": 16384, "step": 8}),
            },
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("output_width", "output_height")

    FUNCTION = "process"

    def process(self, image, width, height):
        # IMAGE: [B, H, W, C]，取第一张图判断朝向
        h, w = image.shape[1], image.shape[2]
        if h > w:
            # 竖图：给定的较大值应分配给图片较长的高边
            output_width, output_height = height, width
        else:
            output_width, output_height = width, height
        return (output_width, output_height)


NODE_CLASS_MAPPINGS = {"ResetResolutionByLongerEdge": ResetResolutionByLongerEdge}
NODE_DISPLAY_NAME_MAPPINGS = {"ResetResolutionByLongerEdge": "Reset Resolution by Longer Edge"}
