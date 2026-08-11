from .downscale_image_threshold import DownscaleImageThreshold

# （必填）填写 import 的类名称，key 需要全局唯一
NODE_CLASS_MAPPINGS = {
    "DownscaleImageThreshold": DownscaleImageThreshold,
}

# （可不写）UI 界面显示名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "DownscaleImageThreshold": "Downscale Image (threshold)",
}

all = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']