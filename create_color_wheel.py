import numpy as np
import colorsys
import matplotlib.pyplot as plt
import math


# 创建无透明边框的色环图
def create_color_wheel_no_border(output_file="color_wheel.png"):
    # 设置图像尺寸
    fig = plt.figure(figsize=[7.3, 7.3])
    ax = fig.add_subplot(projection='polar')

    # 定义极坐标的半径和角度范围
    rho = np.linspace(0, 1, 500)  # 半径从中心到外缘
    phi = np.linspace(0, 2 * np.pi, 1000)  # 完整的角度范围

    RHO, PHI = np.meshgrid(rho, phi)  # 网格化半径和角度

    # 色调映射到角度
    h = (PHI - PHI.min()) / (PHI.max() - PHI.min())  # 色调范围归一化到0-1
    h = np.flip(h)  # 翻转色调方向
    s = RHO  # 饱和度随半径变化
    v = np.ones_like(RHO)  # 亮度固定为1

    # 将HSV转换为RGB
    h, s, v = h.flatten().tolist(), s.flatten().tolist(), v.flatten().tolist()
    c = [colorsys.hsv_to_rgb(*x) for x in zip(h, s, v)]
    c = np.array(c)

    # 绘制色环
    ax.scatter(PHI, RHO, c=c, marker=".")

    # 关闭坐标轴，避免显示边框和刻度
    ax.axis('off')

    # 调整布局，确保无空白
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # 移除透明边框并保存为方形图像
    plt.savefig(output_file, format='png', transparent=True, bbox_inches='tight', pad_inches=0, dpi=300)
    plt.close(fig)
    print(f"色环图已保存到：{output_file}")


from PIL import Image
import numpy as np


# 裁剪透明边框
def crop_transparent_border(input_image, output_image):
    # 打开图像
    img = Image.open(input_image)

    # 转换为 RGBA 模式（包含透明度通道）
    img = img.convert("RGBA")

    # 获取图像的 alpha 通道（透明度通道）
    data = np.array(img)

    # 找到 alpha 通道的非透明部分
    alpha_channel = data[:, :, 3]  # alpha 通道
    non_transparent_rows = np.any(alpha_channel > 0, axis=1)  # 非透明行
    non_transparent_cols = np.any(alpha_channel > 0, axis=0)  # 非透明列

    # 获取裁剪的边界
    top = np.argmax(non_transparent_rows)  # 最上面非透明行
    bottom = len(non_transparent_rows) - np.argmax(non_transparent_rows[::-1])  # 最下面非透明行
    left = np.argmax(non_transparent_cols)  # 最左边非透明列
    right = len(non_transparent_cols) - np.argmax(non_transparent_cols[::-1])  # 最右边非透明列

    # 使用裁剪边界裁剪图像
    img_cropped = img.crop((left, top, right, bottom))

    # 保存裁剪后的图像
    img_cropped.save(output_image, format='PNG')

    print(f"裁剪后的图像已保存为：{output_image}")


# 调用函数生成色环图
# create_color_wheel_no_border("color_wheel.png")

# 调用裁剪函数
crop_transparent_border("color_wheel.png", "color_wheel_cropped.png")
