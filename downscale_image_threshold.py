"""Downscale Image (threshold)

接受大尺寸图片，将其等比缩小至指定尺寸；未超过指定尺寸的图片原样输出。
缩小后不足画布的区域以边缘像素扩展填充并模糊化，实现平滑自然的过渡效果。
"""

import cv2
import numpy as np
import torch


class DownscaleImageThreshold:
    def __init__(self):
        pass

    CATEGORY = "AtoZ-custom-nodes/image"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 2560, "min": 16, "max": 16384, "step": 8}),
                "height": ("INT", {"default": 1920, "min": 16, "max": 16384, "step": 8}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)

    FUNCTION = "process"

    def process(self, image, width, height):
        # 阈值判断：宽高均未超出目标尺寸，原样返回，不做转换避免精度损失
        h, w = image.shape[1], image.shape[2]
        if w <= width and h <= height:
            return (image,)

        # tensor [0,1] float32 -> numpy uint8
        img = np.clip(255. * image[0].cpu().numpy(), 0, 255).astype(np.uint8)
        h, w = img.shape[:2]

        # 等比缩小以完整放入目标画布
        scale = min(width / w, height / h)
        new_w = int(round(w * scale))
        new_h = int(round(h * scale))
        resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

        # 比例吻合时直接输出
        if new_w == width and new_h == height:
            return (self._to_tensor(resized_img),)

        # 居中计算 padding 边距
        pad_w = width - new_w
        pad_h = height - new_h
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
        mask = np.zeros((height, width), dtype=np.float32)
        mask[pad_top:pad_top + new_h, pad_left:pad_left + new_w] = 1.0
        mask = cv2.GaussianBlur(mask, (feather_dist * 2 + 1, feather_dist * 2 + 1), 0)

        # 匹配通道维度，广播融合
        if padded.ndim == 3:
            mask = np.expand_dims(mask, axis=2)

        final_img = (
            padded.astype(np.float32) * mask +
            blurred_background.astype(np.float32) * (1.0 - mask)
        ).astype(np.uint8)

        return (self._to_tensor(final_img),)

    @staticmethod
    def _to_tensor(img):
        # numpy uint8 -> tensor [0,1] float32，补充 batch 维度
        return torch.from_numpy(img.astype(np.float32) / 255.0).unsqueeze(0)


NODE_CLASS_MAPPINGS = {"DownscaleImageThreshold": DownscaleImageThreshold}
NODE_DISPLAY_NAME_MAPPINGS = {"DownscaleImageThreshold": "Downscale Image (threshold)"}