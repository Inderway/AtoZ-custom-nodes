# AtoZ-custom-nodes

ComfyUI 自定义节点库。

## 安装

将本文件夹复制到 ComfyUI 的 `custom_nodes` 目录下。

```bash
# 复制到 custom_nodes 后，安装节点所需的第三方依赖（如有）
pip install -r requirements.txt
```

## 目录结构

```
AtoZ-custom-nodes/
├── __init__.py        # 节点注册入口
├── requirements.txt   # 节点依赖清单（仅包含节点自身需要的第三方包）
└── ...                # 节点代码（当前平铺存放，后续按功能分类重构）
```

## 依赖说明

`requirements.txt` 仅包含节点代码实际使用到的第三方依赖，ComfyUI 运行时自带的依赖（`torch`、`numpy`、`Pillow` 等）不包含在内。

## 节点列表

| 节点 | 说明 |
|------|------|
| Resize Image | 无论图片大小，等比缩放至指定尺寸（默认 2560x1920，按朝向分配长短边）；不足区域以边缘像素填充并模糊化，过渡平滑 |
| Reset Resolution by Longer Edge | 根据输入图片朝向重置给定的宽高分配：竖图（高>宽）时交换给定的 width/height，横图时原样输出；用于按图片长边分配分辨率 |
| Load Image (index) | 按索引读取指定文件夹内的图片，排序与 Windows 按名称排序一致（自然排序，如 2.jpg 排在 10.jpg 前）；支持 jpg/jpeg/bmp/webp/png；索引越界抛出错误 |
| Prompt Selector | 按索引读取指定文件夹内的 txt 文件并输出文本（UTF-8 优先，GBK 回退）；自然排序；索引越界抛出错误 |
| File Selector | 按索引读取指定文件夹内指定格式的文件路径（format 逗号分隔多格式，空串不过滤）；仅统计匹配格式的文件，索引只在该范围内取值；自然排序；索引越界抛出错误 |