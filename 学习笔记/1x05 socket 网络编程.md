# socket 网络编程

18.1. socket — Low-level networking interface 

网络通信是指两台计算机上的两个进程之间的通信。

## 1. TCP/IP简介

互联网协议簇（Internet Protocol Suite）

因为互联网协议包含了上百种协议标准，但是最重要的两个协议是TCP和IP协议，所以，大家把互联网的协议简称TCP/IP协议。

**IP 协议：**负责把数据从一台计算机通过网络发送到另一台计算机。数据被分割成一小块一小块，然后通过IP包发送出去。由于互联网链路复杂，两台计算机之间经常有多条线路，因此，路由器就负责决定如何把一个IP包转发出去。IP包的特点是按块发送，途径多个路由，但不保证能到达，也不保证顺序到达。

**TCP协议**：是建立在IP协议之上的。TCP协议负责在两台计算机之间建立可靠连接，保证数据包按顺序到达。TCP协议会通过握手建立连接，然后，对每个IP包编号，确保对方按顺序收到，如果包丢掉了，就自动重发。

许多常用的更高级的协议都是建立在 TCP 协议基础上的，比如用于浏览器的HTTP协议、发送邮件的SMTP协议等。

一个IP包除了包含要传输的数据外，还包含源IP地址和目标IP地址，源端口和目标端口。

**端口**：在两台计算机通信时，只发IP地址是不够的，因为同一台计算机上跑着多个网络程序。一个IP包来了之后，到底是交给浏览器还是QQ，就需要端口号来区分。每个网络程序都向操作系统申请唯一的端口号，这样，两个进程在两台计算机之间建立网络连接就需要各自的IP地址和各自的端口号。

一个进程也可能同时与多个计算机建立链接，因此它会申请很多端口。

## 2. TCP 编程

套接字 Socket 是网络编程中的一个抽象概念。
通常用一个套接字表示“打开了一个网络连接”。
打开一个 socket 需要知道目标计算机的 IP 地址和端口号，并指定协议类型。

### 客户端

创建 socket > 建立连接 > 发送数据 > 接受数据 > 关闭连接

创建TCP连接时，主动发起连接的叫**客户端**，被动响应连接的叫**服务器**。
下面是创建一个基于TCP连接的 Socket：

```
# 导入socket库:
import socket

# 创建一个socket:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('www.sina.com.cn', 80))
```

-   `class socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)`

    `AF_INET` 表示使用IPv4协议，`AF_INET6` 则表示使用 IPV6
    `SOCK_STREAM` 表示使用面向流的TCP协议

    建立 `Socket` 对象后，还需要客户端主动发起 TCP 连接。


-   `def connect(address)`

    Connect the socket to a remote address. For IP sockets, the address is a pair (host, port). 
    host 如果是域名，则会自动转换为 IP 地址。
    port 端口号与服务器提供的服务有关，如 Web 服务器为 `80` 端口，SMTP服务是`25`端口，FTP服务是`21`端口等。端口号**小于1024**的是Internet标准服务的端口，端口号大于1024的，可以任意使用。

    注意参数是一个`tuple`，包含地址和端口号。

-   `def send(data, flags=None)`

    send(data[, flags]) -> count
    Send a data string to the socket. For the optional flags argument, see the Unix manual. Return the number of bytes sent; this may be less than len(data) if the network is busy.
    建立TCP连接后，我们就可以向新浪服务器发送请求，要求返回首页的内容：

```
# 发送数据:
s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection:close\r\n\r\n')
```

TCP连接创建的是双向通道，双方都可以同时给对方发数据。但是谁先发谁后发，怎么协调，要根据具体的协议来决定。例如，HTTP协议规定客户端必须先发请求给服务器，服务器收到后才发数据给客户端。

发送的文本格式必须符合HTTP标准，如果格式没问题，接下来就可以接收新浪服务器返回的数据了：


```
# 接收数据:
buffer = []
while True:
    # 每次最多接收1k字节:
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break
data = b''.join(buffer)
```

-   `def recv(buffersize, flags=None)`

    recv(buffersize[, flags]) -> data

    Receive up to buffersize bytes from the socket. For the optional flags argument, see the Unix manual. When no data is available, block until at least one byte is available or until the remote end is closed. When the remote end is closed and all data is read, return the empty string.

    接收数据时，调用`recv(max)`方法，一次最多接收指定的字节数，因此，在一个while循环中反复接收，直到`recv()`返回空数据，表示接收完毕，退出循环。

当我们接收完数据后，调用`close()`方法关闭Socket，这样，一次完整的网络通信就结束了：

```
# 关闭连接:
s.close()
```

接收到的数据包括HTTP头和网页本身，我们只需要把HTTP头和网页分离一下，把HTTP头打印出来，网页内容保存到文件：

```
header, html = data.split(b'\r\n\r\n', 1)
print(header.decode('utf-8'))
# 把接收的数据写入文件:
with open('sina.html', 'wb') as f:
    f.write(html)
```

现在，只需要在浏览器中打开这个`sina.html`文件，就可以看到新浪的首页了。

### 服务器

服务器进程首先要绑定一个端口，并监听来自其他客户端的连接。如果某个客户端连接过来了，服务器就与该客户端建立Socket连接，随后的通信就靠这个 Socket 连接了。

-   监听固定端口，每有客户端连接，就创建对应的 socket 连接


-   区分不同的 Socket 连接对应的客户端，利用服务器地址、服务器端口、客户端地址、客户端端口来确定 Socket 的唯一性。


-   服务器需要同时响应多个客户端的请求，每个连接都需要一个**新的进程或线程**来处理。否则，服务器一次就只能服务一个客户端。

示例：编写一个服务器程序，该程序可以接受来自客户端的连接，并把客户端发过来的字符串加上 `hello` 后，回传给客户端。

创建 socket > 绑定地址和端口 > 监听端口 > 接受客户端连接 > 处理通信 > 关闭连接

1.  创建一个基于IPv4和TCP协议的Socket：

```
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

2.  `def bind(address)`

    绑定需要监听的地址和端口。服务器可能有多块网卡，可以绑定到某块网卡的 IP 地址上，也可用 `0.0.0.0` 以绑定到所有的网络地址，用`127.0.0.1` 可绑定到本机地址。

    `127.0.0.1`是一个特殊的IP地址，表示本机地址，如果绑定到这个地址，客户端必须同时在本机运行才能连接，外部的计算机无法连接进来。

    端口号需要预先指定。因为我们写的这个服务不是标准服务，所以用`9999`这个端口号。请注意，小于`1024`的端口号必须要有管理员权限才能绑定：

```
# 监听端口:
s.bind(('127.0.0.1', 9999))
```

3.  `def listen(backlog=None)`

    Enable a server to accept connections. If backlog is specified, it must be at least 0 (if it is lower, it is set to 0); it specifies the number of unaccepted connections that the system will allow before refusing new connections. If not specified, a default reasonable value is chosen.

    调用 `listen()` 方法开始监听端口，传入的参数指定等待连接的最大数量：

```
s.listen(5)
print('Waiting for connection...')
```

4.  `def accept()`

    accept() -> (socket object, address info)

    Wait for an incoming connection. Return a new socket representing the connection, and the address of the client. For IP sockets, the address info is a pair (hostaddr, port).

    接下来，服务器程序通过一个永久循环来接受来自客户端的连接，`accept()`会等待并返回一个客户端的连接。
    每个连接都必须创建新线程（或进程）来处理，否则，单线程在处理连接的过程中，无法接受其他客户端的连接：

```
while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
```

处理 TCP 连接的函数：

```
import threading
import time

def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)
```

连接建立后，服务器首先发一条欢迎消息，然后等待客户端数据，并加上`Hello`再发送给客户端。如果客户端发送了`exit`字符串，就直接关闭连接。

要测试这个服务器程序，我们还需要编写一个客户端程序：

```
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('127.0.0.1', 9999))
# 接收欢迎消息:
print(s.recv(1024).decode('utf-8'))
for data in [b'Michael', b'Tracy', b'Sarah']:
    # 发送数据:
    s.send(data)
    print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close()
```

需要注意的是，客户端程序运行完毕就退出了，而服务器程序会永远运行下去，必须按Ctrl+C退出程序。

用 TCP 协议进行Socket编程在Python中十分简单，对于客户端，要主动连接服务器的IP和指定端口，对于服务器，要首先监听指定端口，然后，对每一个新的连接，创建一个线程或进程来处理。通常，服务器程序会无限运行下去。

同一个端口，被一个 Socket 绑定了以后，就不能被别的 Socket 绑定了。

## 3. UDP编程

TCP是建立可靠连接，并且通信双方都可以以流的形式发送数据。
相对TCP，UDP则是面向无连接的协议。

-   使用 UDP 协议时，无需建立连接，只需要知道对方的 IP 地址和端口号，就可以直接发送数据包。但是，并不能确定数据包的接受情况。
-   UDP 传输数据虽不可靠，但比 TCP 速度快，对于不要求可靠到达的数据，可使用 UDP 协议。

使用UDP的通信双方也分为客户端和服务器。

### 服务器

服务器首先需要绑定端口：

```
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定端口:
s.bind(('127.0.0.1', 9999))
```

-   `SOCK_DGRAM` 指定了这个Socket的类型是UDP。

绑定端口和TCP一样，但是不需要调用`listen()`方法，而是直接接收来自任何客户端的数据：

```
print('Bind UDP on 9999...')
while True:
    # 接收数据:
    data, addr = s.recvfrom(1024)
    print('Received from %s:%s.' % addr)
    s.sendto(b'Hello, %s!' % data, addr)
```

-   `def recvfrom(buffersize, flags=None)`

    Like recv(buffersize, flags) but also return the sender's address info.

    `recvfrom()` 方法返回数据和客户端的地址与端口，这样，服务器收到数据后，直接调用`sendto()`就可以把数据用UDP发给客户端。

注意这里省掉了多线程，因为这个例子很简单。

### 客户端

客户端使用UDP时，首先仍然创建基于UDP的Socket，然后，不需要调用`connect()`，直接通过`sendto()`给服务器发数据：

```
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for data in [b'Michael', b'Tracy', b'Sarah']:
    # 发送数据:
    s.sendto(data, ('127.0.0.1', 9999))
    # 接收数据:
    print(s.recv(1024).decode('utf-8'))
s.close()
```

从服务器接收数据仍然调用`recv()`方法。

仍然用两个命令行分别启动服务器和客户端测试

UDP的使用与TCP类似，但是不需要建立连接。此外，**服务器绑定UDP端口和TCP端口互不冲突**，也就是说，UDP的9999端口与TCP的9999端口可以各自绑定。















