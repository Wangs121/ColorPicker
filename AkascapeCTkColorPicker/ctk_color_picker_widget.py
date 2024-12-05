# CTk Color Picker widget for customtkinter
# Author: Akash Bora (Akascape)

import tkinter
import customtkinter
from PIL import Image, ImageTk
import sys
import os
import math
import colorsys

PATH = os.path.dirname(os.path.realpath(__file__))


def load_media(name):
    if getattr(sys, 'frozen', False):  # 判断程序是否打包成了可执行文件
        img_path = os.path.join(sys._MEIPASS, name)  # 获取临时解压目录中的路径
    else:
        img_path = name  # 如果是源代码模式，则直接使用相对路径
    return img_path

class CTkColorPicker(customtkinter.CTkFrame):

    def __init__(self,
                 master: any = None,
                 width: int = 300,
                 initial_color: str = None,
                 fg_color: str = None,
                 slider_border: int = 1,
                 corner_radius: int = 24,
                 command=None,
                 orientation="vertical",
                 **slider_kwargs):

        super().__init__(master=master, corner_radius=corner_radius)

        WIDTH = width if width >= 200 else 200
        HEIGHT = WIDTH + 150
        self.image_dimension = int(self._apply_widget_scaling(WIDTH - 100))
        self.target_dimension = int(self._apply_widget_scaling(20))
        self.lift()

        self.after(10)
        self.default_hex_color = "#ffffff"
        self.default_rgb = [255, 255, 255]
        self.rgb_color = self.default_rgb[:]

        self.fg_color = self._apply_appearance_mode(self._fg_color) if fg_color is None else fg_color
        self.corner_radius = corner_radius

        self.command = command

        self.slider_border = 10 if slider_border >= 10 else slider_border

        self.configure(fg_color=self.fg_color)

        self.canvas = tkinter.Canvas(self, height=self.image_dimension, width=self.image_dimension,
                                     highlightthickness=0, bg=self.fg_color)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<Button-1>", self.on_mouse_drag)

        self.img1 = Image.open(load_media('color_wheel.png')).resize(
            (self.image_dimension, self.image_dimension), Image.Resampling.LANCZOS)
        self.img2 = Image.open(load_media('target.png')).resize((self.target_dimension, self.target_dimension),
                                                       Image.Resampling.LANCZOS)

        self.wheel = ImageTk.PhotoImage(self.img1)
        self.target = ImageTk.PhotoImage(self.img2)

        self.canvas_wheel = self.canvas.create_image(self.image_dimension / 2, self.image_dimension / 2,
                                                     image=self.wheel)
        self.brightness_slider_value = customtkinter.IntVar()
        self.brightness_slider_value.set(255)

        self.slider = customtkinter.CTkSlider(master=self, width=20, border_width=self.slider_border,
                                              button_length=15, progress_color=self.default_hex_color, from_=0, to=255,
                                              variable=self.brightness_slider_value, number_of_steps=256,
                                              button_corner_radius=self.corner_radius, corner_radius=self.corner_radius,
                                              command=lambda x: self.update_colors(), orientation=orientation,
                                              **slider_kwargs)
        self.canvas_target = self.set_initial_color(initial_color)

        # self.label = customtkinter.CTkLabel(master=self, text_color="#000000", width=10,
        #                                     fg_color=self.default_hex_color,
        #                                     corner_radius=self.corner_radius, text=self.default_hex_color, wraplength=1)
        if orientation == "vertical":
            self.canvas.pack(pady=20, side="left", padx=(10, 0))
            self.slider.pack(fill="y", pady=15, side="right", padx=(0, 10 - self.slider_border))
            # self.label.pack(expand=True, fill="both", padx=10, pady=15)
        else:
            # self.label.configure(wraplength=100)
            self.canvas.pack(pady=15, padx=15)
            self.slider.pack(fill="x", pady=(0, 10 - self.slider_border), padx=15)
            # self.label.pack(expand=True, fill="both", padx=15, pady=(0, 15))

    def get(self):
        return self.default_hex_color

    def destroy(self):
        super().destroy()
        del self.img1
        del self.img2
        del self.wheel
        del self.target

    def on_mouse_drag(self, event):
        x = event.x
        y = event.y
        self.canvas.delete(self.canvas_target)
        # self.canvas.delete("all")
        # self.canvas.create_image(self.image_dimension / 2, self.image_dimension / 2, image=self.wheel)

        d_from_center = math.sqrt(((self.image_dimension / 2) - x) ** 2 + ((self.image_dimension / 2) - y) ** 2)

        if d_from_center < self.image_dimension / 2:
            self.target_x, self.target_y = x, y
        else:
            self.target_x, self.target_y = self.projection_on_circle(x, y, self.image_dimension / 2,
                                                                     self.image_dimension / 2,
                                                                     self.image_dimension / 2 - 1)

        self.canvas_target = self.canvas.create_image(self.target_x, self.target_y, image=self.target)

        self.get_target_color()
        self.update_colors()

    def get_target_color(self):
        try:
            self.rgb_color = self.img1.getpixel((self.target_x, self.target_y))
            r = self.rgb_color[0]
            g = self.rgb_color[1]
            b = self.rgb_color[2]
            self.rgb_color = [r, g, b]
        except AttributeError:
            self.rgb_color = self.default_rgb

    def update_colors(self):
        brightness = self.brightness_slider_value.get()

        self.get_target_color()

        # r, g, b = self.position_to_color(self.target_x, self.target_y, brightness / 255)
        r = int(self.rgb_color[0] * (brightness / 255))
        g = int(self.rgb_color[1] * (brightness / 255))
        b = int(self.rgb_color[2] * (brightness / 255))

        self.rgb_color = [r, g, b]

        self.default_hex_color = "#{:02x}{:02x}{:02x}".format(*self.rgb_color)

        self.slider.configure(progress_color=self.default_hex_color)

        if self.command:
            self.command(self.get().upper())

    def projection_on_circle(self, point_x, point_y, circle_x, circle_y, radius):
        angle = math.atan2(point_y - circle_y, point_x - circle_x)
        projection_x = circle_x + radius * math.cos(angle)
        projection_y = circle_y + radius * math.sin(angle)

        return projection_x, projection_y

    def set_initial_color(self, initial_color):
        # set_initial_color is in beta stage, cannot seek all colors accurately

        if initial_color and initial_color.startswith("#"):
            try:
                r, g, b = tuple(int(initial_color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
            except ValueError:
                return None

            self.default_hex_color = initial_color
            self.target_x, self.target_y = self.set_target_position(r, g, b)
            # print(f"x{self.target_x},y{self.target_y}")
            return self.canvas.create_image(self.target_x, self.target_y, image=self.target)

        return self.canvas.create_image(self.image_dimension / 2, self.image_dimension / 2, image=self.target)

    # 根据颜色RGB计算位置（极坐标位置）
    def set_target_position(self, r, g, b):
        h, s, v = rgb_to_hsv(r, g, b)
        # print(f"h{h},s{s},v{v}")
        # 计算对应的极坐标位置
        # 根据图像的尺寸，将极坐标映射到屏幕坐标
        radius = s * min(self.image_dimension, self.image_dimension) / 2  # 半径由饱和度决定，映射到图像大小
        theta = h * 2 * math.pi  # 色调决定角度

        # 计算坐标
        x = int(self.image_dimension / 2 + radius * math.cos(theta))  # 水平坐标
        y = int(self.image_dimension / 2 + radius * math.sin(theta))  # 垂直坐标，注意y轴方向在图像中是反向的
        x = clamp(x, 1, 199)
        y = clamp(y, 1, 199)
        # print(f"x{x},y{y}")
        self.slider.set(v * 255)
        return x, y

    def reset_target_position(self, color: str):
        if color and color.startswith("#"):
            try:
                r, g, b = tuple(int(color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
                # print(f"r{r},g{g},b{b}")
                self.target_x, self.target_y = self.set_target_position(r, g, b)
                self.canvas.delete(self.canvas_target)
                self.canvas_target = self.canvas.create_image(self.target_x, self.target_y, image=self.target)
            except ValueError:
                return

    # 根据坐标计算颜色RGB
    def position_to_color(self, x, y, v):
        # 将图像坐标转换为极坐标
        cx, cy = self.image_dimension / 2, self.image_dimension / 2
        dx, dy = x - cx, -y - cy

        # 计算半径（饱和度）和角度（色调）
        radius = math.sqrt(dx ** 2 + dy ** 2) / (min(self.image_dimension, self.image_dimension) / 2)
        theta = math.atan2(-dy, dx)  # 角度，反向y轴

        # 将角度从弧度转换为0-1之间的色调
        h = (theta + math.pi) / (2 * math.pi)

        # 计算亮度（v），假设亮度固定为1.0
        # v = 1.0

        # 根据半径计算饱和度（s）
        s = min(radius, 1.0)

        # 根据HSV值计算RGB
        return hsv_to_rgb(h, s, v)


# 转换RGB到HSV
def rgb_to_hsv(r, g, b):
    return colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)


# 转换HSV到RGB
def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)
