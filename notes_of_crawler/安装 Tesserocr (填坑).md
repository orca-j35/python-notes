# 安装 Tesserocr (填坑)

[TOC]

> 环境：
>
> - Win10_64
> - Python 3.6.6，安装路径 `C:\Python36` (后面会用到该路径)

## 1. 安装

### 1.1. tesserocr

[tesserocr](https://github.com/sirfz/tesserocr) 是 Python 下的一个 OCR 识别库，该库本质上是对 [tesseract](https://github.com/tesseract-ocr/tesseract) 做了一层 Python API 封装。通过 tesserocr 的 [PyPI页面](https://pypi.org/project/tesserocr/)，可以找到该项目的 [GitHub 仓库](https://github.com/sirfz/tesserocr) 。仓库的 `README.rst` 中介绍了 Windows 平台的安装方式，原文如下：

> The proposed downloads consist of stand-alone packages containing all the Windows libraries needed for execution. This means that no additional installation of tesseract is required on your system. 
>
> --snip: 这里跳过了使用 Conda 安装的方式，需要的话可以查看原文档--
>
>  pip：Download the wheel file corresponding to your Windows platform and Python installation from [simonflueckiger/tesserocr-windows_build/releases](https://github.com/simonflueckiger/tesserocr-windows_build/releases) and install them via:
>
> ```
> > pip install <package_name>.whl
> ```

也就是说，由于 stand-alone packages 中包含了 Windows 下所需的所有库。所以，如果我们使用 stand-alone packages 安装 tesserocr ，便无需再额外安装 tesseract 。

------

- 坑：stand-alone packages 确实包含了 Windows 下所需的所有库，但并是不包含语言数据文件(language data files)。另外，数据文件需要被统一放置在 `tessdata\` 文件夹中，并置于 `C:\Python36` 内。

  

------

接下来，按照上述方法通过 pip 安装对应的 `.whl` 。
不要通过 `pip3 install tesserocr` 直接安装，因为在 Windows 上会失败——[据说这种方式只能用于 Linux](https://blog.csdn.net/coolcooljob/article/details/80385711)，但我没有仔细研究过。

注意： tesserocr 和 tesseract 版本要匹配，如 "tesserocr v2.2.2 (tesseract 4.0.0 master)" 释放，表明 "tesserocr-2.2.2" 要配合 "tesseract 4.0.0 master" 使用。如果 tesserocr 与 tesseract 间版本不匹配，识别结果中会出现非预期字符。由于，目前 Windows 下 tesseract 最新稳定版是 3.5.2，于是我试图安装 "tesserocr v2.2.2 (tesseract 3.5.1)" 版本的 `.whl` 文件，却提示该 `.whl` 文件不支持当前平台，无法安装。因此，只能安装  "tesserocr v2.2.2 (tesseract 4.0.0 master)" 版本，并配合 "tesseract 4.0.0 master" 使用。—— **坑_2**

如果将 `tesseract 3.5.2` 的 "tessdata\" 配合 "tesserocr-2.2.2" 使用，便会出现非预期字符。

tesseract  版本正确后，还需要使用 tessdata_fast.

### 1.2. tesseract

通过查看 tesseract 的 [GitHub 仓库](https://github.com/tesseract-ocr/tesseract) 的 [Wiki](https://github.com/tesseract-ocr/tesseract/wiki) 主页，可得知 [Windows 下的安装方法](https://github.com/tesseract-ocr/tesseract/wiki#windows) ，原文如下：

> Installer for Windows for Tesseract 3.05-02 and Tesseract 4.00-beta are available from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki). These include the training tools. Both 32-bit and 64-bit installers are available. 
>
> An installer for the **OLD version 3.02** is available for Windows from our [download](https://github.com/tesseract-ocr/tesseract/wiki/Downloads) page. This includes the English training data. If you want to use another language, [download the appropriate training data](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files), unpack it using [7-zip](http://www.7-zip.org/), and copy the .traineddata file into the 'tessdata' directory, probably `C:\Program Files\Tesseract-OCR\tessdata`. 
>
> To access tesseract-OCR from any location you may have to add the directory where the tesseract-OCR binaries are located to the Path variables, probably `C:\Program Files\Tesseract-OCR`. 

也就是说通过 [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)，我们便可获得 Windows 安装包。
UB-Mannheim/tesseract/wiki 中的原文如下：

> The latest installers can be downloaded here: [tesseract-ocr-setup-3.05.02-20180621.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-3.05.02-20180621.exe), [tesseract-ocr-w32-setup-v4.0.0-beta.1.20180608.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v4.0.0-beta.1.20180608.exe) and [tesseract-ocr-w64-setup-v4.0.0-beta.1.20180608.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.0.0-beta.1.20180608.exe) (new, 64 bit, experimental). There are also [older versions](https://digi.bib.uni-mannheim.de/tesseract/) available. 

如果需要  [older versions](https://digi.bib.uni-mannheim.de/tesseract/) 可以去到 https://digi.bib.uni-mannheim.de/tesseract/ 下载。
这里要安装 "tesseract-ocr-w64-setup-v4.0.0-beta.1.20180608.exe"，因为要与 tesserocr-2.2.2 匹配。

安装完成后，需要将 `C:\Program Files (x86)\Tesseract-OCR` 添加到环境变量中。

另外，tesseract 的文档位于 https://github.com/tesseract-ocr/tesseract/wiki/Documentation

#### 1.2.3 语言包

通过 wiki 的 [Data Files](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files) 部分，我们可以下载经过训练的语言包。将下载后的语言包，直接放到`C:\Program Files (x86)\Tesseract-OCR\tessdata`  即可使用。

注意语言包有三个分支：—— **坑_3** 

- <https://github.com/tesseract-ocr/tessdata_best>
- <https://github.com/tesseract-ocr/tessdata_fast>
- <https://github.com/tesseract-ocr/tessdata>

在使用语言数据时要注意区分 Tesseract 的版本，3.04 或 3.05 的语言数据需要从 [3.04 tree](https://github.com/tesseract-ocr/tessdata/tree/3.04.00) 获取。在 [Data Files](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files) 我们可以了解到更多语言包的分支，及其区别。

## 2. 填坑

### 2.1 坑_1

如果依照官方文档，只安装了 tesserocr 的 `.whl` 文件，并尝试运行如下测试代码：

```python
import tesserocr
from PIL import Image
image = Image.open('image.png')
print(tesserocr.image_to_text(image))
```

便会得到如下错误提示：

```
Traceback (most recent call last):
  File "c:/Users/iwhal/Documents/GitHub/python_notes/notes_of_crawler/code_of_learn_is_ignored/test_of_tesserocr .py", line 4, in <module>
    print(tesserocr.image_to_text(image))
  File "tesserocr.pyx", line 2401, in tesserocr._tesserocr.image_to_text
RuntimeError: Failed to init API, possibly an invalid tessdata path: C:\\
```

因此我们仍然需要安装 tesseract，并将 `C:\Program Files (x86)\Tesseract-OCR\`  下的 `tessdata\` 文件夹复制到 `C:\Python36` 。



测试了几种验证码，感觉 tessdata_fast 表现最稳定

