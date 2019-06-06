# Sublime
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库



![python-sublime](Sublime.assets/python-sublime.png)

- 首先可以通过[官方网站](https://www.sublimetext.com/)下载安装程序安装Sublime 3或Sublime 2。

- 安装包管理工具。

  1. 通过快捷键 Ctrl+` 或者在View菜单中选择Show Console打开控制台，输入下面的代码。

  - Sublime 3

  ```Python
  import  urllib.request,os;pf='Package Control.sublime-package';ipp=sublime.installed_packages_path();urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler()));open(os.path.join(ipp,pf),'wb').write(urllib.request.urlopen('http://sublime.wbond.net/'+pf.replace(' ','%20')).read())
  ```

  - Sublime 2

  ```Python
  import  urllib2,os;pf='Package Control.sublime-package';ipp=sublime.installed_packages_path();os.makedirs(ipp)ifnotos.path.exists(ipp)elseNone;urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler()));open(os.path.join(ipp,pf),'wb').write(urllib2.urlopen('http://sublime.wbond.net/'+pf.replace(' ','%20')).read());print('Please restart Sublime Text to finish installation')
  ```

  2. 手动安装浏览器输入  https://sublime.wbond.net/Package%20Control.sublime-package 下载这个文件
     下载好以后，打开sublime text，选择菜单Preferences->Browse Packages... 打开安装目录
     此时会进入到一个叫做Packages的目录下，点击进入上一层目录Sublime Text3，在此目录下有一个文件夹叫做Installed Packages，把刚才下载的文件放到这里就可以了。然后重启sublime text3，观察Preferences菜单最下边是否有Package Settings 和Package Control两个选项，如果有，则代表安装成功了。

- 安装插件。通过Preference菜单的Package Control或快捷键Ctrl+Shift+P打开命令面板，在面板中输入Install Package就可以找到安装插件的工具，然后再查找需要的插件。我们推荐大家安装以下几个插件：
  - SublimeCodeIntel - 代码自动补全工具插件。
  - Emmet - 前端开发代码模板插件。
  - Git - 版本控制工具插件。
  - Python PEP8 Autoformat - PEP8规范自动格式化插件。
  - ConvertToUTF8 - 将本地编码转换为UTF-8。

