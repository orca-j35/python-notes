知识背景：我有一点 C 的知识，也学习过 Python3。我没有 C++ 背景，所以在一些术语我沿用了 Python的，可能对于 C++ 来说比较外行。

# Qt vs PyQt

**为什么要对比代码？**

因为在 [PyQt 5.9 Reference Guide](http://pyqt.sourceforge.net/Docs/PyQt5/index.html#) 中并没有给出详细的参考文档，仅仅是将相关内容指向了 Qt C++ 文档的 URL。比如像下面这样一段内容：

> *class* [PyQt5.QtWidgets](http://pyqt.sourceforge.net/Docs/PyQt5/QtWidgets.html#PyQt5-QtWidgets).QApplication
>
> The C++ documentation can be found [here](https://doc.qt.io/qt-5/qapplication.html).

其实 PyQt 和 Qt 的使用方法是极其类似的，所以我们在此简要对比两者的异同，试图建立起 Qt 和 PyQt 在使用方式上的映射关系。

> 知识背景：我并没有 C++ 背景，只用 C 写过一些单片机程序，所以对于 C++ 都是边看边学。一些术语会沿用 Python 的表述方式，对于 C++ 可能会不太严谨。个人能力有限，望大家纠正。

## 一个显示简单的Widget

### Qt 的 C++ 代码

```c++
#include <QApplication> //导入QApplication类
#include <QLabel> //导入QLabel类

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    //为QApplication类创建一个名为app的实例

    QLabel label("Hello, world");
    //创建QLabel对象，并为构造函数赋值。
    label.show();
    //调用label实例的show()方法，将其显示出来

    return app.exec();
    //在main()函数的最后调用app.exec()，开启事件循环。
}
```

GUI 程序属于 `QApplication` 类，非 GUI 程序属于`QCoreApplication` 类。
`QApplication` 类其实是 `QCoreApplication` 的子类。

对于 Qt 程序而言，`main()` 函数一般以创建 application 对象开始，后面才是实际业务的代码。这个对象用于管理 Qt 程序的生命周期，开启事件循环，这一切都是必不可少的。

在main()函数的最后调用`app.exec()`，开启事件循环。我们现在可以简单地将事件循环理解成一段无限循环。正因为如此，我们在栈上构建了`QLabel` 对象后，能够一直显示在那里（试想，如果不是无限循环，`main()` 函数立刻会退出，`QLabel`对象当然也就直接析构了）。[这一节参考的相关内容](https://www.devbean.net/2012/08/qt-study-road-2-hello-world/) 

### PyQt 的 Python3 代码

```python
import sys
from PyQt5.QtWidgets import QApplication #导入QApplication类
from PyQt5.QtWidgets import QLabel #导入QLabel类

app = QApplication(sys.argv) #为QApplication类创建一个名为app的实例

label = QLabel("Hello, world")#创建QLabel对象，并为构造函数赋值。

label.show() #调用label实例的show()方法，将其显示出来

sys.exit(app.exec_()) #调用app.exec()，开启事件循环。
```

仔细对比两段代码，便会发现两者的相识之处，由此可见 PyQt 和 Qt 的拥有类似的使用方式。

> 关于`exec_()` 和 `exec()` ：
>
> 在 Python3 之前 `exec` 被作为[保留关键字](https://docs.python.org/2.7/reference/lexical_analysis.html#keywords)，不能被用作普通标识符。在 Python3 中 `exec` 不再是保留关键字，而被用作内置函数名（类似的情况有 `print` ）。在 PyQt5 + Python3 的环境中，`exec_()` 和 `exec()` 等效，但后者和 C++ 文档保持了一致性。对于旧版的 PyQt，只能够使用 `exec_()` 。

## Static Public Members

这一小节主要是为了理解 Qt 文档中 Static Public Members 的使用方式。

有时，我们会看到 Qt C++ 中，会在没有实例的情况下，直接调用类中的某个方法。
这些可被直接调用的方法就叫做 Static Public Members(静态公共成员)。
下面将展示一些有关静态成员的一些特性，以及 Python3 中有类似功能的装饰器。

### C++

在C++中，静态成员属于整个类而非某个对象。静态成员变量仅有一个副本，所有对象共用此副本。使用静态成员变量可实现多个对象之间的数据共享，并且不会破坏隐藏的原则，既保证了安全性还可以节省内存。

声明静态成员时，需要使用 `static` 关键字。
调用静态成员时，可以使用 `::` ，如 `<类名>::<静态成员名>` 。

1. 通过类名可调用静态成员，但不可调用非静态成员。

```C++
class Point
{
public:   
       void init()
       { 
       }
       static void output()
       {
       }
};
void main()
{
       Point::init();
       Point::output();
}
```

​	上面这段代码在编译时会出现错误：
​	error C2352: 'Point::init' : illegal call of non-static member function

2. 通过类实例可调用静态成员函数和非静态成员函数，修改上面的 `main()` 函数：

```C++
void main()
{
       Point pt;
       pt.init();
       pt.output();
}
```

​	上面这段代码编译正常，没有错误。

如果还想多了解一点，可以参考这里：[C++ 类的静态成员详细讲解](http://www.cnblogs.com/morewindows/archive/2011/08/26/2154198.html)

### Python3

C++ 中定义静态成员时，使用的 `static` 关键字，类似于 Python 中的 `@classmethod` 或 `@staticmethod` 装饰器。这两个装饰器，可以将实例方法转换类方法和静态方法。当然这两个装饰器之间还是稍有不同的，具体请查阅官方文档。

1. 通过类名可调用静态方法和类方法，当不可调用实例方法。
2. 通过类实例可调用静态方法和类方法。

```python
class Point(object):
    bar = 1

    def foo(self):
        print('method')

    @staticmethod
    def static_foo():
        print('static_method')
        print(Point.bar)

    @classmethod
    def class_foo(cls):
        print('class_method')
        print(cls.bar)
        cls().foo()


Point.static_foo()
Point.class_foo()
print()
pt = Point()
pt.foo()
pt.static_foo()
pt.class_foo()
```

输出：

```
static_method
1
class_method
1
method

method
static_method
1
class_method
1
method
```

### 调用示例

比如 [QMessageBox](https://doc.qt.io/qt-5/qmessagebox.html) 类中的 `warning` 就属于静态公共成员。
不像 Public Functions 需要实例对象。

Qt C++：

```c++
int ret = QMessageBox::warning(this, tr("My Application"),
                               tr("The document has been modified.\n"
                                  "Do you want to save your changes?"),
                               QMessageBox::Save | QMessageBox::Discard
                               | QMessageBox::Cancel,
                               QMessageBox::Save);
```

Python3：

```python
ret = QMessageBox.warning(self, 'My Application',
                          str("The document has been modified.\n"
                              "Do you want to save your changes?"),
                          QMessageBox.Save | QMessageBox.Discard
                          | QMessageBox.Cancel,
                          QMessageBox.Save)
```

## 返回值的数量

在 C++ 中，函数只能有一个返回值。
Qt C++ 为了获得多个返回值，便会在函数的参数列表中使用指针，然后在函数体内修改该指针指向的内存中的数据。
PyQt  则是通过让函数返回 Tuple，并对该 Tuple 进行拆包，以获取多个返回值。

那么我们如何通过 Qt C++ 文档，便能快速的知道 PyQt 中有多少个返回值喃？
答案是，PyQt 返回值的数量 = 1+ Qt参数列表中指针的数量 -1。

- 第一个 1 ，表示 Qt 中函数原本的返回值(在 C++ 中，函数只能有一个返回值。)
- 第二个 1 ，表示需要减去 `QWidget *parent` 指针。

### 确定指针数量

那么，如何确定 Qt C++ 参数列表中指针的数量喃？
首先让我们了解下 `*` 和 `&` 符号，主要是不要混淆了以下两种情况：

情况一，函数定义时：

- `*` ：声明一个指针变量，用于储存地址。
- `&` ：声明[引用](http://www.runoob.com/cplusplus/cpp-references.html)变量。

情况二，函数调用时：

- `*` ：取值运算符。对于指针 `a` ，`*a` 表示指针 `a` 指向的内存地址中存储的值；
- `&` ：取地址运算符。对于变量 `b` ，`&b` 将给出变量的实际内存地址。

下面这个示例展示了部分应用场景：

```c++
#include <iostream>
using namespace std;

void func(int &x, int *y) 
	//函数定义时：&x声明引用变量，*y声明引用变量
{
	x = x + 1;
	cout << "x：" << x << endl;
    cout << "y：" << y << endl;
    return;
}

int main ()
{
    int a = 100;
    int b = 200;
    func(a, &b); //函数调用时，&b表示取b的地址
	cout << "a：" << a << endl;
	return 0;
}
```

输出：

```
x：101
y：0x7ffe842338cc
a：101
```

注意：我们只需要关注函数定义时，指针的数量即可。通过函数定义时，所用 `*` 的数量，便能很快确定其中指针的数量。

### 确定返回值的数量

下面是一段 Qt C++ 文档，给出了静态公共成员 `getInt()` 的定义：

```c++
int QInputDialog::getInt(QWidget *parent, //指针1
	const QString &title, 
	const QString &label, 
	int value = 0, 
	int min = -2147483647, 
	int max = 2147483647, 
	int step = 1, 
	bool *ok = Q_NULLPTR, //指针2
	Qt::WindowFlags flags = Qt::WindowFlags())
```

`getInt()` 的定义中包含了两个指针。但是 `指针1` 表示父系关系，不会作为返回值，这里只有 `指针2` 被当作返回值使用。
那么，此时函数便有**两个返回值**，一个是函数原本的 `int` 类型的返回值，另一个是 `指针2` 指向的地址中的值。

下面再来看一段调用 `getInt()` 的代码：

```c++
    bool ok1;
    int i = QInputDialog::getInt(this, tr("QInputDialog::getInteger()"),
                                 tr("Percentage:"), 25, 0, 100, 1, &ok1);
    if (ok1)
        integerLabel->setText(tr("%1%").arg(i));
```

这里我们将 `ok1` 的地址传递给 `指针2` ，并会通过函数的运行情况，为 `ok1` 设置恰当的值。

最后我们来看一看 PyQt 的代码：

```python
    def getInt(self, QWidget, p_str, p_str_1, value=0, min=-2147483647, max=2147483647, step=1, flags, Qt_WindowFlags=None, Qt_WindowType=None, *args, **kwargs): # real signature unknown; NOTE: unreliably restored from __doc__ 
        """ getInt(QWidget, str, str, value: int = 0, min: int = -2147483647, max: int = 2147483647, step: int = 1, flags: Union[Qt.WindowFlags, Qt.WindowType] = Qt.WindowFlags()) -> Tuple[int, bool] """
        pass
```

由 `-> Tuple[int, bool]` 可见，函数有两个返回值，和我们之前的分析的结果是一致的。

## Q_NULLPTR

Q_NULLPTR 宏定义，在 Python 中即是 `null`

```c++
/*
 * C++11 keywords and expressions
 */
#ifdef Q_COMPILER_NULLPTR
# define Q_NULLPTR         nullptr
#else
# define Q_NULLPTR         NULL
#endif
```

## Protected Functions

C++ 有 public / protected / private 三种访问标号

访问标号的访问范围：

- private：只能由 1.该类中的函数、2.其友元函数访问。不能被任何其他访问，该类的对象也不能访问。

- protected：可以被1.该类中的函数、2.子类的函数、以及3.其友元函数访问。但不能被该类的对象访问。

- public：可以被1.该类中的函数、2.子类的函数、3.其友元函数访问，也可以由4.该类的对象访问。

  注：友元函数包括3种：设为友元的普通的非成员函数；设为友元的其他类的成员函数；设为友元类中的所有成员函数。

第二：类的继承后方法属性变化。

private 属性不能够被继承。
使用 private 继承，父类的 protected 和 public 属性在子类中变为 private；
使用 protected 继承，父类的 protected 和 public 属性在子类中变为 protected；
使用 public 继承，父类中的 protected 和 public 属性不发生改变; 

如下所示： 

|              | public    | protected | private |
| ------------ | --------- | --------- | ------- |
| public 继承    | public    | protected | 不可用     |
| protected 继承 | protected | protected | 不可用     |
| private 继承   | private   | private   | 不可用     |

protected继承和private继承能降低访问权限。

http://cnmtjp.blog.51cto.com/204390/36548

**protected Members**

The protected access label can be thought of as a blend of private and public :

- Like private members, protected members are inaccessible to users of the class.
- Like public members, the protected members are accessible to classes derived from this class.
- In addition, protected has another important property:
  A derived object may access the protected members of its base class only through a derived object. The derived class has no special access to the protected members of base type objects.

在没有继承的情况下，protected跟private相同。在派生类的时候才出现分化。

上面那段英文前两条都很好理解，基类对象不能访问基类的protected成员，派生类中可以访问基类的protected成员。也就是说private成员是不能被继承的，只有public，protected的成员才可以被继承。

就是最后一条有些迷惑人，派生类对象如果要访问基类protected成员只有通过派生类对象，派生类不能访问基类对象的protected成员。

请注意 drived class和drived object:派生类和派生类对象。第一点和第二点都是针对派生类来说的。

对于第三点总结一句话：只有在派生类中才可以通过派生类对象访问基类的protected成员。

举一个简单的例子：

```
#include <iostream>  
using namespace std;  
class Base  
{  
public:  
    Base(){};  
    virtual ~Base(){};  
protected:  
    int int_pro;  
};  
class A : public Base  
{  
public:  
    A(){};  
    A(int da){int_pro = da;}  
    void Print(A &obj){obj.int_pro = 24;}  
    void PrintPro(){cout << "The proteted data is " << int_pro <<endl;}  
};  
int main()  
{  
    A aObj;  
    A aObj2(5);  
    aObj2.PrintPro();  
    aObj.Print(aObj2);  
    aObj2.PrintPro();  
      
         //注释1  
         //aObj.int_pro = 8;  
}  
```

编译运行结果如下：

The protected data is 5

The protected data is 24

可见，在派生类内部直接访问protected成员和访问派生类对象基类的protected成员都是可行的。

但是若果解开注释1.就会编译报错。

很多书上都说有派生类的情况下protected的访问权限同public。这种说法是不对的，类内部直接访问没什么区别，但是访问对象基类的protected成员只能是在该类的内部。

我这里只列举了只有一层继承的情况，如果有多重继承的情况，比如三层。那么。中间层的类的内部还可以访问第三层类对象的基类成员，但是不能访问第三层类自己的protected的成员。http://blog.csdn.net/xlf13872135090/article/details/43563617

**对于 Qt**

通常用于子类扩展父类的功能的时候用，即类库程序员可以，但客户程序员不得使用。所以程序员一旦偷懒，不写子类而想直接使用保护函数，那是不行的。比如要给QLabel加上Click功能，明明有现成的mouseReleaseEvent的函数就可以实现点击效果，但客户程序员就是无法使用，不得不写一个QLabel的子类来实现，代码其实很简单：
http://qt-project.org/wiki/Make-a-QLabel-Clickable

http://www.cnblogs.com/findumars/p/4324358.html

### 小结

由以上内容可见，保护成员不能被类实例直接调用。主要是用在类继承的过程中，并不会在类实例中直接调用。

不过在 PyQt 中并没有这样的限制，类实例同样可以调用保护成员。

## C++ 类对象实例创建的4种方法

不用new关键字

在Stack栈里面分配空间，自动释放。

- A a; //默认无参构造函数
- A a(); //无参构造函数
- A a = A(); //无参构造函数
- *A a = A(Param param); //有参构造函数*

用new关键字

动态的，不确定分配空间大小

在heap堆里面分配空间，要手动释放(delete a或者delete a[]，如果a是数组的话)

- A* a = new A();

http://blog.csdn.net/peopleqinlei/article/details/55057077



























