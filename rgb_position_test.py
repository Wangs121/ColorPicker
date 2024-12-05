import numpy as np
import colorsys
import matplotlib.pyplot as plt
import math

# 定义图像的尺寸
WIDTH, HEIGHT = 500, 500  # 图像宽度和高度


# 转换RGB到HSV
def rgb_to_hsv(r, g, b):
    return colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)


# 转换HSV到RGB
def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


# 根据颜色RGB计算位置（极坐标位置）
def color_to_position(r, g, b):
    h, s, v = rgb_to_hsv(r, g, b)

    # 计算对应的极坐标位置
    # 根据图像的尺寸，将极坐标映射到屏幕坐标
    radius = s * min(WIDTH, HEIGHT) / 2  # 半径由饱和度决定，映射到图像大小
    theta = h * 2 * np.pi  # 色调决定角度

    # 计算坐标
    x = WIDTH / 2 + radius * np.cos(theta)  # 水平坐标
    y = HEIGHT / 2 - radius * np.sin(theta)  # 垂直坐标，注意y轴方向在图像中是反向的

    return x, y


# 根据坐标计算颜色RGB
def position_to_color(x, y):
    # 将图像坐标转换为极坐标
    cx, cy = WIDTH / 2, HEIGHT / 2
    dx, dy = x - cx, y - cy

    # 计算半径（饱和度）和角度（色调）
    radius = np.sqrt(dx ** 2 + dy ** 2) / (min(WIDTH, HEIGHT) / 2)
    theta = np.arctan2(-dy, dx)  # 角度，反向y轴

    # 将角度从弧度转换为0-1之间的色调
    h = (theta + np.pi) / (2 * np.pi)

    # 计算亮度（v），假设亮度固定为1.0
    v = 1.0

    # 根据半径计算饱和度（s）
    s = min(radius, 1.0)

    # 根据HSV值计算RGB
    return hsv_to_rgb(h, s, v)


# 测试示例：根据RGB获取坐标，反向获取颜色
def test_color_position():
    r, g, b = 255, 0, 0  # 红色
    x, y = color_to_position(r, g, b)
    print(f"RGB({r}, {g}, {b}) -> Position: ({x:.2f}, {y:.2f})")

    r, g, b = position_to_color(x, y)
    print(f"Position ({x:.2f}, {y:.2f}) -> RGB({r}, {g}, {b})")


# 测试：绘制色环并标记一些位置
def plot_color_wheel():
    fig = plt.figure(figsize=[7.3, 7.3])
    ax = fig.add_subplot(projection='polar')

    rho = np.linspace(0, 1, 100)  # Radius of 1, distance from center to outer edge
    phi = np.linspace(0, math.pi * 2., 1000)  # in radians, one full circle

    RHO, PHI = np.meshgrid(rho, phi)  # get every combination of rho and phi

    h = (PHI - PHI.min()) / (PHI.max() - PHI.min())  # use angle to determine hue, normalized from 0-1
    h = np.flip(h)
    s = RHO  # saturation is set as a function of radius
    v = np.ones_like(RHO)  # value is constant

    # convert the np arrays to lists. This actually speeds up the colorsys call
    h, s, v = h.flatten().tolist(), s.flatten().tolist(), v.flatten().tolist()
    c = [colorsys.hsv_to_rgb(*x) for x in zip(h, s, v)]
    c = np.array(c)

    ax.scatter(PHI, RHO, c=c)

    # 标记红色的位置
    r, g, b = 255, 0, 0  # 红色
    x, y = color_to_position(r, g, b)
    ax.plot(np.arctan2(y - HEIGHT / 2, x - WIDTH / 2),
            np.sqrt((x - WIDTH / 2) ** 2 + (y - HEIGHT / 2) ** 2) / (min(WIDTH, HEIGHT) / 2), 'ro')  # 在极坐标系中标记红色

    ax.axis('off')
    plt.show()


# 调用测试函数
test_color_position()

# 调用绘制色环的函数
plot_color_wheel()
