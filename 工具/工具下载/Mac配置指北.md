# Mac装机指北

## 本机情况

MacBook Pro（16英寸，2021年）
- 芯片：Apple M1 Pro
- 内存大小：16 GB
- 专业：CS，Information Security

---

## 软件安装

### 沟通工具

- **微信**
- **QQ**
- **钉钉**
- **腾讯会议**
- **telegram** 

---

### 实用工具

- **Chrome**
  - 一个账号同步所有插件与书签，爽的

- **keka**
  -  解压软件

- **GitHub Desktop**
  - 用vscode的插件也很爽

- **ClashX Pro**
  - 科学上网

- **brew**
  - MacOS包管理工具
  - 一键安装命令：`/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"` 

- **Parallels Desktop**
  - Apple silicon 的虚拟机

- **Open VPN**

- **WPS**

- **百度网盘**


---

### 安全相关

- **Python**
  - 3.9.12
  - 没有选择3.10，因为3.10好像很多bug

- **Java**
  - 选择了 **java11** ，burp破解需要 9-14 的版本
  

- **Burp**

  - [安装方法](https://blog.csdn.net/weixin_41924764/article/details/118997114)

- **Postman**


---

### 终端

- **Iterm2**
  
**安装地址：** [https://iterm2.com/](https://iterm2.com/)

**配置：**


---

## ERROR or WARNING

- `curl: (7) Failed to connect to raw.githubusercontent.com port 443: Connection refused`
  - 443 端口连接被拒一般是因为墙的原因，如果你可以科学上网（Virtual Private Network）的话，在命令行键以下命令执行：
  ```bash
  # 7890 和 789 需要换成你自己的端口
    export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:789
  ```

- `Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get http://%2Fvar%2Frun%2Fdocker.sock/v1.40/containers/json: dial unix /var/run/docker.sock: connect: permission denied`
  - `sudo chmod 666 /var/run/docker.sock`
