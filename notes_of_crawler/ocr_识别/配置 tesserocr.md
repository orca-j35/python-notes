# 配置 tesserocr

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 环境: Win10_64 | Python 3.7.2

## Tesserocr 

tesserocr 相关资源:

- GitHub: https://github.com/sirfz/tesserocr
- PyPI: https://pypi.org/project/tesserocr/

### 安装 Tesserocr

[tesserocr](https://github.com/sirfz/tesserocr) 是 Python 下的一个 OCR 识别库，其本质是对 [tesseract](https://github.com/tesseract-ocr/tesseract) 做了一层 Python API 封装。通过 tesserocr 的 [PyPI页面](https://pypi.org/project/tesserocr/)，可以找到该项目的 [GitHub 仓库](https://github.com/sirfz/tesserocr) 。在仓库的 `README.rst` 中介绍了 Windows 平台的安装方式，原文如下：

> Windows:
>
> The proposed downloads consist of stand-alone packages containing all the Windows libraries needed for execution. This means that no additional installation of tesseract is required on your system.
>
> - Conda
>
>   You can use the channel [simonflueckiger](https://anaconda.org/simonflueckiger/tesserocr) to install from Conda:
>
>   ```shell
>   > conda install -c simonflueckiger tesserocr
>   ```
>
>   or to get **tesserocr** compiled with **tesseract 4.0.0**:
>
>   ```shell
>   > conda install -c simonflueckiger/label/tesseract-4.0.0-master tesserocr
>   ```
>
> - pip
>
>   Download the wheel file corresponding to your Windows platform and Python installation from [simonflueckiger/tesserocr-windows_build/releases](https://github.com/simonflueckiger/tesserocr-windows_build/releases) and install them via:
>
>   ```shell
>   > pip install <package_name>.whl
>   ```

上述文档建议我们下载 stand-alone packages，因为其中包含了在 Windows 下执行 tesserocr 时，需要的所有库。也就是说，如果通过 stand-alone packages 安装 tesserocr ，便无需再额外安装 tesseract 。因此，务必通过上述两种方式来安装 tesserocr，不要直接使用 `pip3 install tesserocr` 进行安装。我曾在 Windows 上尝试通过 `pip3 install tesserocr` 进行安装，结果是提示安装失败——[据说这种方式只能用于 Linux](https://blog.csdn.net/coolcooljob/article/details/80385711)，但我没有仔细研究过。

这里建议通过 `conda` 安装(后文默认采用这种安装方法)，直接执行以下命令即可：

```shell
> conda install -c simonflueckiger/label/tesseract-4.0.0-master tesserocr
```

在选择 tesserocr 的版本时，需要和 tesseract 的版本相匹配。比如，当使用 [tesserocr v2.4.0 (tesseract 4.0.0)](https://github.com/simonflueckiger/tesserocr-windows_build/releases/tag/tesserocr-v2.4.0-tesseract-4.0.0) 时，就必需使用 tesseract-v4.0 中的 `/tessdata/` 目录。如果 tesserocr 和 tesseract 版本不匹配，识别结果中会出现非预期字符。例如，若是将 "tesserocr v2.4.0 (tesseract 4.0.0)" 与 "tesseract 3.5.2" 搭配使用，结果中便会出现非预期字符。

### 缺少 tessdata 数据

当我们按照上一小节的方法安装 tesserocr 后，会发现 tesserocr 并不能正常工作。例如，当我们尝试运行以下代码时，会抛出异常:

```python
import tesserocr
from PIL import Image
image = Image.open('image.png') # image.png 见附件
print(image)
print(tesserocr.image_to_text(image, lang='eng'))
'''Out:
(spider) C:\Users\iwhal\Desktop\PyTest>C:/ProgramData/Anaconda3/envs/spider/python.exe c:/Users/iwhal/Desktop/PyTest/learn.py
<PIL.PngImagePlugin.PngImageFile image mode=RGBA size=281x118 at 0x178B0B23A20>
Traceback (most recent call last):
  File "c:/Users/iwhal/Desktop/PyTest/learn.py", line 5, in <module>
    print(tesserocr.image_to_text(image))
  File "tesserocr.pyx", line 2443, in tesserocr._tesserocr.image_to_text
RuntimeError: Failed to init API, possibly an invalid tessdata path: C:\ProgramData\Anaconda3\envs\spider\/tessdata/
'''
```

Traceback 告诉我们：tessdata 路径无效，无法初始化 API。原因是 stand-alone packages 中虽包含了 Windows 下需要的所有库，但并是不包含语言数据文件(*language* *data* *files*)。数据文件需要被统一放置在 `tessdata\` 文件夹中，并置于 `~\Anaconda3\envs\spider\` 内(注，当前 conda 环境名为 spider)。

获得数据文件的方式有如下两种：

- 方法一: 安装 [tesseract-ocr-w64-setup-v4.0.0.20181030.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.0.0.20181030.exe) —— 与之前安装的 [tesserocr v2.4.0 (tesseract 4.0.0)](https://github.com/simonflueckiger/tesserocr-windows_build/releases/tag/tesserocr-v2.4.0-tesseract-4.0.0) 相匹配。然后，将 `C:\Program Files\Tesseract-OCR\` 下的 `tessdata\` 文件夹复制到 `~\Anaconda3\envs\spider\` 下即可(注，当前 conda 环境名为 spider)。
- 方法二：获取 [tesseract 仓库](https://github.com/tesseract-ocr/tesseract) 的主分支，然后将其中的 `tessdata\` 文件夹复制到 `~\Anaconda3\envs\spider\` 下(注，当前 conda 环境名为 spider)。相较于方法一，方法二的 `tessdata\` 目录中缺少 `.traineddata` 语言文件(如，`eng.traineddata`)，需要在语言数据仓库中手动下载，详见下文﹝语言数据文件﹞小节。在 [tesseract 仓库](https://github.com/tesseract-ocr/tesseract) 的 `VERSION` 文件中可查看 tesseract 当前分支的版本号，最好与 tesserocr 要求的版本号对应。

获得语言数据文件的关键在于得到 tesseract 的 `tessdata\` 目录，且其中包含正确的文件，并不一定非要安装 tesseract。

接下来尝试运行之前的代码：

```python
import tesserocr
from PIL import Image
image = Image.open('image.png') # image.png 见附件
print(image)
print(tesserocr.image_to_text(image, lang='eng'))
'''Out:
<PIL.PngImagePlugin.PngImageFile image mode=RGBA size=281x118 at 0x2A08CB46860>
4VC7
'''
```

另外，`tesserocr.file_to_text()` 可直接接收图片对象。

### 选择语言数据的仓库

tesseract 有三个独立的仓库用于存放语言包，其区别大致如下(详见 [GitHub-Wiki](https://github.com/tesseract-ocr/tesseract/wiki) 的 [Data Files](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files) 部分)：

> Most users will want **tessdata_fast** and that is what will be shipped as part of Linux distributions. **tessdata_best** is for people willing to trade a lot of speed for slightly better accuracy. It is also better for certain retraining scenarios for advanced users.
>
> The third set in **tessdata** is for the legacy recognizer. The 4.00 files from November 2016 have both LSTM and legacy models.

补充: 我曾分别使用三个仓库中的 `eng.traineddata` 文件来识别了文末的验证码。发现只有 [tessdata_fast 仓库](https://github.com/tesseract-ocr/tessdata_fast) 的识别结果与预期相同，另外两个都没有输出。但对于更加简单的内容，[tessdata 仓库](https://github.com/tesseract-ocr/tessdata) 和 [tessdata_best 仓库](https://github.com/tesseract-ocr/tessdata_best) 都有输出，但前者表现更好。[tesseract-ocr-w64-setup-v4.0.0.20181030.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.0.0.20181030.exe) 安装包中也使用的是 [tessdata_fast](https://github.com/tesseract-ocr/tessdata_fast) 中的 `eng.traineddata` 文件。

## Tesseract

tesseract 相关资源:

- GitHub: https://github.com/tesseract-ocr/tesseract
- Wiki: https://github.com/tesseract-ocr/tesseract/wiki
  - 在 Wiki 主页中有安装指导
- Docs: https://github.com/tesseract-ocr/tesseract/wiki/Documentation
- 语言数据文件 - Wiki: https://github.com/tesseract-ocr/tesseract/wiki/Data-Files
- Tesseract for Windows at UB Mannheim: https://github.com/UB-Mannheim/tesseract/wiki
  - 历史版本: https://digi.bib.uni-mannheim.de/tesseract/
  - GitHub: https://github.com/UB-Mannheim/tesseract

### 安装

通过 tesseract 的 [GitHub-Wiki](https://github.com/tesseract-ocr/tesseract/wiki) 可知 [Windows 下的安装方法](https://github.com/tesseract-ocr/tesseract/wiki#windows)，原文如下：

> Installer for Windows for Tesseract 3.05-02 and Tesseract 4.00-beta are available from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki). These include the training tools. Both 32-bit and 64-bit installers are available.
>
> An installer for the **OLD version 3.02** is available for Windows from our [download](https://github.com/tesseract-ocr/tesseract/wiki/Downloads) page. This includes the English training data. If you want to use another language, [download the appropriate training data](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files), unpack it using [7-zip](http://www.7-zip.org/), and copy the .traineddata file into the 'tessdata' directory, probably `C:\Program Files\Tesseract-OCR\tessdata`.
>
> To access tesseract-OCR from any location you may have to add the directory where the tesseract-OCR binaries are located to the Path variables, probably `C:\Program Files\Tesseract-OCR`.
>
> Experts can also get binaries build with Visual Studio from the build artifacts of the [Appveyor Continuous Integration](https://ci.appveyor.com/project/zdenop/tesseract/history).

第一段告诉我们，可以在 [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) 得 Windows 安装包，[Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) 中的原文如下：

> The latest installers can be downloaded here: [tesseract-ocr-setup-3.05.02-20180621.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-3.05.02-20180621.exe), [tesseract-ocr-w32-setup-v4.0.0.20181030.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v4.0.0.20181030.exe) (32 bit) and [tesseract-ocr-w64-setup-v4.0.0.20181030.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.0.0.20181030.exe) (64 bit). There are also [older versions](https://digi.bib.uni-mannheim.de/tesseract/) available.

这里告诉我们最新的稳定版有:

- [tesseract-ocr-setup-3.05.02-20180621.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-3.05.02-20180621.exe), 
- [tesseract-ocr-w32-setup-v4.0.0.20181030.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v4.0.0.20181030.exe) (32 bit) 
- [tesseract-ocr-w64-setup-v4.0.0.20181030.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.0.0.20181030.exe) (64 bit)

另外，如果需要历史版本，可以去 [older versions](https://digi.bib.uni-mannheim.de/tesseract/) 下载。

在选择 tesseract 的版本时，需要和 tesserocr 的版本相匹配。比如，当使用 [tesserocr v2.4.0 (tesseract 4.0.0)](https://github.com/simonflueckiger/tesserocr-windows_build/releases/tag/tesserocr-v2.4.0-tesseract-4.0.0) 时，就必需使用 tesseract-v4.0 中的 `/tessdata/` 目录。

在安装过程中注意勾选 `Additional script data` 和 `Additional language data` 组件。

如果需要在命令行中使用 tesseract，则需要将安装目录添加到环境变量中(如，`C:\Program Files\Tesseract-OCR`)。在 power shell 中的使用效果如下(image.png 见附件):

```powershell
PS C:\Users\iwhal\Desktop\PyTest> tesseract image.png result -l eng
Tesseract Open Source OCR Engine v4.0.0.20181030 with Leptonica
Warning: Invalid resolution 0 dpi. Using 70 instead.
Estimating resolution as 609
PS C:\Users\iwhal\Desktop\PyTest> cat result.txt


4VC7





```

### 语言数据文件

在 tesseract [GitHub-Wiki](https://github.com/tesseract-ocr/tesseract/wiki) 的 [Data Files](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files) 章节，我们可以下载经过训练的语言包。将语言包直接放到 `C:\Program Files (x86)\Tesseract-OCR\tessdata` 目录下即可使用。

有三个独立的仓库用于存放语言包:

> Most users will want **tessdata_fast** and that is what will be shipped as part of Linux distributions. **tessdata_best** is for people willing to trade a lot of speed for slightly better accuracy. It is also better for certain retraining scenarios for advanced users.
>
> The third set in **tessdata** is for the legacy recognizer. The 4.00 files from November 2016 have both LSTM and legacy models.

- https://github.com/tesseract-ocr/tessdata_best
- https://github.com/tesseract-ocr/tessdata_fast
- https://github.com/tesseract-ocr/tessdata

在使用语言数据时要注意区分 tesseract 的版本，3.04 或 3.05 的语言数据需要从 [3.04 tree](https://github.com/tesseract-ocr/tessdata/tree/3.04.00) 获取。在 [Data Files](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files) 中可以了解到更多语言包的分支，及其区别。

### 特殊数据文件

通过 tesseract 的 [GitHub-Wiki](https://github.com/tesseract-ocr/tesseract/wiki) 的 [Data Files](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files) 部分，我们可以下载经过训练的特殊数据文件。将下载后的数据文件，直接放到 `C:\Program Files (x86)\Tesseract-OCR\tessdata` 目录下即可使用。

| Lang Code | Description                      | 4.0/3.0x traineddata                                         |
| --------- | -------------------------------- | ------------------------------------------------------------ |
| osd       | Orientation and script detection | [osd.traineddata](https://github.com/tesseract-ocr/tessdata/raw/3.04.00/osd.traineddata) |
| equ       | Math / equation detection        | [equ.traineddata](https://github.com/tesseract-ocr/tessdata/raw/3.04.00/equ.traineddata) |

**Note**: These two data files are compatible with older versions of Tesseract. `osd` is compatible with version 3.01 and up, and `equ` is compatible with version 3.02 and up.

## Pillow

> tesserocr is designed to be [`Pillow`](http://python-pillow.github.io/)-friendly but can also be used with image files instead.

在使用 tesserocr 时，最好一并安装 [`Pillow`](http://python-pillow.github.io/) 库。

## 附件

![image](配置 Tesserocr.assets/image.png)





