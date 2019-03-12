# conda 常用命令
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - [Getting started with conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-python)
> - [Command reference](https://conda.io/projects/conda/en/latest/commands.html#)
> - [canda 常用命令](https://www.cnblogs.com/Jimc/archive/2018/09/13/9641963.html)

注意: conda 是一个完全独立于 Python 的包&环境管理器，Python 对于 conda 来说只是 conda 的一个包，就如同 Linux 把 conda 当成一个包一样，
scipy、jupyter 对于 conda 来说也都是包——详见 [conda & pip](bicmr.pku.edu.cn/~wenzw/pages/conda.html) 。

## 1. 管理 conda

> 详见: [Managing conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-conda.html#managing-conda)

```shell
# 更新conda
conda update conda
# 如果位于非base环境中，在更新base时，需要选择base环境
conda update -n base conda
# 版本信息
conda --version
# 帮助信息
conda --help
# 获取特定命令的帮助信息
conda install --help
conda remove --help
```

命令选项由 `--` 加英文单词组成，可简写为 `-` 加首字母的形式。因此，`--name` 与 `-n` 等效，`--evns` 与 `-e` 等效。

## 2. 管理环境

> 详见: [Managing environments](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

### 2.1 列出所有现存环境

```shell
conda info --envs
conda env list
```

### 2.2 新建环境

新环境位于 `~/Anaconda/envs` 目录

```shell
# 创建一个空环境
conda create --name $env_name
# 创建包含指定包的环境
conda create -n $env_name $package_spec [$package_spec...]
# 还可指定特定版本的包
conda create -n $env_name python=3.6
conda create -n $env_name python=2.7 scrapy numpy
# 如果没有指定python版本，conda
conda create -n $env_name python
```

### 2.3 激活某个环境

```shell
# 仅适用于conda4.6以后的版本
conda activate $env_name
# conda4.6之前的版本
activate $env_name # in Windows
source activate $env_name # in Linux and macOS
```

### 2.4 停用当前环境

```python
conda deactivate # in Windows
source deactivate # in Linux and macOS
```

### 2.5 克隆某个环境

```shell
conda create --name $new_env_name --clone $old_env_name
```

不能直接克隆当前所在环境(base除外)

### 2.6 删除环境

删除指定环境中的所有包，即删除该环境

```shell
conda remove --name $env_name --all
```

### 2.7 分享环境

如果需要分享或备份 conda 创建的环境，可依照如下步骤：

```shell
# 1.激活目标环境
activate target_env
# 2.在当前工具目录生成一个.yml文件
conda env export -> environment.yml
# 3.在其它机器上重建环境，将.yml放到工作目录下，并使用该.yml文件创建环境
conda env create -f environment.yml
```

## 3. 管理包

> 详见: [Managing packages](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-pkgs.html)

### 3.1 安装包

```shell
# 在当前环境中安装包
conda install $package_spec [$package_spec ...]
# 在指定环境中安装包
conda install -n $env_name $package_spec [$package_spec ...]
# 从指定源中安装包
conda install -c $URL $package_spec [$package_spec ...]
```

### 3.2 列出已安装的包

```shell
# 列出当前环境中已安装的包
conda list
# 列出指定环境中已安装的包
conda list -n $env_name
```

### 3.3 更新包

```shell
# 更新当前环境中的包
conda update $package_spec [$package_spec ...]
# 更新指定环境中的包
conda update -n $env_name $package_spec [$package_spec ...]
```

### 3.4 卸载包

```shell
# 卸载当前环境中的包
conda remove $package_spec [$package_spec ...]
# 卸载指定环境中的包
conda remove -n $env_name $package_spec [$package_spec ...]
```

### 3.5 查找包

```shell
# 在索引中查找名为SEARCH_TERM的包
conda search $SEARCH_TERM # 查看名称中包含SEARCH_TERM的包
conda search --full --name $SEARCH_TERM # 查看名称完全与SEARCH_TERM匹配的包
```

如果在索引中找不到，还可尝试在 https://anaconda.org/ 中手动搜索

## 4. 管理 channels

> 详见: [Managing channels](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-channels.html)

```shell
# 清华镜像
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
```

配置信息位于 `user/.condarc` 中，如果需要使用 Conda 三方源可参考：

- https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/
- http://mirrors.ustc.edu.cn/help/anaconda.html









