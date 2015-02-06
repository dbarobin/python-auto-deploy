# Python 自动化部署 #

## 1.文档摘要 ##

> Python 自动化部署，本机只需执行脚本，远程即可自动部署。脚本采用Python编写，远程调用使用Fabric实现。

## 2.更新日志 ##

2014-11-28
> 文档版本为「1.0」，文档名为「Python 自动化部署 V1.0」，备注为「文档正式版，已测试通过」，By Robin。

2014-12-04
> 文档版本为「2.0」，文档名为「Python 自动化部署 V2.0-Release」，备注为「文档正式版第二版，修复若干Bug」，By Robin。

2014-12-12
> 文档版本为「2.1」，文档名为「Python 自动化部署 V2.1-Release」，备注为「添加部署 Tomcat 脚本」，By Robin。

2014-12-17
> 文档版本为「2.2」，文档名为「Python 自动化部署 V2.2-Release」，备注为「添加部署到 Nginx 服务器脚本」，By Robin。

2014-12-19
> 文档版本为「2.3」，文档名为「Python 自动化部署 V2.3-Release」，备注为「添加部署到 Tomcat 服务器脚本」，By Robin。

2014-12-24
> 文档版本为「2.4」，文档名为「Python 自动化部署 V2.4-Release」，备注为「添加自动化生成测试报告脚本」，By Robin。

2015-01-31
> 文档版本为「2.5」，文档名为「Python 自动化部署 V2.5-Release」，备注为「添加 All in One 部署 Java 项目脚本」，By Robin。

## 3.版本信息 ##

本机 XXX：

> 系统版本：<br/>
> 主机名：XXX <br/>
> IP：xxx.xxx.xxx.xxx <br/>
> Python：2.6.6

远程服务器 XXX：

> 系统版本：XXX <br/>
> 主机名：XXX <br/>
> IP：xxx.xxx.xxx.xxx <br/>
> Python：2.7.3 <br/>
> JDK：1.8.25 <br/>
> Maven：3.2.3 <br/>
> SVN：1.6.17

Tomcat服务器 XXX：

> 系统版本：XXX <br/>
> 主机名：XXX <br/>
> IP：xxx.xxx.xxx.xxx

Web服务器 XXX：

> 系统版本：XXX <br/>
> 主机名：XXX <br/>
> IP：xxx.xxx.xxx.xxx

## 4.先决条件 ##

**本机安装软件：**

> Python 2.7.5

安装包如下：

> apt-get: python python-pip python-dev subversion subversion-tools <br/>
> yum: python python-pip python-devel subversion <br/>
> pip: fabric

**远程服务器安装软件：**

> JDK：JDK 1.6.45 1.7.71 1.8.25 方便不同版本切换<br/>
> Maven：3.2.3 <br/>
> SVN：1.6.17

安装包如下：

> dos2unix subversion subversion-tools

**Tomcat服务器安装软件：**

> JDK：JDK 1.6.45 1.7.71 1.8.25 方便不同版本切换<br/>
> Tomcat：6.0.45 <br/>
> SVN：1.6.17 <br/>
> ant：1.9.4 用于打包 <br/>
> Jmeter：2.12 用于后期做自动化测试扩展

**Web服务器安装软件：**

> Nginx：1.6.2 <br/>
> SVN：1.6.17

## 5.软件综述 ##

参考 Wiki：[Python Auto Deploy 概述](http://git.io/bwSy)

## 6.脚本详解之Linux版本 ##

参考 Wiki：[部署 Java 项目到 Tomcat(Core Platform)](http://git.io/bwQq)

## 7.脚本详解之Windows版本 ##

参考 Wiki：[部署 Java 项目到 Tomcat(Core Platform, Windows 版本)](http://git.io/bw7q)

## 8.脚本详解之Tomcat版本 ##

参考 Wiki：[部署 Java 项目到 Tomcat(Mall)](http://git.io/bw7A)

## 9.脚本详解之Nginx版本 ##

参考 Wiki：[部署 PHP 项目到 Nginx](http://git.io/bwdv)

## 10.脚本详解之自动化生成测试报告 ##

参考 Wiki：[自动生成测试报告](http://git.io/bwd5)

Enjoy！

## 11.GitHub地址 ##

python-auto-deploy：https://github.com/dbarobin/python-auto-deploy

## 12.项目说明 ##

auto_deploy_app_v2: 适用于Linux。<br/>
auto_deploy_app_windows: 适用于Windows。<br/>
auto_deploy_app_to_tomcat: 适用于Linux下部署到Tomcat服务器。<br/>
auto_deploy_app_to_nginx: 适用于Linux下部署到Nginx服务器。<br/> 
auto_gen_testing_reports：适用于Linux下自动化生成测试报告。

## 13.作者信息 ##

温国兵

* Robin Wen
* <a href="mailto:dbarobinwen@gmail.com"><img src="http://i.imgur.com/7yOaC7C.png" title="Robin's Gmail" border="0" height="16px" width="16px" alt="Robin's Gmail" /></a>
* <a href="https://github.com/dbarobin" target="_blank"><img src="https://farm9.staticflickr.com/8653/15815300288_69bb6bb56d_o_d.png" title="Github" border="0" alt="Github" height="16px" width="16px" /></a>
* <a href="http://dbarobin.com" target="_blank"><img src="http://i.imgur.com/dEfMkyt.jpg" title="Robin's Blog" border="0" alt="Robin's Blog" height="16px" width="16px" /></a>
* <a href="http://blog.csdn.net/justdb" target="_blank"><img src="http://i.imgur.com/BROigUO.jpg" title="DBA@Robin's CSDN" height="16px" width="16px" border="0" alt="DBA@Robin's CSDN" /></a>


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/dbarobin/python-auto-deploy/trend.png)](https://bitdeli.com/free "Bitdeli Badge")
