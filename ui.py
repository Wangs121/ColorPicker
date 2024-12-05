from doctest import master
import tkinter as tk
from customtkinter import StringVar
import customtkinter
import pyperclip
import re
# from UX0l0lCTkColorPicker import *

from AkascapeCTkColorPicker import *

app = customtkinter.CTk()
app.title("Color Picker")

NotifyLabel = None
btnRGB666 = None
btnRGB565 = None
textbox888 = None
textbox565 = None

switch_var = customtkinter.StringVar(value="off")

rgb888Var = customtkinter.StringVar()
rgb565Var = customtkinter.StringVar()


def configtextColor() -> bool:
    return switch_var.get() == 'off'


def RGB888toRGB565(hex_str: str):
    # Convert hex string to integer (remove the leading '#')
    rgb888 = int(hex_str.lstrip('#'), 16)

    # Extract the RGB components
    r = (rgb888 >> 16) & 0xFF
    g = (rgb888 >> 8) & 0xFF
    b = rgb888 & 0xFF

    # Convert to RGB565
    r_565 = (r >> 3) & 0x1F
    g_565 = (g >> 2) & 0x3F
    b_565 = (b >> 3) & 0x1F

    # Combine into RGB565
    rgb565 = (r_565 << 11) | (g_565 << 5) | b_565
    return f"0x{rgb565:04X}"


def RGB5665toRGB888(rgb565: str):
    # Extract the RGB components from the RGB565 value
    rgb565 = int(rgb565[2:], 16)
    r = (rgb565 >> 11) & 0x1F
    g = (rgb565 >> 5) & 0x3F
    b = rgb565 & 0x1F

    # Convert to RGB888
    r_888 = (r << 3) | (r >> 2)
    g_888 = (g << 2) | (g >> 4)
    b_888 = (b << 3) | (b >> 2)

    # Combine into a hex string
    rgb888 = (r_888 << 16) | (g_888 << 8) | b_888
    return f"#{rgb888:06X}"


def CopiedtoClipboardNotify(color):
    NotifyLabel.configure(text=f"Copied {color} to clipboard")


def btnRGB666_function():
    color = colorpicker.get()
    pyperclip.copy(color)
    CopiedtoClipboardNotify(color)


def btnRGB565_function():
    color = RGB888toRGB565(colorpicker.get())
    pyperclip.copy(color)
    CopiedtoClipboardNotify(color)


def colorpickerhandler(e):
    NotifyLabel.configure(text="")
    if configtextColor():
        # set button color
        btnRGB666.configure(text_color=e)
        btnRGB565.configure(text_color=e)
        # set textbox text
        textbox666.configure(text_color=e)
        textbox565.configure(text_color=e)
    else:
        btnRGB666.configure(fg_color=e)
        btnRGB565.configure(fg_color=e)
        # set textbox text
        textbox666.configure(fg_color=e)
        textbox565.configure(fg_color=e)
    textbox666.configure(textvariable=StringVar(value=e))
    textbox565.configure(textvariable=StringVar(value=RGB888toRGB565(e)))
    # textbox666.insert("0.0", text=e)
    # textbox565.delete('1.0', tk.END)
    # textbox565.insert("0.0", text=RGB888toRGB565(e))


def switch_event():
    if configtextColor():
        switch.configure(text="FG Color")
        # set colorpicker to fg color
    else:
        switch.configure(text="BG Color")
        # set colorpicker to bg color


def is_valid_rgb888(input_str):
    # 正则表达式匹配#后跟随6位16进制数字
    if input_str and input_str.startswith("#"):
        try:
            r, g, b = tuple(int(input_str.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
            return True
        except ValueError:
            return False
    return False


def is_valid_rgb565(input_str):
    if input_str and input_str.startswith("0x"):
        # 去掉前缀"0x"，并检查剩下的部分是否是有效的16进制数
        hex_str = input_str[2:]
        print(hex_str,len(hex_str))
        if len(hex_str) != 4:  # RGB565总共是16位，需要4个十六进制字符
            return False
        try:
            # 将十六进制字符串转换为整数
            color_value = int(hex_str, 16)

            print(color_value)
            if 0 <= color_value <= 0xFFFF:
                return True
            else:
                return False
        except ValueError:
            return False
    return False


def rgb888textChange(e):
    # print(f"input is rgb888{is_valid_rgb888(textbox666.get('1.0', tk.END))}")
    color = textbox666.get()
    if is_valid_rgb888(color):
        print(f"color {color}")
        # 色轮位置变换
        colorpicker.reset_target_position(color)
        textbox565.configure(textvariable=StringVar(value=RGB888toRGB565(color)))


def rgb585textChange(e):
    # print(f"input is rgb565{is_valid_rgb565(textbox565.get('1.0', tk.END))}")
    color = textbox565.get()
    print(color)
    if is_valid_rgb565(color):
        print(f"color {color}")
        color888 = RGB5665toRGB888(color)
        colorpickerhandler(color888)
        rgb888textChange(e)


switch = customtkinter.CTkSwitch(app, text="FG Color", command=switch_event,
                                 variable=switch_var, onvalue="on", offvalue="off")
LABEL_WIDTH, LABEL_HEIGH = 100, 40
INIT_BG_COLOR = "#FFFFFF"
INIT_FG_COLOR = "#000000"
NotifyLabel = customtkinter.CTkLabel(app, text="")
colorpicker = CTkColorPicker(master=app, width=300, command=colorpickerhandler, initial_color=INIT_BG_COLOR)
btnRGB666 = customtkinter.CTkButton(master=app, text='RGB888', width=LABEL_WIDTH, height=LABEL_HEIGH,
                                    fg_color=INIT_FG_COLOR, text_color=INIT_BG_COLOR,
                                    command=btnRGB666_function)
btnRGB565 = customtkinter.CTkButton(master=app, text='RGB565', width=LABEL_WIDTH, height=LABEL_HEIGH,
                                    fg_color=INIT_FG_COLOR, text_color=INIT_BG_COLOR,
                                    command=btnRGB565_function)
textbox666 = customtkinter.CTkEntry(master=app, width=LABEL_WIDTH, height=LABEL_HEIGH, fg_color=INIT_FG_COLOR,
                                    text_color=INIT_BG_COLOR, corner_radius=20,
                                    textvariable=StringVar(value=INIT_BG_COLOR))
textbox565 = customtkinter.CTkEntry(master=app, width=LABEL_WIDTH, height=LABEL_HEIGH, fg_color=INIT_FG_COLOR,
                                    text_color=INIT_BG_COLOR, corner_radius=20,
                                    textvariable=StringVar(value=RGB888toRGB565(INIT_BG_COLOR)))
textbox666.bind('<KeyRelease>', rgb888textChange)
textbox565.bind('<KeyRelease>', rgb585textChange)

row = 0
NotifyLabel.grid(row=row, column=0, columnspan=2)
row += 1
switch.grid(row=row, column=1, padx=20, sticky="ew", columnspan=2)
row += 1
colorpicker.grid(row=row, column=0, padx=20, sticky="ew", columnspan=2)

row += 1
btnRGB666.grid(row=row, column=0, padx=20, pady=20)
btnRGB565.grid(row=row, column=1, padx=20, pady=20)
row += 1
textbox666.grid(row=row, column=0, padx=20, pady=(0, 20))
textbox565.grid(row=row, column=1, padx=20, pady=(0, 20))
row += 1
app.mainloop()
