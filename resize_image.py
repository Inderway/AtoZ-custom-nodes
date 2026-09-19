"""Resize Image

无论输入图片大小，均等比缩放至指定画布尺寸；不足区域以边缘像素扩展填充并模糊化，实现平滑自然的过渡效果。
横图以 long 为宽、short 为高，竖图以 short 为宽、long 为高。
"""

import cv2
import numpy as np
import torch


class ResizeImage:
    def __init__(self):
        pass

    CATEGORY = "AtoZ-custom-nodes/image"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "long": ("INT", {"default": 2560, "min": 16, "max": 16384, "step": 8}),
                "short": ("INT", {"default": 1920, "min": 16, "max": 16384, "step": 8}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("image", "width", "height")

    FUNCTION = "process"

    def process(self, image, long, short):
        h, w = image.shape[1], image.shape[2]
        # 根据图片宽高对比决定目标尺寸：宽>高为横图，宽<高为竖图
        if w > h:
            target_w, target_h = long, short
        else:
            target_w, target_h = short, long

        # tensor [0,1] float32 -> numpy uint8
        img = np.clip(255. * image[0].cpu().numpy(), 0, 255).astype(np.uint8)
        h, w = img.shape[:2]

        # 等比缩放以完整放入目标画布
        scale = min(target_w / w, target_h / h)
        new_w = int(round(w * scale))
        new_h = int(round(h * scale))
        resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

        # 比例吻合时直接输出
        if new_w == target_w and new_h == target_h:
            return (self._to_tensor(resized_img), new_w, new_h)

        # 居中计算 padding 边距
        pad_w = target_w - new_w
        pad_h = target_h - new_h
        pad_top = pad_h // 2
        pad_bottom = pad_h - pad_top
        pad_left = pad_w // 2
        pad_right = pad_w - pad_left

        # 边缘像素扩展填充
        padded = cv2.copyMakeBorder(
            resized_img, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_REPLICATE
        )

        # 高斯模糊背景，实现填充区域的平滑过渡
        blur_kernel_size = 51
        blurred_background = cv2.GaussianBlur(padded, (blur_kernel_size, blur_kernel_size), 0)

        # 原图区域遮罩（原图为1，填充区为0），高斯模糊实现羽化过渡
        feather_dist = 15
        mask = np.zeros((target_h, target_w), dtype=np.float32)
        mask[pad_top:pad_top + new_h, pad_left:pad_left + new_w] = 1.0
        mask = cv2.GaussianBlur(mask, (feather_dist * 2 + 1, feather_dist * 2 + 1), 0)

        # 匹配通道维度，广播融合
        if padded.ndim == 3:
            mask = np.expand_dims(mask, axis=2)

        final_img = (
            padded.astype(np.float32) * mask +
            blurred_background.astype(np.float32) * (1.0 - mask)
        ).astype(np.uint8)

        return (self._to_tensor(final_img), target_w, target_h)

    @staticmethod
    def _to_tensor(img):
        # numpy uint8 -> tensor [0,1] float32，补充 batch 维度
        return torch.from_numpy(img.astype(np.float32) / 255.0).unsqueeze(0)


NODE_CLASS_MAPPINGS = {"ResizeImage": ResizeImage}
NODE_DISPLAY_NAME_MAPPINGS = {"ResizeImage": "Resize Image"}
