## Qt Designer 的使用

> 本节内容主要参考了 http://pyqt.sourceforge.net/Docs/PyQt5/designer.html
>
> 代码：C:\learn_PyQt\use_QtDesigner_code

Qt Designer 是用于设计和构建图形用户界面的 Qt 工具。它允许你使用屏幕中的窗体和简单的拖放界面，来设计widgets / dialogs 或者完整的 main windows 。该工具可以对设计进行预览，以确保符合设计者的预期。完全可以在向用户展示设计原型后，再编写需要实现程序的代码。

Qt Designer 使用 XML 格式 `.ui` 文件存储设计，但不会生成任何代码。Qt 内含的 `uic` utility 用于生成创建用户界面的 C++ 代码。Qt 还包含 `QUiLoader` 类，该类允许应用程序加载 `.ui` 文件，并动态创建相应的用户界面。

PyQt5 并没有打包 `QUiLoader` 类，而是包含了 [`uic`](http://pyqt.sourceforge.net/Docs/PyQt5/uic.html#PyQt5-uic) Python 模块。类似于 `QUiLoader` 类，`uic` 模块可以加载 `.ui` 文件，并动态创建用户界面。另外，就像 **uic** utility 一样，该模块可以为需要创建的用户界面生成相应的 Python 代码。PyQt5 的 **pyuic5** utility 是 [`uic`](http://pyqt.sourceforge.net/Docs/PyQt5/uic.html#PyQt5-uic) 模块的命令行界面。在接下来的章节中，会详细描述这两种功能的使用方法。

### 使用 pyuic5 生成的代码

为了便于理解，我们会先用 pyuic5 生成一段 python 代码。
然后，再演示如何使用这些由 pyuic5 生成的代码。

#### a. 生成代码

1. 在 Qt Designer 中新建一个 Dialog 窗体，并将其保存为 `imagedialog.ui`。
   注意：其中 [`QDialog`](http://pyqt.sourceforge.net/Docs/PyQt5/api/QtWidgets/qdialog.html#PyQt5-QtWidgets-QDialog) 对象的名称是 `ImageDialog` 。

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <ui version="4.0">
    <class>ImageDialog</class>
    <widget class="QDialog" name="ImageDialog">
     <property name="geometry">
      <rect>
       <x>0</x>
       <y>0</y>
       <width>400</width>
       <height>300</height>
      </rect>
     </property>
     <property name="windowTitle">
      <string>Dialog</string>
     </property>
    </widget>
    <resources/>
    <connections/>
   </ui>
   ```

   注意：为了使整个演示过程更加直观，这里无需向 Dialog 窗体添加任何控件；也是出于同样的原因，没有选择新建 Main Windows 窗体（这会使得代码更长），但这些并不影响对整个过程的理解。

2. 使用 pyuic5 将 `imagedialog.ui` 编译为 `ui_imagedialog.ui`。代码如下：

   ```python
   from PyQt5 import QtCore, QtGui, QtWidgets

   class Ui_ImageDialog(object):
       def setupUi(self, ImageDialog): #ImageDialog是QDialog的实例
           ImageDialog.setObjectName("ImageDialog")
           ImageDialog.resize(400, 300)

           self.retranslateUi(ImageDialog) #调用翻译方法
           QtCore.QMetaObject.connectSlotsByName(ImageDialog) #用于连接信号和插槽

       def retranslateUi(self, ImageDialog):#该方法用于翻译
           _translate = QtCore.QCoreApplication.translate
           ImageDialog.setWindowTitle(_translate("ImageDialog", 		"Dialog"))
           
   if __name__ == "__main__":
       import sys
       app = QtWidgets.QApplication(sys.argv)
       ImageDialog = QtWidgets.QDialog() #创建QDialog实例
       ui = Ui_ImageDialog() #创建Ui_ImageDialog实例
       ui.setupUi(ImageDialog) #设置窗体
       ImageDialog.show() #显示窗体
       sys.exit(app.exec_())
   ```

#### b. 使用代码

以上由 pyuic5 生成的代码与 Qt's `uic` utility 生成的代码具有相同的结构，并且可以以相同的方式使用。

代码包含由 Python `object` type 派生的一个类。类名称由 Designer 中设置的顶层对象名称加上 `Ui_` 前缀构成。比如：在 `imagedialog.ui` 中，顶层对象的名称是 `ImageDialog` ，因此类名为 `Ui_ImageDialog` 。( 在 C++ 版本中该类将会在 `Ui` 命名空间中被定义 )。我们将这样的类称为 *form class* 。

*form class* 中会包含一个叫做 `setupUi()` 的方法。该方法需要一个 widget 参数，并在该 widget 中创建用户界面。形参的类型[^1]在 Designer 中被设置 (typically [`QDialog`](http://pyqt.sourceforge.net/Docs/PyQt5/api/QtWidgets/qdialog.html#PyQt5-QtWidgets-QDialog), [`QWidget`](http://pyqt.sourceforge.net/Docs/PyQt5/api/QtWidgets/qwidget.html#PyQt5-QtWidgets-QWidget) or [`QMainWindow`](http://pyqt.sourceforge.net/Docs/PyQt5/api/QtWidgets/qmainwindow.html#PyQt5-QtWidgets-QMainWindow))。我们将这种类型称作 *Qt base class* 。

> [^1]: 这句话翻译自官方文档 [Using the Generated Code](http://pyqt.sourceforge.net/Docs/PyQt5/designer.html#using-the-generated-code) ，但是在 python 无需设置形参的类型。因此我怀疑这句话的原文来自 Qt C++ 文档，因为 C++ 需要设置参数类型。

在下面的示例中，我们将利用 `ui_imagedialog.py` 演示多种代码的使用方式：
注意：For a full description see the [Qt Designer Manual](https://doc.qt.io/qt-5/designer-using-a-ui-file.html#reacting-to-language-changes) in the Qt Documentation.

##### 1.直接使用法

在包含 `ui_imagedialog.py` 的目录下，创建 `direct_approch.py` ，并写入以下用于创建对话框的代码：

```
import sys
from PyQt5.QtWidgets import QApplication, QDialog
from ui_imagedialog import Ui_ImageDialog

app = QApplication(sys.argv)
window = QDialog()
ui = Ui_ImageDialog()
ui.setupUi(window)

window.show()
sys.exit(app.exec_())
```

##### 2.单继承方法

首先需要创建 [`QDialog`](http://pyqt.sourceforge.net/Docs/PyQt5/api/QtWidgets/qdialog.html#PyQt5-QtWidgets-QDialog) 的子类，然后在 `__init__()` 方法中设置用户界面。
在包含 `ui_imagedialog.py` 的目录下，创建 `single_inheritance_approach.py` ，并写入以下用于创建对话框的代码：

```python
import sys
from PyQt5.QtWidgets import QApplication, QDialog
from ui_imagedialog import Ui_ImageDialog


class ImageDialog(QDialog):
    def __init__(self):
        super(ImageDialog, self).__init__()
    
        # Set up the user interface from Designer.
        self.ui = Ui_ImageDialog()
        self.ui.setupUi(self)
    
        # Make some local modifications.
    
        # Connect up the buttons.


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_dialog = ImageDialog()
    my_dialog.show()
    sys.exit(app.exec())
```

##### 3.多继承方法

在包含 `ui_imagedialog.py` 的目录下，创建 `multiple_inheritance_approach.py` ，并写入以下用于创建对话框的代码：

```python
import sys
from PyQt5.QtWidgets import QApplication, QDialog
from ui_imagedialog import Ui_ImageDialog


class ImageDialog(QDialog, Ui_ImageDialog):
    def __init__(self):
        super(ImageDialog, self).__init__()
    
        # Set up the user interface from Designer.
        self.setupUi(self)
    
        # Make some local modifications.
    
        # Connect up the buttons.


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_dialog = ImageDialog()
    my_dialog.show()
    sys.exit(app.exec())
```

#### c. 关于 parent

有些代码中会看到 `parent=None` ，`parent` 用于表明窗体间的父子关系。比如：

```
import sys
from PyQt5.QtWidgets import QApplication, QDialog
from ui_imagedialog import Ui_ImageDialog


class ImageDialog(QDialog, Ui_ImageDialog):
    def __init__(self, parent=None):
        super(ImageDialog, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_dialog = ImageDialog()
    my_dialog.show()
    sys.exit(app.exec())
```

`parent=None` 的 QWidget 类被认为是最上层的窗体。
但是 `parent` 的默认值是 `None` ，所以不用显示的写出。

```
""" QDialog(parent: QWidget = None, flags: Union[Qt.WindowFlags, Qt.WindowType] = Qt.WindowFlags()) """
```
