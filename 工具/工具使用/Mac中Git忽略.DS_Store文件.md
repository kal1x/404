# Mac中Git忽略.DS_Store文件

## 方案一：项目设置.gitignore

仅针对git的处理最naive的想法就是设置.gitignore文件。

.gitignore文件用于忽略文件，官网介绍在[这里](https://git-scm.com/docs/gitignore)，规范如下：

- 所有空行或者以注释符号 ＃ 开头的行都会被 git 忽略，空行可以为了可读性分隔段落，# 表明注释。
- 第一个 / 会匹配路径的根目录，举个栗子，”/*.html”会匹配”index.html”，而不是”d/index.html”。
- 通配符 * 匹配任意个任意字符，? 匹配一个任意字符。需要注意的是通配符不会匹配文件路径中的 /，举个栗子，”d/*.html”会匹配”d/index.html”，但不会匹配”d/a/b/c/index.html”。
- 两个连续的星号 ** 有特殊含义：
  - 以 **/ 开头表示匹配所有的文件夹，例如 **/test.md 匹配所有的test.md文件。
  - 以 /** 结尾表示匹配文件夹内所有内容，例如 a/** 匹配文件夹a中所有内容。
  - 连续星号 ** 前后分别被 / 夹住表示匹配0或者多层文件夹，例如 a/**/b 匹配到 a/b 、a/x/b 、a/x/y/b 等。
  - 前缀 ! 的模式表示如果前面匹配到被忽略，则重新添加回来。如果匹配到的父文件夹还是忽略状态，该文件还是保持忽略状态。如果路径名第一个字符为 ! ，则需要在前面增加 \ 进行转义。

对于一些常用的系统、工程文件的.gitignore文件可以参考[这个网站](https://www.gitignore.io/)进行设置，这里有很多模板。

针对.DS_Store文件，在git工程文件夹中新建.gitignore文件，在文件中设置：

```.git
**/.DS_Store
```

对于已经提交的内容，希望git能够忽略，但同时并不会删除本地文件，需要在terminal输入以下命令：

```sh
$ git rm -r --cached $file_path
```

这个方案的优点就是方便、快捷、最容易想到，缺点就是每个git项目都要重复一遍。

---

## 方案二：全局设置忽略
虽然每个项目配.gitignore文件可以成功，但是每个项目都需要配，嗯，有点烦。我们可以在git的全局进行配置来忽略.DS_Store文件。

设置之前我们先看下现在的git config配置情况（git config官方文档说明）：

```sh
$ git config --list
```

实际上git配置情况可以在 ~/.gitconfig 文件中查看。

```sh
$ vim ~/.gitconfig
```

通过 :q! 退出后，我们需要建立一个文件，把需要全局忽略的文件路径写入其中。该文件起名为.gitignore_global：
```sh
$ touch ~/.gitignore_global
```
然后对这个文件进行修改。

```sh
# Mac OS
**/.DS_Store
```

然后对git进行全局设置，让git忽略.gitignore_global中的所有文件：

```sh
$ git config --global core.excludesfile ~/.gitignore_global
```

这样就不用每个git目录都设置忽略.DS_Store文件了！