# 0x04 json - PyMOTW-3

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 在阅读本文时，务必配合﹝0x03 json - JSON encoder and decoder.md﹞一起食用
>
> 参考:
>
> - https://pymotw.com/3/json/index.html
> - 译文 [每周一个 Python 模块 json.md](https://github.com/yongxinz/tech-blog/blob/master/python-module/%E6%AF%8F%E5%91%A8%E4%B8%80%E4%B8%AA%20Python%20%E6%A8%A1%E5%9D%97%20json.md)
> - 笔记[﹝0x02 pickle - Python object serialization.md﹞](./0x02 pickle - Python object serialization.md)
>
> 扩展阅读:
>
> - https://www.liaoxuefeng.com/wiki/1016959663602400/1017624706151424
>
> - [Python 2 to 3 porting notes for json](https://pymotw.com/3/porting_notes.html#porting-json)
> - [JavaScript Object Notation](http://json.org/) – JSON home, with documentation and implementations in other languages.
> - [jsonpickle](http://code.google.com/p/jsonpickle/) – `jsonpickle` allows for any Python object to be serialized into JSON.



**Purpose: **将 Python 对象编码为 JSON 字符串，或将 JSON 字符串解码为 Python 对象。

`json` 模块的 API 与 `pickle` 模块类似，用于将内存中的 Python 对象转换为 JSON 序列。与 `pickle` 不同的是，JSON 具有以多种语言（尤其是 JavaScript）实现的优点。它在 REST API 中 Web 服务端和客户端之间的通信被广泛应用，同时对于应用程序间通信需求也很有用。

## 编码和解码简单数据类型

默认编码器(*encoder*)可有效处理 Python 中的原生类型(`str`，`int`，`float`，`list`， `tuple`，和`dict`):

```python
import json

data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
print('DATA:', repr(data))	
#> DATA: [{'a': 'A', 'b': (2, 4), 'c': 3.0}]

data_string = json.dumps(data)
print('JSON:', data_string)	
#> JSON: [{"a": "A", "b": [2, 4], "c": 3.0}]
```

从表面上看，JSON 编码器的输出与 `repr()` 的输出类似。:arrow_up:

Python 对象在经历编码(*encoding*)和解码(*re-decoding*)后可能会改变原有对象类型:

```python
import json

data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
print('DATA   :', data)	
#> DATA   : [{'a': 'A', 'b': (2, 4), 'c': 3.0}]

data_string = json.dumps(data)
print('ENCODED:', data_string)	
#> ENCODED: [{"a": "A", "b": [2, 4], "c": 3.0}]

decoded = json.loads(data_string)
print('DECODED:', decoded)	
#> [{'a': 'A', 'b': [2, 4], 'c': 3.0}]

print('ORIGINAL:', type(data[0]['b']))	
#> ORIGINAL: <class 'tuple'>
print('DECODED :', type(decoded[0]['b']))	
#> DECODED : <class 'list'>
```

特别是，元组成为了列表。

将内置类型编码为 JSON 字符串的过程遵循如下转换表:

| Python                                 | JSON      |
| :------------------------------------- | :-------- |
| dict                                   | {} object |
| list, tuple                            | [] array  |
| str                                    | "string"  |
| int, float, int- & float-derived Enums | number    |
| True                                   | true      |
| False                                  | false     |
| None                                   | null      |

将 JSON 字符串解码为 Python 对象的过程遵循如下转换表:

| JSON          | Python |
| :------------ | :----- |
| object        | dict   |
| array         | list   |
| string        | str    |
| number (int)  | int    |
| number (real) | float  |
| true          | True   |
| false         | False  |
| null          | None   |



## 格式化输出

> 另见笔记﹝0x02 pickle - Python object serialization.md﹞

相较于 `pickle`，JSON 序列的另一个好处是人类可读。通过调整 `json.dump()` 的实参值，可使输出结果更易于阅读。例如，参数 *sort_keys* 会让编码器按照 key 对输出字典进行排序，而不是以随机顺序排列字典:

```python
import json

data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
print('DATA:', repr(data))	
#> DATA: [{'a': 'A', 'b': (2, 4), 'c': 3.0}]

unsorted = json.dumps(data)
print('JSON:', json.dumps(data))	
#> JSON: [{"a": "A", "b": [2, 4], "c": 3.0}]
print('SORT:', json.dumps(data, sort_keys=True))	
#> SORT: [{"a": "A", "b": [2, 4], "c": 3.0}]

first = json.dumps(data, sort_keys=True)
second = json.dumps(data, sort_keys=True)

print('UNSORTED MATCH:', unsorted == first)	
#> UNSORTED MATCH: True
print('SORTED MATCH  :', first == second)	
#> SORTED MATCH  : True
```

排序不仅有利于人类阅读，还可以直接比较 JSON 序列中的字典是否相等。:arrow_up:

对于高度嵌套的数据结构，可以使用 *indent* 参数来格式化输出。

```python
# json_indent.py
import json

data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
print('DATA:', repr(data))

print('NORMAL:', json.dumps(data, sort_keys=True))
print('INDENT:', json.dumps(data, sort_keys=True, indent=2))

# $ python3 json_indent.py
# DATA: [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
# NORMAL: [{"a": "A", "b": [2, 4], "c": 3.0}]
# INDENT: [
#   {
#     "a": "A",
#     "b": [
#       2,
#       4
#     ],
#     "c": 3.0
#   }
# ]
```

当 *indent* 是非负整数时，输出类似于 `pprint()`，并且数据结构中的每个级别都具备相应的缩进级别。:arrow_up:

但是，对于生产环境而言，上面这种输出方式会增加传输相同数据量所需的字节数。为了使输出数据更加紧凑，可利用 *separators* 参数来调整分隔 item 和 key-value 的方式，默认分隔方式是 `(',', ': ')`，item 之间使用 `','` 分隔，key-value 之间使用 `': '` 分隔。

```python
# json_compact_encoding.py
import json

data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
print('DATA:', repr(data))

print('repr(data)             :', len(repr(data)))

plain_dump = json.dumps(data)
print('dumps(data)            :', len(plain_dump))

small_indent = json.dumps(data, indent=2)
print('dumps(data, indent=2)  :', len(small_indent))

# 通过移除:后的空白，可以产生更紧凑的输出。
with_separators = json.dumps(data, separators=(',', ':'))
print('dumps(data, separators):', len(with_separators))

# $ python3 json_compact_encoding.py
# DATA: [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
# repr(data)             : 35
# dumps(data)            : 35
# dumps(data, indent=2)  : 73
# dumps(data, separators): 29
```



## 编码字典

> 另见笔记﹝0x02 pickle - Python object serialization.md﹞

JSON 字典中的 key 始终是字符串，将 Python `dict` 序列化为 JSON 字典时，在遇到以下类型的 Python key 时，会强制将以下 key 转换为字符串:

- `int`, `float`, `bool`, `None`

```python
>>> d = {'a': '--', 23: '--', True: '--', None: '--'}
>>> json.dumps(d)
'{"a": "--", "23": "--", "true": "--", "null": "--"}'
```

因此，如果将 `dict` 序列化为 JSON，然后又再次逆序列化为 `dict`，那么新 `dict` 对象可能与原 `dict` 对象并不相等。也就是说，如果字典 x 包含非字符串 key，则 `loads(dumps(x)) != x`。

```python
import json

original_dict = [1, {'2': 2, 1: 1}]
print(json.dumps(original_dict))
new_dict = json.loads(json.dumps(original_dict))
print(new_dict)
print(original_dict == new_dict)
```

输出:

```
[1, {"2": 2, "1": 1}]
[1, {'2': 2, '1': 1}]
False
```

如果在 Python `dict` 中包含 `tuple` 或其它类型的对象，则会在序列化时抛出 `TypeError`。解决该限制的一种方法是使用 *skipkeys* 参数告诉编码器跳过非字符串键：

``` python
# json_skipkeys.py
import json

data = [{'a': 'A', 'b': (2, 4), 'c': 3.0, ('d',): 'D tuple'}]

print('First attempt')
try:
    print(json.dumps(data))
except TypeError as err:
    print('ERROR:', err)

print()
print('Second attempt')
print(json.dumps(data, skipkeys=True))

# $ python3 json_skipkeys.py
# First attempt
# ERROR: keys must be str, int, float, bool or None, not tuple
# 
# Second attempt
# [{"a": "A", "b": [2, 4], "c": 3.0}]
```

此时，不会引发异常，而是忽略非字符串键。



## 序列化自定义类型

> 另见笔记﹝0x02 pickle - Python object serialization.md﹞

在前面的示例中，我们一直在使用 Python 内置类型，因为 `json` 原生就支持它们。不过有时我们也需要编码和解码自定义类，具体方法如下。

尝试把下面的类编码为 JSON 字符串:

```python
# json_myobj.py
class MyObj:

    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return '<MyObj({})>'.format(self.s)
```

编码 `MyObj` 实例最简单的方法是定义一个函数，其功能是把"未知的类型转"换成"已知类型"。该函数不需要进行编码操作，只需要把一个对象转换成另一个对象即可。

```python
# json_dump_default.py
import json
import json_myobj

obj = json_myobj.MyObj('instance value goes here')

print('First attempt')
try:
    print(json.dumps(obj))
except TypeError as err:
    print('ERROR:', err)


def convert_to_builtin_type(obj):
    print('default(', repr(obj), ')')
    # Convert objects to a dictionary of their representation
    d = {
        '__class__': obj.__class__.__name__,
        '__module__': obj.__module__,
    }
    d.update(obj.__dict__)
    return d


print()
print('With default')
print(json.dumps(obj, default=convert_to_builtin_type))

# $ python3 json_dump_default.py
# First attempt
# ERROR: Object of type MyObj is not JSON serializable
# 
# With default
# default( <MyObj(instance value goes here)> )
# {"__class__": "MyObj", "__module__": "json_myobj", "s": "instance value goes here"}
```

当 `json.dump()` 遇到无法序列化的 Python 对象时，便会调用 *default* 函数 `convert_to_bulitin_type()`，其功能是将 Python 对象转换为携带实例数据的 `dict` 对象，然后 `json.dump()` 会将 `dict` 对象序列化为 JSON 字典。:arrow_up:

由 JSON 字符串中重建 `MyObj()` 实例时，需要使用 `json.loads()` 的 *object_hook* 参数。在逆序列化过程中，如果 `json.loads()` 遇到 `dict` 对象，就会调用 *object_hook* 函数(以 `dict` 对象做实参)，并将 *object_hook* 的返回值用作逆序列化的结果。因此，我们可利用 *object_hook* 参数来重建实例对象。

```python
# json_load_object_hook.py
import json

def dict_to_object(d):
    if '__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name) # 如果模块不存在，需要导入模块
        print('MODULE:', module.__name__)
        class_ = getattr(module, class_name)
        print('CLASS:', class_)
        args = {
            key: value
            for key, value in d.items()
        }
        print('INSTANCE ARGS:', args)
        inst = class_(**args)
    else:
        inst = d
    return inst


encoded_object = '''
    [{"s": "instance value goes here",
      "__module__": "json_myobj", "__class__": "MyObj"}]
    '''

myobj_instance = json.loads(
    encoded_object,
    object_hook=dict_to_object,
)
print(myobj_instance)

# $ python3 json_load_object_hook.py
# MODULE: json_myobj
# CLASS: <class 'json_myobj.MyObj'>
# INSTANCE ARGS: {'s': 'instance value goes here'}
# [<MyObj(instance value goes here)>]
```

由于 `json` 会将字符串转成 Unicode 对象，在把它们作为类构造器的关键字参数之前我们还需要把它们重新编码为 ASCII 字符串(针对 Python 2)。

类似的 hook 参数还有 *parse_int*, *parse_float*, *parse_constant*，详见﹝0x02 pickle - Python object serialization.md﹞

## 编码器和解码器类

> 另见笔记﹝0x02 pickle - Python object serialization.md﹞

`json` 不仅提供了用于编码和解码的函数，还提供了用于解码和编码的类。通过类可以访问额外的 APIs。

利用编码器 `JSONEncoder` 的可迭代接口，可获得包含已编码数据的迭代器。此时无需在内存中存放整个数据结构。

```python
# json_encoder_iterable.py
import json

encoder = json.JSONEncoder()
data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]

for part in encoder.iterencode(data):
    print('PART:', part)
    
# $ python3 json_encoder_iterable.py
# PART: [
# PART: {
# PART: "a"
# PART: :
# PART: "A"
# PART: ,
# PART: "b"
# PART: :
# PART: [2
# PART: , 4
# PART: ]
# PART: ,
# PART: "c"
# PART: :
# PART: 3.0
# PART: }
# PART: ]
```

迭代器在生成数据时每次返回一个逻辑单元，而不是返回特定长度的数据。:arrow_up:

`encode()` 方法基本上等同于 `''.join(encoder.iterencode())`，但前者还包含一些额外的错误检测。

如果想要编码非内置对象，则需要对 `JSONEncode` 进行扩展。在进行扩展时，你需要子类化 `JSONEncode`，并重新实现 `default()` 方法，实现方法类似于前面提到的 `convert_to_bulitin_type()` 函数。

```python
# json_encoder_default.py
import json
import json_myobj


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        print('default(', repr(obj), ')')
        # Convert objects to a dictionary of their representation
        d = {
            '__class__': obj.__class__.__name__,
            '__module__': obj.__module__,
        }
        d.update(obj.__dict__)
        return d


obj = json_myobj.MyObj('internal data')
print(obj)
print(MyEncoder().encode(obj))

# $ python3 json_encoder_default.py
# <MyObj(internal data)>
# default( <MyObj(internal data)> )
# {"__class__": "MyObj", "__module__": "json_myobj", "s": "internal data"}
```

输出结果与之前的实现相同。:arrow_up:

解码文本，然后转换字典到对象需要比之前稍多的步骤。

```python
# json_decoder_object_hook.py
import json


class MyDecoder(json.JSONDecoder):

    def __init__(self):
        json.JSONDecoder.__init__(
            self,
            object_hook=self.dict_to_object,
        )

    def dict_to_object(self, d):
        if '__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            print('MODULE:', module.__name__)
            class_ = getattr(module, class_name)
            print('CLASS:', class_)
            args = {
                key: value
                for key, value in d.items()
            }
            print('INSTANCE ARGS:', args)
            inst = class_(**args)
        else:
            inst = d
        return inst


encoded_object = '''
[{"s": "instance value goes here",
  "__module__": "json_myobj", "__class__": "MyObj"}]
'''

myobj_instance = MyDecoder().decode(encoded_object)
print(myobj_instance)

# $ python3 json_decoder_object_hook.py
# MODULE: json_myobj
# CLASS: <class 'json_myobj.MyObj'>
# INSTANCE ARGS: {'s': 'instance value goes here'}
# [<MyObj(instance value goes here)>]
```

输出与前面的例子相同。

## 使用流和文件

> 另见笔记﹝0x02 pickle - Python object serialization.md﹞

到目前为止，所有示例都假设整个数据结构的已编码版本可被完整存储到内存中。对于大型数据结构，最好将 JSON 序列直接写入 file-like 对象中。`load()` 和 `dump()` 可接受 file-like 对象的引用，并进行读取或写入。

```python
# json_dump_file.py
import io
import json

data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]

f = io.StringIO()
json.dump(data, f)

print(f.getvalue())	
#> [{"a": "A", "b": [2, 4], "c": 3.0}]
```

套接字或普通文件句柄的工作方式与本示例中使用的 `StringIO` 缓冲区相同 。:arrow_up:

类似于 `dump()`，可将 file-like 对象都可以传递给 `load()`。

```python
# json_load_file.py
import io
import json

f = io.StringIO('[{"a": "A", "c": 3.0, "b": [2, 4]}]')
print(json.load(f))	
#> [{'a': 'A', 'c': 3.0, 'b': [2, 4]}]
```



## 混合数据流

> 另见笔记﹝0x02 pickle - Python object serialization.md﹞

`JSONDecoder` 包含名为 `raw_decode()` 的实例方法，当 JSON 数据后面跟有额外数据时，可用此方法解码。返回值是一个元组，其中包含解码 JSON 序列得到的 Python 对象和解码结束的位置的索引值。

:warning: JSON 数据只能位于待解码字符串的最前端，否则会发生异常。

```python
# json_mixed_data.py
import json

decoder = json.JSONDecoder()


def get_decoded_and_remainder(input_data):
    obj, end = decoder.raw_decode(input_data)
    remaining = input_data[end:]
    return (obj, end, remaining)


encoded_object = '[{"a": "A", "c": 3.0, "b": [2, 4]}]'
extra_text = 'This text is not JSON.'

print('JSON first:')
data = ' '.join([encoded_object, extra_text])
obj, end, remaining = get_decoded_and_remainder(data)

print('Object              :', obj)
print('End of parsed input :', end)
print('Remaining text      :', repr(remaining))

print()
print('JSON embedded:')
try:
    data = ' '.join([extra_text, encoded_object, extra_text])
    obj, end, remaining = get_decoded_and_remainder(data)
except ValueError as err:
    print('ERROR:', err)
    
# $ python3 json_mixed_data.py
# JSON first:
# Object              : [{'a': 'A', 'c': 3.0, 'b': [2, 4]}]
# End of parsed input : 35
# Remaining text      : ' This text is not JSON.'
# 
# JSON embedded:
# ERROR: Expecting value: line 1 column 1 (char 0)
```



## 命令行中的 JSON

`json.tool` 模块实现了一个命令行程序，用于重新格式化 JSON 数据以便于阅读。

```python
# example.json
[{"a": "A", "c": 3.0, "b": [2, 4]}]
```

输入文件 `example.json` 中的键值对并没有按照 key 的字母顺序排列。在下面的第一个示例中，只会重新格式化数据；第二个示例中，在格式化数据的同时，还会按照 key 的字母顺序重排字典中的内容。

```python
$ python3 -m json.tool example.json

[
    {
        "a": "A",
        "c": 3.0,
        "b": [
            2,
            4
        ]
    }
]

$ python3 -m json.tool --sort-keys example.json

[
    {
        "a": "A",
        "b": [
            2,
            4
        ],
        "c": 3.0
    }
]
```

