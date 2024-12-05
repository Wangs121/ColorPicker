## 介绍

一款使用custompicker做的颜色选择器

将rgb888转换为rgb565，方便调试嵌入式设备使用

![software](.\images\main.png)

### V1.0

基本功能完成

## 打包

```shell
auto-py-to-exe
```

生成的指令为

```shell
pyinstaller --noconfirm --onedir --windowed --icon "C:\Users\shuai\Desktop\ColorPicker\color_wheel_cropped.ico" --name "Color Picker" --add-data "C:\Users\shuai\anaconda3\envs\ColorPicker\Lib\site-packages\customtkinter;customtkinter/" --add-data "C:\Users\shuai\Desktop\ColorPicker\color_wheel_cropped.ico;." --add-data "C:\Users\shuai\Desktop\ColorPicker\color_wheel.png;." --add-data "C:\Users\shuai\Desktop\ColorPicker\target.png;."  "C:\Users\shuai\Desktop\ColorPicker\main.py"
```

## 依赖

```shell
pip install pyperclip
pip install pillow
pip install auto-py-to-exe
pip install PyInstaller
pip install CustomTkinter
```

## Reference

* [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
* [CTkColorPicker](https://github.com/Akascape/CTkColorPicker)
* [CTkColorPicker](https://github.com/UX0l0l/CTkColorPicker/tree/main)

