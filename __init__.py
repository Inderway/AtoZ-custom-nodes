from .downscale_image_threshold import DownscaleImageThreshold
from .reset_resolution_by_longer_edge import ResetResolutionByLongerEdge
from .load_image_index import LoadImageIndex
from .prompt_selector import PromptSelector
from .file_selector import FileSelector

# （必填）填写 import 的类名称，key 需要全局唯一
NODE_CLASS_MAPPINGS = {
    "DownscaleImageThreshold": DownscaleImageThreshold,
    "ResetResolutionByLongerEdge": ResetResolutionByLongerEdge,
    "LoadImageIndex": LoadImageIndex,
    "PromptSelector": PromptSelector,
    "FileSelector": FileSelector,
}

# （可不写）UI 界面显示名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "DownscaleImageThreshold": "Downscale Image (threshold)",
    "ResetResolutionByLongerEdge": "Reset Resolution by Longer Edge",
    "LoadImageIndex": "Load Image (index)",
    "PromptSelector": "Prompt Selector",
    "FileSelector": "File Selector",
}

all = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']