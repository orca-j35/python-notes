# Charles Proxy
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

Charles 集成了 HTTP proxy / HTTP monitor / Reverse Proxy，你可以利用 Charles 来查看机器与互联网之间的所有 HTTP 和 SSL / HTTPS 流量——包括请求(*request*)、响应(*responses*)和 HTTP 头(包含 cookies 和缓存信息)。

Fiddler 是与 Charles 类似的软件，但后者的功能更为强大，且跨平台支持更好。

相关资源:

- Home: https://www.charlesproxy.com/
- Download: https://www.charlesproxy.com/download/
- Crack: (Charles 是付费软件)
  - 利用 charles.jar 文件破解 Charles(暂未尝试过此方法)，详见 https://www.zzzmode.com/mytools/charles/
  - 通过第三方服务器来注册 Charles(已尝试，可成功注册)，详见 https://zhile.io/2017/07/07/charles-proxy-usage-and-license.html

使用参考:

- https://blog.csdn.net/mxw2552261/article/details/78645118

## SSL 代理

> 参考: https://www.charlesproxy.com/documentation/proxying/ssl-proxying/

Charles 可用作中间人(*man-in-the-middle*) HTTPS 代理(*proxy*)，这使得你能够以纯文本格式查看 Web 浏览器和 SSL Web 服务器之间的通信。

Charles 作中间人(*man-in-the-middle*) HTTPS 代理(*proxy*)时，它并不会让你的浏览器看到服务器的证书(*certificate*)。此时，Charles 会为服务器动态生成证书，并使用自己的根证书(Charles CA Certificate)对其签名。Charles 会收到服务器的证书，而你的浏览器会收到 Charles 的证书。当你的浏览器(或其它应用)收到来自 Charles 的证书时，会显式一个安全警告，用以提示你该证书并非来自服务器，且该根权限不受信任。你可以在每次出现该警告时点选确认按钮；你也可以将 Charles CA Certificate 添加至受信任的证书中，这就浏览器(或其它应用)就不会在出现任何警告了(见下一小节)。

Charles 作中间人(*man-in-the-middle*) HTTPS 代理(*proxy*)时，仍然会通过 SSL 与 Web 服务器通信。通信是从 Web 浏览器到 Charles，再从 Charles 到 Web 服务器，且均为 SSL(encrypted) 。

可在 Proxy Preferences 中关闭或开启 SSL 代理(Proxy -> SSL Proxying Settings)。在关闭 SSL 代理后，Charles 只会将所有 SSL 流量直接转发至目标 Web 服务器。

### Choosing hosts to SSL Proxy

你需要手动设置需要启用 SSL Proxying 的 host 列表，该列表位于(Proxy -> SSL Proxying Settings)中。还可以在 structure 视图中右键单击 host 并选择开启或关闭 SSL Proxying。

在将 host 添加到 SSL Proxying 列表后，你可能需要重启 Charles 才能更改现有的浏览器会话。

如果你想要 SSL 代理所有 host，则需要将 `*` 添加至 SSL Proxying Settings 的列表中。

对于没有启用 SSL 代理的 host，则会在 Notes 中提示 "SSL Proxying not enabled for this host: enable in Proxy Settings, SSL locations"

## 安装 Charles's  SSL 证书

> 参考: 
>
> - https://www.charlesproxy.com/documentation/using-charles/ssl-certificates/
> - 《Python3网络爬虫开发实战》-> 1.7 App爬取相关库的安装 -> Charles 的安装
> - https://www.jianshu.com/p/91815d0afb44

Charles 会为站点生成自己的证书，并使用 Charles Root Certificate 来为这些证书签名。如果 Charles Root Certificate 不在"受信任根证书列表"中，那么当你浏览器(或其它应用)收到该证书时便会发出警告，你可以在每次出现该警告时点选确认按钮；你也可以将 Charles CA Certificate 添加至受信任的证书中，这就浏览器(或其它应用)就不会在出现任何警告了。

另外，由于 Charles Root Certificate 会随 Charles 的版本而便会，所以当 Charles 的版本发生变化时，可能需要重新配置 Charles Root Certificate。

这里只介绍几个我会用到的环境，其余环境的证书配置详见 https://www.charlesproxy.com/documentation/using-charles/ssl-certificates/

### Windows / Internet Explorer

1. 依次点击 Help -> SSL Proxying ->Install Charles Root Certificate，将出现"证书窗口"，并警告"此 CA 根目录证书不受信任。要启用信任，请将该证书安装到'受信任的根证书颁发机构'存储区"
2. 通过在"证书窗口"中点击 "安装证书"来启动"证书导入导向"。必须手动选择将证书导入"受信任的根证书颁发机构"
3. 安装完 Charles Root Certificate 后，可能需要重启浏览器

### Chrome

我在 Windows 10 下使用的是 Chrome 73，当我按照 Windows / Internet Explorer 中的方法配置完 Charles Root Certificate 后，Chrome 便能正常使用 Charles Root Certificate，无需额外设置。

如果按照官方给出的方法(如下)，实际上与 Windows / Internet Explorer 导入的是同一个证书。

> In Charles go to the Help menu and choose "SSL Proxying > Save Charles Root Certificate". Save the root certificate as a Binary Certificate (.cer) to your desktop, or somewhere where you can easily access it in the next step.
>
> In Chrome, open the Settings. At the bottom of the settings page, click "Advanced" to open the advanced section, then click the "Manage certificates…" button.
>
> Go to the "Trusted Root Certification Authorities" tab and click "Import…".
>
> Find the certificate file you saved from Charles in the previous step, then click Next and Finish, leaving the default options, until you complete the import. Chrome will now always trust certificates signed by Charles.
>
> After importing you can delete the certificate file that you saved.

### Android

以下方法仅适用于 Android N 之前的设备:

- 将 Android 设备的代理设置为 Charles 的 HTTP 代理，可在 Charles -> Help -> Local IP Addresses 中查看 Charles 的当前 IP。
- 在 Android 设备的浏览器中打开 https://chls.pro/ssl，然后下载并安装证书即可。

### Python

Python's *requests* module will fail with an error when you try to use it with SSL Proxying in Charles:

```python
requests.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate
verify failed (_ssl.c:590)
```

You can configure *requests* to trust your Charles Root Certificate. First save your certificate as a .pem file using the Help > SSL Proxying > Save Charles Root Certificate menu. Then configure your Session as follows:

```python
from requests import Session
session = Session()
session.verify = "charles-ssl-proxying-certificate.pem"
```

