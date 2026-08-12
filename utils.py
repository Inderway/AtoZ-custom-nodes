"""公共工具函数"""

import re


def natural_key(name):
    """Windows 资源管理器按名称排序的自然排序 key

    文件名中的数字段按数值比较（如 2.jpg 排在 10.jpg 前），非数字段忽略大小写。
    """
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', name)]