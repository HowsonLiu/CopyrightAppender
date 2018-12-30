# CopyrightAppender
作为一个程序员，我们经常希望在自己的代码上加上属于自己的标记<br>
比如Copyright:
```python
# Copyright: Copyright(c) 2018
# Created on 2018 - 12 - 14
# Author: HowsonLiu
# Version 1.5
# Title: Sankaku爬虫
```
或者ASCII ART：
```python
#  _    _                               _      _       
# | |  | |                             | |    (_)      
# | |__| | _____      _____  ___  _ __ | |     _ _   _ 
# |  __  |/ _ \ \ /\ / / __|/ _ \| '_ \| |    | | | | |
# | |  | | (_) \ V  V /\__ \ (_) | | | | |____| | |_| |
# |_|  |_|\___/ \_/\_/ |___/\___/|_| |_|______|_|\__,_|
#                                                      
#                                                      
```
## 现在使用CopyrightAppender就能很方便批量对指定文件添加啦╮(￣▽￣)╭
* 下载并解压CopyrightAppender
![下载并解压](https://raw.githubusercontent.com/HowsonLiu/ReadmeImage/master/CopyrightAppender/1.png)
* 放到要添加的文件夹的子一级目录内(我已项目中的test文件夹示例)
![放置](https://raw.githubusercontent.com/HowsonLiu/ReadmeImage/master/CopyrightAppender/2.png)
* 配置ini文件
![配置ini](https://raw.githubusercontent.com/HowsonLiu/ReadmeImage/master/CopyrightAppender/3.png)
* 配置Copyright.txt文件。ヽ(`Д´)ﾉ注意！最好用utf-8，不然出现乱码你就糟了
![配置txt](https://raw.githubusercontent.com/HowsonLiu/ReadmeImage/master/CopyrightAppender/4.png)
* 现在可以运行代码了(｀・ω・´)
![运行](https://raw.githubusercontent.com/HowsonLiu/ReadmeImage/master/CopyrightAppender/5.png)
* 先按a添加吧
![添加](https://raw.githubusercontent.com/HowsonLiu/ReadmeImage/master/CopyrightAppender/6.png)
这里添加的规则是这样的：先跳过文件夹->再跳过指定文件->再匹配指定文件->最后匹配后缀<br>
添加之后当前路径会写入ini文件，值为1
#### 这时候强烈建议去看一下修改的文件有没有乱码ヽ(`Д´)ﾉ 有得话还能按c救一下，不然就只能手动删了
* 假设我不想要了或是出错了，按c
![clean](https://raw.githubusercontent.com/HowsonLiu/ReadmeImage/master/CopyrightAppender/7.png)
* 可以c多几次保证
![多次操作](https://raw.githubusercontent.com/HowsonLiu/ReadmeImage/master/CopyrightAppender/8.png)
* 没问题就退出吧，退出只能按×，没有其他退出办法(｡･ω･｡)
![退出](https://raw.githubusercontent.com/HowsonLiu/ReadmeImage/master/CopyrightAppender/9.png)
* 清理的还是绝对可靠的, TortoiseGit都看不出来
![效果](https://raw.githubusercontent.com/HowsonLiu/ReadmeImage/master/CopyrightAppender/10.png)
## 效果(o≖◡≖)
![c](https://raw.githubusercontent.com/HowsonLiu/ReadmeImage/master/CopyrightAppender/11.png)  
![python](https://raw.githubusercontent.com/HowsonLiu/ReadmeImage/master/CopyrightAppender/12.png)  
![ini](https://raw.githubusercontent.com/HowsonLiu/ReadmeImage/master/CopyrightAppender/13.png)  
![text](https://raw.githubusercontent.com/HowsonLiu/ReadmeImage/master/CopyrightAppender/14.png)  
## 小贴士（づ￣3￣）づ╭❤～
* 本工具唯一退出方式，就是右上角的×
* 改Copyright.txt之前最好clean一下
* Copyright.txt最好用utf-8
* 记得备份哦，记得备份哦，记得备份哦
## 关于乱码（〃｀ 3′〃）
代码中写入与清除都是按照字节进行的，如果你将一个带中文的gb2312编码的Copyright.txt写入一个ANSI编码的文件中，那妥妥的乱码了。你最好
* 确保Copyright.txt一定是utf-8
* 全部文件都是utf-8编码
* 出现乱码是不要慌，我相信大家都是中国人，出现乱码无非就gb2312或者big5之类的。只要Copyright.txt是utf-8,那一般将乱码文件转为utf-8就没事了
## 关于注释格式<(ˉ^ˉ)>
代码中支持4种注释格式
* C风格的 /**/ 后缀为.c .cpp .h .java .php .js
* Python风格的 #  后缀为.py
* ini风格的 ; 后缀为 .ini
* 文本风格的 其余所有后缀<br>
若你想改动的话，到CopyrightAppender.py改动吧
