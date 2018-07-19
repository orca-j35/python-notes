# 安装 Tesserocr (填坑)

[TOC]

> 环境：
>
> - Win10_64
> - Python 3.6.6，安装路径 `C:\Python36` (后面会用到该路径)

## 1. 安装 Tesserocr

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

按照文档的意思，由于 stand-alone packages 中包含了 Windows 下所需的所有库。如果使用 stand-alone packages 安装 tesserocr ，便无需再额外安装 tesseract 。

这里一定要通过独立的 `.whl` 文件安装，不要通过 `pip3 install tesserocr` 直接安装，因为在 Windows 上会失败——[据说这种方式只能用于 Linux](https://blog.csdn.net/coolcooljob/article/details/80385711)，但我没有仔细研究过。

选择安装包时，tesserocr 和 tesseract 的版本要匹配，如 "tesserocr v2.2.2 (tesseract 4.0.0 master)" 释放，表明 "tesserocr-2.2.2" 要配合 "tesseract 4.0.0 master" 使用。如果 tesserocr 与 tesseract 间版本不匹配，识别结果中会出现非预期字符。例如，若是将 "tesserocr-2.2.2" 与 "tesseract 3.5.2" 搭配使用，结果中便会出现非预期字符。

由于，目前 Windows 下 tesseract 的最新稳定版是 3.5.2，于是我试图安装 "tesserocr v2.2.2 (tesseract 3.5.1)" 版本的 `.whl` 文件，却提示该 `.whl` 文件不支持当前平台，无法安装。所以，只能安装  "tesserocr v2.2.2 (tesseract 4.0.0 master)" 版本，在后文中需要配合 "tesseract 4.0.0 master" 使用。

### 1.1. 坑-1 

如果依照官方文档，只安装了 tesserocr 的 `.whl` 文件，并尝试运行如下测试代码：

```python
import tesserocr
from PIL import Image
image = Image.open('image.jpg') # 可在文末找到image.jpg
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

Traceback 告诉我们：tessdata 路径无效，无法初始化 API。

错误的原因是：stand-alone packages 虽然包含了 Windows 下所需的所有库，但并是不包含语言数据文件(language data files)。并且数据文件需要被统一放置在 `tessdata\` 文件夹中，并置于 `C:\Python36` 内。

获得数据文件有如下两种方式：

- 方法一：按照下一节的方法安装 "tesseract-ocr-w64-setup-v4.0.0-beta.1.20180608.exe"(因为要与 tesserocr-2.2.2 匹配)。然后，将 `C:\Program Files (x86)\Tesseract-OCR\` 下的 `tessdata\` 文件夹复制到 `C:\Python36\` 下即可 。
- 方法二：无需安装 tesseract ，只需克隆 [tesseract 仓库](https://github.com/tesseract-ocr/tesseract)的主分支，然后将其中的 `tessdata\` 文件夹复制到 `C:\Python36\` 中。接下来，通过 [tessdata_fast 仓库](https://github.com/tesseract-ocr/tessdata_fast)下载 `eng.traineddata` 语言文件，并放置于 `C:\Python36\tessdata\` 内即可。

可见，解决此问题的关键在于获得 tesseract 的 `tessdata\` 文件夹，并不一定要安装 tesseract ，但 tesseract 的版本一定要正确。

接下来尝试运行之前的代码：

```python
import tesserocr
from PIL import Image
image = Image.open('image.jpg') # 可在文末找到image.jpg
print(tesserocr.image_to_text(image))
```

便会输出：

```
4VC7
```

### 1.2. 坑-2

为什么要使用 [tessdata_fast 仓库](https://github.com/tesseract-ocr/tessdata_fast) 中的语言数据文件，而不使用 [tessdata_best 仓库](https://github.com/tesseract-ocr/tessdata_best) 或 [tessdata 仓库](https://github.com/tesseract-ocr/tessdata) 中的文件喃？

因为，我使用了三个仓库各自的 `eng.traineddata` 文件，来识别了文末的验证码，发现只有 [tessdata_fast 仓库](https://github.com/tesseract-ocr/tessdata_fast) 的识别结果与预期相同，另外两个都没有输出。
但对于更加简单的内容，[tessdata 仓库](https://github.com/tesseract-ocr/tessdata) 和 [tessdata_best 仓库](https://github.com/tesseract-ocr/tessdata_best) 都有输出，但前者表现更好。
另外，"tesseract-ocr-w64-setup-v4.0.0-beta.1.20180608.exe" 安装包中同样使用的是 [tessdata_fast 仓库](https://github.com/tesseract-ocr/tessdata_fast) 中的 `eng.traineddata` 文件。

## 2. 安装 tesseract

通过查看 tesseract 的 [GitHub 仓库](https://github.com/tesseract-ocr/tesseract) 的 [Wiki](https://github.com/tesseract-ocr/tesseract/wiki) 主页，可得知 [Windows 下的安装方法](https://github.com/tesseract-ocr/tesseract/wiki#windows) ，原文如下：

> Installer for Windows for Tesseract 3.05-02 and Tesseract 4.00-beta are available from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki). These include the training tools. Both 32-bit and 64-bit installers are available. 
>
> An installer for the **OLD version 3.02** is available for Windows from our [download](https://github.com/tesseract-ocr/tesseract/wiki/Downloads) page. This includes the English training data. If you want to use another language, [download the appropriate training data](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files), unpack it using [7-zip](http://www.7-zip.org/), and copy the .traineddata file into the 'tessdata' directory, probably `C:\Program Files\Tesseract-OCR\tessdata`. 
>
> To access tesseract-OCR from any location you may have to add the directory where the tesseract-OCR binaries are located to the Path variables, probably `C:\Program Files\Tesseract-OCR`. 

大意是在 [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)，可获得 Windows 安装包。
转到 UB-Mannheim/tesseract/wiki 后可见到下载链接，如下：

> The latest installers can be downloaded here: [tesseract-ocr-setup-3.05.02-20180621.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-3.05.02-20180621.exe), [tesseract-ocr-w32-setup-v4.0.0-beta.1.20180608.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v4.0.0-beta.1.20180608.exe) and [tesseract-ocr-w64-setup-v4.0.0-beta.1.20180608.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.0.0-beta.1.20180608.exe) (new, 64 bit, experimental). There are also [older versions](https://digi.bib.uni-mannheim.de/tesseract/) available. 

如果需要  [older versions](https://digi.bib.uni-mannheim.de/tesseract/) 可以去到 https://digi.bib.uni-mannheim.de/tesseract/ 下载。
这里需要安装 "tesseract-ocr-w64-setup-v4.0.0-beta.1.20180608.exe"，因为要与 tesserocr-2.2.2 匹配。

安装完成后，需要将 `C:\Program Files (x86)\Tesseract-OCR` 添加到环境变量中。

另外，tesseract 的文档位于 https://github.com/tesseract-ocr/tesseract/wiki/Documentation

### 2.1 语言包

通过 wiki 的 [Data Files](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files) 部分，我们可以下载经过训练的语言包。将下载后的语言包，直接放到`C:\Program Files (x86)\Tesseract-OCR\tessdata`  即可使用。

注意语言包有三个分支：

- <https://github.com/tesseract-ocr/tessdata_best>
- <https://github.com/tesseract-ocr/tessdata_fast>
- <https://github.com/tesseract-ocr/tessdata>

在使用语言数据时要注意区分 Tesseract 的版本，3.04 或 3.05 的语言数据需要从 [3.04 tree](https://github.com/tesseract-ocr/tessdata/tree/3.04.00) 获取。在 [Data Files](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files) 中可以了解到更多语言包的分支，及其区别。

## 3. 附件

![image](assets/image.png)





