# PDFPlumber `v0.5.12`

Plumb a PDF for detailed information about each text character, rectangle, and line. Plus: Table extraction and visual debugging.

Works best on machine-generated, rather than scanned, PDFs. Built on [`pdfminer`](https://github.com/euske/pdfminer) and [`pdfminer.six`](https://github.com/goulu/pdfminer). 

Currently [tested](tests/) on [Python 2.7, 3.1, 3.4, 3.5, and 3.6](tox.ini).

## Table of Contents

- [Installation](#installation)
- [Command line interface](#command-line-interface)
- [Python library](#python-library)
- [Visual debugging](#visual-debugging)
- [Extracting tables](#extracting-tables)
- [Demonstrations](#demonstrations)
- [Acknowledgments / Contributors](#acknowledgments--contributors)
- [Contributing](#contributing)

## 安装

```sh
pip install pdfplumber
```

如果要使用 `pdfplumber` 包中的可视化调试工具，则需要在电脑上安装 [ImageMagick](https://www.imagemagick.org/)，过程如下:

- 首先需要安装 `Wand` 和  [ImageMagick](http://www.imagemagick.org/)，详见 <http://docs.wand-py.org/en/latest/guide/install.html>

- 其次需要安装 [Ghostscript](https://www.ghostscript.com/download/gsdnld.html) 

  > You need to install Ghostscript in order to rasterize vector files (PDF, EPS, PS, etc.) with ImageMagick. IM will shell out to Ghostscript when doing these manipulations (you can see it if you use the -verbose tag in your IM invocation). You could also use Ghostscript by itself to rasterize vector files.
  >
  > -- <https://stackoverflow.com/questions/32466112/imagemagick-convert-pdf-to-jpeg-failedtoexecutecommand-gswin32c-exe-pdfdel>

## 命令行接口

### Basic example

```sh
curl "https://cdn.rawgit.com/jsvine/pdfplumber/master/examples/pdfs/background-checks.pdf" > background-checks.pdf
pdfplumber < background-checks.pdf > background-checks.csv
```

The output will be a CSV containing info about every character, line, and rectangle in the PDF.

### Options

| Argument | Description |
|----------|-------------|
|`--format [format]`| `csv` or `json`. The `json` format returns slightly more information; it includes PDF-level metadata and height/width information about each page.|
|`--pages [list of pages]`| A space-delimited, `1`-indexed list of pages or hyphenated page ranges. E.g., `1, 11-15`, which would return data for pages 1, 11, 12, 13, 14, and 15.|
|`--types [list of object types to extract]`| Choices are `char`, `anno`, `line`, `curve`, `rect`, `rect_edge`. Defaults to `char`, `anno`, `line`, `curve`, `rect`.|

## Python library

### 基本示例

```python
import pdfplumber

with pdfplumber.open("path/to/file.pdf") as pdf:
    first_page = pdf.pages[0]
    print(first_page.chars[0])
```

### 加载 PDF 文档

`pdfplumber` provides two main ways to load a PDF:

- `pdfplumber.open("path/to/file.pdf")`
- `pdfplumber.load(file_like_object)`

上述两种加载方法均会返回 `pdfplumber.PDF` 类的实例。

在加载受密码保护的 PDF 时，需传递 `password` 关键字参数，例如: `pdfplumber.open("file.pdf", password = "test")`.

### pdfplumber.PDF🛠

顶层 `pdfplumber.PDF` 类用于表示单个 PDF 文档，主要属性如下:

| Property | Description |
|----------|-------------|
|`.metadata`| A dictionary of metadata key/value pairs, drawn from the PDF's `Info` trailers. Typically includes "CreationDate," "ModDate," "Producer," et cetera.|
|`.pages`| 由`pdfplumber.Page` 实例构成的一个列表，每一页 PDF 对应一个`pdfplumber.Page` 实例 |

Note: 还有一些没有列出的属性

```python
import pdfplumber
from pprint import pprint
pdf_path = r'C:\Users\iwhal\Desktop\invoice\No_tax_rate.pdf'
with pdfplumber.open(pdf_path) as pdf:
    pprint(pdf.metadata)
    pprint(pdf.pages) 
```

输出:

```
{'CreationDate': "D:20190507091406+08'00'",
 'ModDate': "D:20190507091406+08'00'",
 'Producer': 'iText® 5.4.5 ©2000-2013 1T3XT BVBA (AGPL-version)'}
[<pdfplumber.page.Page object at 0x00000252339AE978>]
```



### pdfplumber.Page🛠

`pdfplumber` 的核心是 `pdfplumber.Page` 类，大多数的操作都将通过 `pdfplumber.Page` 来完成。

#### 主要属性

`pdfplumber.Page` 类的主要属性如下:

| Property | Description |
|----------|-------------|
|`.page_number`| `Page` 对象的页码，页码从 `1` 开始计数 |
|`.width`| 页宽 |
|`.height`| 页高 |
|`.objects` / `.chars` / `.lines` / `.rects`| 这些属性均以列表表示，列表以字典作为项，字典中的内容是被嵌入到页面中的对象。详见下方的 "[Objects](#objects)" 小节 |

Note: 还有一些没有列出的属性

```python
import pdfplumber
from pprint import pprint
# 该PDF文档仅有一页
pdf_path = r'C:\Users\iwhal\Desktop\invoice\No_tax_rate.pdf'
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        pprint(page.page_number)
        pprint(page.width)
        pprint(page.height)
```

输出:

```
1
Decimal('623.583')
Decimal('396')
```



#### 主要方法

`pdfplumber.Page` 类的主要方法如下:

| Method | Description |
|--------|-------------|
|`.crop(bounding_box)`| Returns a version of the page cropped to the bounding box, which should be expressed as 4-tuple with the values `(x0, top, x1, bottom)`. Cropped pages retain objects that fall at least partly within the bounding box. If an object falls only partly within the box, its dimensions are sliced to fit the bounding box.|
|`.within_bbox(bounding_box)`| Similar to `.crop`, but only retains objects that fall *entirely* within the bounding box.|
|`.filter(test_function)`| Returns a version of the page with only the `.objects` for which `test_function(obj)` returns `True`.|
|`.extract_text(x_tolerance=0, y_tolerance=0)` ✨| 将页面中所有的字符对象整理为单个字符串，返回值是一个字符串<br />Collates all of the page's character objects into a single string. Adds spaces where the difference between the `x1` of one character and the `x0` of the next is greater than `x_tolerance`. Adds newline characters where the difference between the `doctop` of one character and the `doctop` of the next is greater than `y_tolerance`. |
|`.extract_words(x_tolerance=0, y_tolerance=0)`| 返回所有看起来像单词的东西及其边界框的列表。<br />Returns a list of all word-looking things and their bounding boxes. Words are considered to be sequences of characters where the difference between the `x1` of one character and the `x0` of the next is less than or equal to `x_tolerance` *and* where the `doctop` of one character and the `doctop` of the next is less than or equal to `y_tolerance`. |
|`.extract_tables(table_settings)`✨| 从页面中提取表格数据。<br />Extracts tabular data from the page. For more details see "[Extracting tables](#extracting-tables)" below. |
|`.to_image(**conversion_kwargs)`| Returns an instance of the `PageImage` class. For more details, see "[Visual debugging](#visual-debugging)" below. For conversion_kwargs, see [here](http://docs.wand-py.org/en/latest/wand/image.html#wand.image.Image).|

### Objects

`pdfplumber.PDF` 和 `pdfplumber.Page` 实例支持访问四种类型的 PDF 对象。这些属性均以列表表示，列表以字典作为项，字典中的内容是被嵌入到页面中的对象。如下:

- `.chars` - 该列表中的每个字典表示一个文本字符
- `.annos` - 该列表中的每个字典表示一个 annotation-text 字符
- `.lines` - 该列表中的每个字典表示一条一维(1-dimensional)线段 
- `.rects` - 该列表中的每个字典表示一个二维(1-dimensional)矩形
- `.curves` - 该列表中的每个字典表示一系列连续的点
- `.objects` - ?文档中未解释

```python
import pdfplumber
from pprint import pprint
pdf_path = r'C:\Users\iwhal\Desktop\invoice\4pages.pdf'
with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    pprint(page.chars)
    pprint(page.annos) # 没有注释文本，所以输出为空列表
    pprint(page.lines) # 没有一维线段，所以输出为空列表
    pprint(page.rects)
    pprint(page.curves)
```

输出:

```python
[{'adv': Decimal('1.000'),
  'bottom': Decimal('42.969'),
  'doctop': Decimal('16.572'),
  'fontname': 'AdobeKaitiStd-Regular',
  'height': Decimal('26.397'),
  'object_type': 'char',
  'page_number': 1,
  'size': Decimal('26.397'),
  'text': '北',
  'top': Decimal('16.572'),
  'upright': 1,
  'width': Decimal('21.000'),
  'x0': Decimal('195.000'),
  'x1': Decimal('216.000'),
  'y0': Decimal('353.031'),
  'y1': Decimal('379.428')},
 --snip--]
[]
[]
[{'bottom': Decimal('358.256'),
  'doctop': Decimal('92.366'),
  'evenodd': False,
  'fill': True,
  'height': Decimal('265.890'),
  'linewidth': Decimal('0'),
  'non_stroking_color': None,
  'object_type': 'rect',
  'page_number': 1,
  'stroke': False,
  'stroking_color': None,
  'top': Decimal('92.366'),
  'width': Decimal('1.137'),
  'x0': Decimal('30.533'),
  'x1': Decimal('31.670'),
  'y0': Decimal('37.744'),
  'y1': Decimal('303.634')},
 --snip--]
[{'bottom': Decimal('88.172'),
  'doctop': Decimal('32.172'),
  'evenodd': False,
  'fill': False,
  'height': Decimal('56.000'),
  'linewidth': Decimal('3.078'),
  'non_stroking_color': None,
  'object_type': 'curve',
  'page_number': 1,
  'points': [(Decimal('353.899'), Decimal('60.172')),
             (Decimal('353.899'), Decimal('75.636')),
             (Decimal('334.870'), Decimal('88.172')),
             (Decimal('311.399'), Decimal('88.172')),
             (Decimal('287.927'), Decimal('88.172')),
             (Decimal('268.899'), Decimal('75.636')),
             (Decimal('268.899'), Decimal('60.172')),
             (Decimal('268.899'), Decimal('44.708')),
             (Decimal('287.927'), Decimal('32.172')),
             (Decimal('311.399'), Decimal('32.172')),
             (Decimal('334.870'), Decimal('32.172')),
             (Decimal('353.899'), Decimal('44.708')),
             (Decimal('353.899'), Decimal('60.172'))],
  'stroke': True,
  'stroking_color': None,
  'top': Decimal('32.172'),
  'width': Decimal('85.000'),
  'x0': Decimal('268.899'),
  'x1': Decimal('353.899'),
  'y0': Decimal('307.828'),
  'y1': Decimal('363.828')},
 --snip--]
```



#### `char` / `anno` properties

`.objects` / `.chars` / `.lines` / `.rects` 均是以列表表示的对象，列表以字典作为项，字典中的内容是被嵌入到页面中的对象。针对不同的对象，字典中还包含如下键值对。

| Property | Description |
|----------|-------------|
|`page_number`| y页码Page number on which this character was found. |
|`text`| E.g., "z", or "Z" or " ".|
|`fontname`| Name of the character's font face.|
|`size`| Font size.|
|`adv`| Equal to text width * the font size * scaling factor.|
|`upright`| Whether the character is upright.|
|`height`| Height of the character.|
|`width`| Width of the character.|
|`x0`| Distance of left side of character from left side of page.|
|`x1`| Distance of right side of character from left side of page.|
|`y0`| Distance of bottom of character from bottom of page.|
|`y1`| Distance of top of character from bottom of page.|
|`top`| Distance of top of character from top of page.|
|`bottom`| Distance of bottom of the character from top of page.|
|`doctop`| Distance of top of character from top of document.|
|`object_type`| "char" / "anno"|

示例

```python
import pdfplumber
from pprint import pprint
pdf_path = r'C:\Users\iwhal\Desktop\invoice\4pages.pdf'
with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    for char in page.chars:
        print(char.get('text'),end='')
```

输出:

```
四川增值税电子普通发票全国统一发票监制章国家税务局监制密码区货物或应税劳务、服    称名务规格型号单位金    额税率税    额数  量单  价合              计价税合计 (大写）名                   称 ：纳税人识别号： 地  址、电  话 ：开户行及账号 ：名                   称 ：纳税人识别号： 地  址、电  话 ：开户行及账号 ：销售方购买方（小写）备注： 人款收复核：开票人：销售方：   （章） ：发票号码 ：校  验      码  ：开票日期 ：发票代码机器编号  ：四   川499099438939曾翔中国电信股份有限公司成都分公司915101006721511356成都市成华区双林北支路473号，电话：10000中国工商银行春熙支行营业室4402209029005401812051001700111816051672018年09月10日05682 83296 72734 26623￥ 68.00*￥ 68.00陆拾捌元整帐期：2018年08月代表号码：13350064165部工号3管理员计费内部030136<>0+>>3<231*4>>5476+*-8769+*7+>80136<>0+>>3<232**+1*0136<>0+>>3<231*010>/3/6*9/50++0764-01<873193709--//49168.00项**68.00*电信服务*电信业务使用费无
```



#### `line` properties

`.objects` / `.chars` / `.lines` / `.rects` 均是以列表表示的对象，列表以字典作为项，字典中的内容是被嵌入到页面中的对象。针对不同的对象，字典中还包含如下键值对。

| Property | Description |
|----------|-------------|
|`page_number`| Page number on which this line was found.|
|`height`| Height of line.|
|`width`| Width of line.|
|`x0`| Distance of left-side extremity from left side of page.|
|`x1`| Distance of right-side extremity from left side of page.|
|`y0`| Distance of bottom extremity from bottom of page.|
|`y1`| Distance of top extremity bottom of page.|
|`top`| Distance of top of line from top of page.|
|`bottom`| Distance of bottom of the line from top of page.|
|`doctop`| Distance of top of line from top of document.|
|`linewidth`| Thickness of line.|
|`object_type`| "line"|

#### `rect` properties

`.objects` / `.chars` / `.lines` / `.rects` 均是以列表表示的对象，列表以字典作为项，字典中的内容是被嵌入到页面中的对象。针对不同的对象，字典中还包含如下键值对。

| Property | Description |
|----------|-------------|
|`page_number`| Page number on which this rectangle was found.|
|`height`| Height of rectangle.|
|`width`| Width of rectangle.|
|`x0`| Distance of left side of rectangle from left side of page.|
|`x1`| Distance of right side of rectangle from left side of page.|
|`y0`| Distance of bottom of rectangle from bottom of page.|
|`y1`| Distance of top of rectangle from bottom of page.|
|`top`| Distance of top of rectangle from top of page.|
|`bottom`| Distance of bottom of the rectangle from top of page.|
|`doctop`| Distance of top of rectangle from top of document.|
|`linewidth`| Thickness of line.|
|`object_type`| "rect"|

#### `curve` properties

`.objects` / `.chars` / `.lines` / `.rects` 均是以列表表示的对象，列表以字典作为项，字典中的内容是被嵌入到页面中的对象。针对不同的对象，字典中还包含如下键值对。

| Property | Description |
|----------|-------------|
|`page_number`| Page number on which this curve was found.|
|`points`| Points — as a list of `(x, top)` tuples — describing the curve.|
|`height`| Height of curve's bounding box.|
|`width`| Width of curve's bounding box.|
|`x0`| Distance of curve's left-most point from left side of page.|
|`x1`| Distance of curve's right-most point from left side of the page.|
|`y0`| Distance of curve's lowest point from bottom of page.|
|`y1`| Distance of curve's highest point from bottom of page.|
|`top`| Distance of curve's highest point from top of page.|
|`bottom`| Distance of curve's lowest point from top of page.|
|`doctop`| Distance of curve's highest point from top of document.|
|`linewidth`| Thickness of line.|
|`object_type`| "curve"|

Additionally, both `pdfplumber.PDF` and `pdfplumber.Page` provide access to two derived lists of objects: `.rect_edges` (which decomposes each rectangle into its four lines) and `.edges` (which combines `.rect_edges` with `.lines`). 

## 可视化调试

### `.to_image()`

使用 `my_page.to_image()` 方法可将任何页面(包括裁剪后的页面)转换为 `PageImage` 对象。关键字参数 `resolution={integer}` 用于控制分辨率，也就是输出图片的大小，默认值是 72

```python
im = my_pdf.pages[0].to_image(resolution=150)
```

`PageImage` 对象可与 IPython/Jupyter notebooks 协作，会自动呈现 cell 输出，例如:

![在Jupyter中进行可视化调试](pdfplumber.assets/visual-debugging-in-jupyter.png)

### `PageImage` 对象

#### 基本方法

| Method | Description |
|--------|-------------|
|`im.reset()`| Clears anything you've drawn so far.|
|`im.copy()`| Copies the image to a new `PageImage` object.|
|`im.save(path_or_fileobject, format="PNG")`| Saves the annotated image.|

#### 绘制方法

你可以向绘制方法传递坐标(*coordinates*)或任何 `pdfplumber` PDF 对象(e.g., char, line, rect)

| Single-object method | Bulk method | Description |
|----------------------|-------------|-------------|
|`im.draw_line(line, stroke={color}, stroke_width=1)`| `im.draw_lines(list_of_lines, **kwargs)`| Draws a line from a `line`, `curve`, or a 2-tuple of 2-tuples (e.g., `((x, y), (x, y))`).|
|`im.draw_vline(location, stroke={color}, stroke_width=1)`| `im.draw_vlines(list_of_locations, **kwargs)`| Draws a vertical line at the x-coordinate indicated by `location`.|
|`im.draw_hline(location, stroke={color}, stroke_width=1)`| `im.draw_hlines(list_of_locations, **kwargs)`| Draws a horizontal line at the y-coordinate indicated by `location`.|
|`im.draw_rect(bbox_or_obj, fill={color}, stroke={color}, stroke_width=1)`| `im.draw_rects(list_of_rects, **kwargs)`| Draws a rectangle from a `rect`, `char`, etc., or 4-tuple bounding box.|
|`im.draw_circle(center_or_obj, radius=5, fill={color}, stroke={color})`| `im.draw_circles(list_of_circles, **kwargs)`| Draws a circle at `(x, y)` coordinate or at the center of a `char`, `rect`, etc.|

Note: The methods above are built on Pillow's [`ImageDraw` methods](http://pillow.readthedocs.io/en/latest/reference/ImageDraw.html), but the parameters have been tweaked for consistency with SVG's `fill`/`stroke`/`stroke_width` nomenclature.

### Troubleshooting ImageMagick on Debian-based systems

If you're using `pdfplumber` on a Debian-based system and encounter a `PolicyError`, you may be able to fix it by changing the following line in `/etc/ImageMagick-6/policy.xml` from this:

```xml
<policy domain="coder" rights="none" pattern="PDF" />
```

... to this:

```xml
<policy domain="coder" rights="read|write" pattern="PDF" />
```

(More details about `policy.xml` [available here](https://imagemagick.org/script/security-policy.php).)

## 提取表格

`pdfplumber`'s approach to table detection borrows heavily from [Anssi Nurminen's master's thesis](http://dspace.cc.tut.fi/dpub/bitstream/handle/123456789/21520/Nurminen.pdf?sequence=3), and is inspired by [Tabula](https://github.com/tabulapdf/tabula-extractor/issues/16). It works like this:

1. For any given PDF page, find the lines that are (a) explicitly defined and/or (b) implied by the alignment of words on the page.
2. Merge overlapping, or nearly-overlapping, lines.
3. Find the intersections of all those lines.
4. Find the most granular set of rectangles (i.e., cells) that use these intersections as their vertices.
5. Group contiguous cells into tables. 



### 提取表格的方法

可以在 `pdfplumber.Page` 对象上调用以下方法来提取表格:

| Method | Description |
|--------|-------------|
|`.find_tables(table_settings={})`|Returns a list of `Table` objects. The `Table` object provides access to the `.cells`, `.rows`, and `.bbox` properties, as well as the `.extract(x_tolerance=3, y_tolerance=3)` method.|
|`.extract_tables(table_settings={})`|Returns the text extracted from *all* tables found on the page, represented as a list of lists of lists, with the structure `table -> row -> cell`.|
|`.extract_table(table_settings={})`|Returns the text extracted from the *largest* table on the page, represented as a list of lists, with the structure `row -> cell`. (If multiple tables have the same size — as measured by the number of cells — this method returns the table closest to the top of the page.)|
|`.debug_tablefinder(table_settings={})`|Returns an instance of the `TableFinder` class, with access to the `.edges`, `.intersections`, `.cells`, and `.tables` properties.|

For example:

```python
pdf = pdfplumber.open("path/to/my.pdf")
page = pdf.pages[0]
page.extract_table()
```

[Click here for a more detailed example.](examples/notebooks/extract-table-ca-warn-report.ipynb)

### Table-extraction settings

By default, `extract_tables` uses the page's vertical and horizontal lines (or rectangle edges) as cell-separators. But the method is highly customizable via the `table_settings` argument. The possible settings, and their defaults:

```python
{
    "vertical_strategy": "lines", 
    "horizontal_strategy": "lines",
    "explicit_vertical_lines": [],
    "explicit_horizontal_lines": [],
    "snap_tolerance": 3,
    "join_tolerance": 3,
    "edge_min_length": 3,
    "min_words_vertical": 3,
    "min_words_horizontal": 1,
    "keep_blank_chars": False,
    "text_tolerance": 3,
    "text_x_tolerance": None,
    "text_y_tolerance": None,
    "intersection_tolerance": 3,
    "intersection_x_tolerance": None,
    "intersection_y_tolerance": None,
}
```

| Setting | Description |
|---------|-------------|
|`"vertical_strategy"`| Either `"lines"`, `"lines_strict"`, `"text"`, or `"explicit"`. See explanation below.|
|`"horizontal_strategy"`| Either `"lines"`, `"lines_strict"`, `"text"`, or `"explicit"`. See explanation below.|
|`"explicit_vertical_lines"`| A list of vertical lines that explicitly demarcate cells in the table. Can be used in combination with any of the strategies above. Items in the list should be either numbers — indicating the `x` coordinate of a line the full height of the page — or a dictionary describing the line, with at least the following keys: `x`, `top`, `bottom`. |
|`"explicit_horizontal_lines"`| A list of vertical lines that explicitly demarcate cells in the table. Can be used in combination with any of the strategies above. Items in the list should be either numbers — indicating the `y` coordinate of a line the full height of the page — or a dictionary describing the line, with at least the following keys: `top`, `x0`, `x1`.|
|`"snap_tolerance"`| Parallel lines within `snap_tolerance` pixels will be "snapped" to the same horizontal or vertical position.|
|`"join_tolerance"`| Line segments on the same infinite line, and whose ends are within `join_tolerance` of one another, will be "joined" into a single line segment.|
|`"edge_min_length"`| Edges shorter than `edge_min_length` will be discarded before attempting to reconstruct the table.|
|`"min_words_vertical"`| When using `"vertical_strategy": "text"`, at least `min_words_vertical` words must share the same alignment.|
|`"min_words_horizontal"`| When using `"horizontal_strategy": "text"`, at least `min_words_horizontal` words must share the same alignment.|
|`"keep_blank_chars"`| When using the `text` strategy, consider `" "` chars to be *parts* of words and not word-separators.|
|`"text_tolerance"`, `"text_x_tolerance"`, `"text_y_tolerance"`| When the `text` strategy searches for words, it will expect the individual letters in each word to be no more than `text_tolerance` pixels apart.|
|`"intersection_tolerance"`, `"intersection_x_tolerance"`, `"intersection_y_tolerance"`| When combining edges into cells, orthogonal edges must be within `intersection_tolerance` pixels to be considered intersecting.|

### Table-extraction strategies

Both `vertical_strategy` and `horizontal_strategy` accept the following options:

| Strategy | Description |
|----------|-------------|
| `"lines"` | Use the page's graphical lines — including the sides of rectangle objects — as the borders of potential table-cells. |
| `"lines_strict"` | Use the page's graphical lines — but *not* the sides of rectangle objects — as the borders of potential table-cells. |
| `"text"` | For `vertical_strategy`: Deduce the (imaginary) lines that connect the left, right, or center of words on the page, and use those lines as the borders of potential table-cells. For `horizontal_strategy`, the same but using the tops of words. |
| `"explicit"` | Only use the lines explicitly defined in `explicit_vertical_lines` / `explicit_horizontal_lines`. |

### Notes

- Often it's helpful to crop a page — `Page.crop(bounding_box)` — before trying to extract the table.

- Table extraction for `pdfplumber` was radically redesigned for `v0.5.0`, and introduced breaking changes.


## Demonstrations

- [Using `extract_table` on a California Worker Adjustment and Retraining Notification (WARN) report](examples/notebooks/extract-table-ca-warn-report.ipynb). Demonstrates basic visual debugging and table extraction.
- [Using `extract_table` on the FBI's National Instant Criminal Background Check System PDFs](examples/notebooks/extract-table-nics.ipynb). Demonstrates how to use visual debugging to find optimal table extraction settings. Also demonstrates `Page.crop(...)` and `Page.extract_text(...).`
- [Inspecting and visualizing `curve` objects](examples/notebooks/ag-energy-roundup-curves.ipynb).
- [Extracting fixed-width data from a San Jose PD firearm search report](examples/notebooks/san-jose-pd-firearm-report.ipynb), an example of using `Page.extract_text(...)`.

## Acknowledgments / Contributors

Many thanks to the following users who've contributed ideas, features, and fixes:

- [Jacob Fenton](https://github.com/jsfenfen)
- [Dan Nguyen](https://github.com/dannguyen)
- [Jeff Barrera](https://github.com/jeffbarrera)
- [Bob Lannon](https://github.com/boblannon)
- [Dustin Tindall](https://github.com/dustindall)
- [@yevgnen](https://github.com/Yevgnen)
- [@meldonization](https://github.com/meldonization)
- [Oisín Moran](https://github.com/OisinMoran)

## Contributing

Pull requests are welcome, but please submit an issue (or email jsvine@gmail.com) before submitting one, as the library is in active development. The current development branch is `v0.6.0`.
