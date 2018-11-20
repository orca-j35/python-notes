# Window and Dialog Widgets

[TOC]

https://doc.qt.io/qt-5/application-windows.html

## 窗口

A [widget](https://doc.qt.io/qt-5/widgets-tutorial.html) that is not embedded嵌入 in a parent widget is called a **window**. (Usually, windows have a frame框架 and a title bar, although it is also possible to create windows without such decoration装饰 using suitable相应的 window flags). In Qt, [QMainWindow](https://doc.qt.io/qt-5/qmainwindow.html) and the various subclasses of [QDialog](https://doc.qt.io/qt-5/qdialog.html) are the most common常见的 window types.

In applications, windows provide the screen space upon which the user interface is built. Windows separate分隔 applications visually from each other and usually provide a window decoration that allows the user to resize and position the applications according to his preferences. Windows are typically integrated into the desktop environment and to some degree managed by the window management system that the desktop environment provides. For instance, selected windows of an application are represented in the task bar.