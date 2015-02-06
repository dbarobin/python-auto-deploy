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

### 9.1 软件概要 ###

Nginx版本目录结构如下：

	tree auto_deploy_app_to_nginx

> auto_deploy_app_to_nginx <br/>
> ├── auto_deploy_app_remote.py <br/>
> ├── auto_deploy_app_v_final.py <br/>
> ├── auto_execute_shop.sh <br/>
> ├── auto_scp_nginx_log.sh <br/>
> ├── config.conf <br/>
> └── crontab <br/>
> 
> 0 directories, 6 files

该脚本实现的功能如下：

* 打印帮助
* 检出Shop项目
* 更新Shop项目
* 部署Shop项目
* 启动、关闭、重启Nginx服务器

### 9.2 脚本帮助 ###

	./auto_deploy_app_remote.py -h
 
 ``` bash
  Auto deploy application to the remote web server. Write in Python.
 Version 1.0. By Robin Wen. Email:dbarobinwen@gmail.com
 
 Usage auto_deploy_app.py [-hcustrd]
   [-h | --help] Prints this help and usage message
   [-c | --svn-co-shop] Checkout the shop repo via svn
   [-u | --svn-update-shop] Update the shop repo via svn
   [-s | --shutdown-nginx] Shutdown the shop via the nginx shutdown and startup scripts
   [-t | --startup-nginx] Startup the shop  via the nginx shutdown and startup scripts
   [-r | --restart-nginx] Restart the shop via the nginx shutdown and startup scripts
   [-d | --deploy-shop] Deploy shop to nginx server.

 ``` 

在脚本名后加上「-h 或者 --help」表示打印帮助。
同理，加上「 -c | --svn-co-shop」表示检出Shop项目，加上「-u | --svn-update-shop」表示更新Shop项目，加上「-s | --shutdown-nginx」表示关闭Nginx服务器，加上「-t | --startup-nginx」表示启动Nginx服务器，加上「-r | --restart-nginx」表示重启Nginx服务器，加上「-d | --deploy-shop]」表示部署Mall API项目。

### 9.3 脚本概述 ###

如前所述，「auto_deploy_app_remote.py」是主执行脚本，用于显示帮助以及调用相应函数。「auto_deploy_app_v_final.py」是核心执行脚本，实现所有的相关功能。核心执行脚本采用Fabric实现远程执行命令，主执行脚本再通过**fab -f 脚本名 任务名**调用相应方法。

主执行脚本和核心执行脚本的方法名基本一致，主执行脚本包括如下方法：main(argv)、usage()、svn_co_shop()、svn_update_shop()、shutdown_nginx()、startup_nginx()、restart_nginx()和deploy_shop()。

核心执行脚本包括如下方法：svn_co_shop()、svn_update_shop()、shutdown_nginx()、startup_nginx()、restart_nginx()、deploy_shop()和getConfig()。

**主执行脚本：**

* main(argv) 主函数
* usage() 使用说明函数
* svn_co_shop() 检出Shop项目
* svn_update_shop() 更新Shop项目
* shutdown_nginx() 关闭Nginx服务器
* startup_nginx() 启动Nginx服务器
* restart_nginx() 重启Nginx服务器
* deploy_shop() 部署Shop项目

**主执行脚本**

主执行脚本内容如下：
参考脚本auto_deploy_app_remote.py。

**核心执行脚本**

方法和主执行脚本基本一致，相同的不赘述。核心执行脚本还提供getConfig()方法，用于读取配置文件。

核心执行脚本内容如下：
参考脚本auto_deploy_app_v_final.py。

`auto_execute_shop.sh`脚本实现了自动从SVN检出项目，自动部署到Nginx。

参考auto_execute_shop.sh脚本。

`auto_scp_nginx_log.sh`脚本实现了从Nginx服务器自动拉取日志。为了更好的查看日志，拉取了access log和error log。

参考auto_scp_nginx_log.sh脚本。

### 9.4 配置文件概述 ###

完整配置文件内容如下：

```bash
# Remote server section.
[remote]
# Remote server ip.
remote_ip=
# Remote server port.
remote_port=
# Remote server username.
remote_usr=
# Remote server password.
remote_pwd=

# SVN path section.
[svn_path]
# Svn main directory of repo.
svn_shop_dir=

# Shop svn configuration section. 
[svn]
# Shop svn url.
svn_url=
# Shop svn username.
svn_username=
# Shop svn password.
svn_password=

# Nginx section.
[nginx]
# Nginx webapps path.
nginx_path=

# Other configuration section.
[other]
# Remote log path.
remote_log_path=
```

接下来，我逐一进行讲解。

配置文件包括以下段：remote、svn_path、svn_admin、svn_api、tomcat和other。

每个段的说明如下：

* remote 该段定义远程服务器登录信息。
	* remote_ip 部署远程服务器IP。
	* remote_port 部署远程服务器端口。
	* remote_usr 部署远程服务器用户名。
	* remote_pwd 部署远程服务器密码。
*  svn_path 该段定义SVN的相关路径。
	* svn_shop_dir 该段定义SVN的Shop目录。
*  svn 该段定义Shop项目的SVN相关信息。
	*  svn_url Shop SVN的URL。
	*  svn_username Shop SVN的URL。
	*  svn_password Shop VN的密码。
* nginx 该段定义Nginx相关信息。
	* nginx_path Nginx的webapps路径。
* other 该段定义其他配置信息。
	* remote_log_path 远程服务器Log路径。

如有需要，请酌情修改。

## 9.5 脚本使用 ##

**Step 1：** 把以auto_开头的四个脚本以及config.conf配置文件放到远程服务器，脚本中的路径（YOUR_PATH）、Nginx access log（access_log）、Nginx error log（error_log）、用户名（YOUR_NAME）、密码（YOUR_IP）请酌情修改。


**Step 2：** 添加crontab计划任务。

	crontab -e

crontab 任务如下。

	crontab -l

> 00 00 * * * bash YOUR_PATH/auto_execute_shop.sh
> 00 01 * * * bash YOUR_PATH/auto_scp_nginx_log.sh
> */1 * * * * ntpdate pool.ntp.org

该任务定义了凌晨0点部署项目，以及凌晨1点拷贝日志。

**Step 3：** 早晨上班就可以看到昨晚的部署日志了，如果有问题，把日志给开发人员，再做调试。So easy, 妈妈再也不用担心我加班了！:)

## 10.脚本详解之自动化生成测试报告 ##

### 10.1 软件概要 ###

该软件实现了自动化生成测试报告。首先测试人员生成测试脚本（亦即jmx文件），然后使用Python脚本和Shell脚本，实现自动化生成测试报告。生成测试报告使用了ant和jmeter。

自动化生成测试报告目录结构如下：

	tree auto_gen_testing_reports

> auto_gen_testing_reports <br/>
> ├── auto_deploy_app_remote.py <br/>
> ├── auto_deploy_app_v_final.py <br/>
> ├── auto_gen_testing_reports.sh <br/>
> ├── build.xml <br/>
> ├── config.conf <br/>
> ├── crontab <br/>
> ├── get_git_version.py <br/>
> └── test_result.py <br/>
> 
> 0 directories, 8 files

该脚本实现的功能如下：

* 打印帮助
* 克隆Git项目
* 拉取Git项目
* 配置生成报告
* 自动生成测试报告
* 拷贝生成报告

### 10.2 脚本帮助 ###

	./auto_deploy_app_remote.py -h
 
 ``` bash
 Auto generate testing reports. Write in Python.
 Version 1.0. By Robin Wen. Email:dbarobinwen@gmail.com
 
 Usage auto_deploy_app.py [-hpas]
   [-h | --help] Prints this help and usage message
   [-c | --git-clone] Clone the repo via git
   [-u | --git-pull] Update the repo via git
   [-p | --pre-conf] Pre config before generate testing reports
   [-a | --auto-gen] Auto generate testing reports
   [-s | --scp-report] SCP generated testing reports

 ``` 

在脚本名后加上「-h 或者 --help」表示打印帮助。
同理，加上「-c  | --git-clone」表示克隆Git项目，加上「-u | --git-pull」表示获取Git项目，加上「-p | -pre-conf」表示测试前准备，加上「-a | --auto-gen」表示自动化生成测试报告，加上「-s | --scp-report」表示拷贝生成的测试报告。

### 10.3 脚本概述 ###

如前所述，「auto_deploy_app_remote.py」是主执行脚本，用于显示帮助以及调用相应函数。「auto_deploy_app_v_final.py」是核心执行脚本，实现所有的相关功能。核心执行脚本采用Fabric实现远程执行命令，主执行脚本再通过**fab -f 脚本名 任务名**调用相应方法。

主执行脚本和核心执行脚本的方法名基本一致，主执行脚本包括如下方法：main(argv)、usage()、git_clone()、git_pull()、pre_conf()、auto_gen()和scp_report()。

核心执行脚本包括如下方法：git_clone()、git_pull()、pre_conf()、auto_gen()、scp_report()和getConfig()。

**主执行脚本：**

* main(argv) 主函数
* usage() 使用说明函数
* git_clone() 克隆项目函数
* git_pull() 拉取项目函数
* pre_conf() 执行自动化生成测试报告之前的准备工作
* auto_gen() 自动化生成测试报告
* scp_report() 拷贝生成的测试报告

**主执行脚本**

主执行脚本内容如下：
参考脚本auto_deploy_app_remote.py。

**核心执行脚本**

方法和主执行脚本基本一致，相同的不赘述。核心执行脚本还提供getConfig()方法，用于读取配置文件。

核心执行脚本内容如下：
参考脚本auto_deploy_app_v_final.py。

`auto_gen_testing_reports.sh`脚本实现了自动生成测试报告，并且拷贝生成的测试报告。

参考auto_gen_testing_reports.sh脚本。

`build.xml`为ant的配置文件。

### 10.4 配置文件概述 ###

完整配置文件内容如下：

```bash
# Remote server section.
[remote]
# Remote server ip.
remote_ip=
# Remote server port.
remote_port=
# Remote server username.
remote_usr=
# Remote server password.
remote_pwd=

# Jmeter section.
[jmeter]
# Jmeter home directory.
jmeter_home=

# Ant section.
[ant]
# Ant home directory.
ant_home=

# Scripts section.
[script]
# Mall scripts home dir.
script_dir=
# Jmeter mall scripts section.
mall_script=

# Report section.
[report]
# Report directory.
report_dir=
# Report export directory.
report_exp_dir=

# Git section.
[git]
# Git Url.
git_url=
# Git repo diectory.
git_repo=
```

接下来，我逐一进行讲解。

配置文件包括以下段：remote、jmeter、ant、script、report和git。

每个段的说明如下：

* remote 该段定义远程服务器登录信息。
	* remote_ip 部署远程服务器IP。
	* remote_port 部署远程服务器端口。
	* remote_usr 部署远程服务器用户名。
	* remote_pwd 部署远程服务器密码。
*  jmeter 该段定义Jmeter的相关路径。
	* jmeter_home Jmeter主目录。
*  ant 该段定义Ant的相关信息。
	*  ant_home Ant的主目录。
* script 该段定义脚本相关信息。
	* script_dir 脚本的主目录。
	* mall_script 自动化测试报告的脚本路径。
* report 该段定义测试报告的相关信息。
	* report_dir 存放Jmeter脚本的服务器的测试报告目录。
	* report_exp_dir 导出到远程服务器的测试报告目录。
* git 该段定义Git的相关信息。
	* git_url Git的URL。
	* git_repo 克隆的Git项目目录。

如有需要，请酌情修改。

## 10.5 脚本使用 ##

**Step 1：** 把以auto_开头的三个脚本以及config.conf配置文件放到远程服务器，脚本中的路径（YOUR_PATH）请酌情修改。

**Step 2：** 把`get_git_version.py`放到存放Jmeter脚本的服务器，请酌情存放。

**Step 3：** 把`build.xml`放到存放Jmeter脚本的服务器，其中JMeter.home、testing.testplans.home、testing.report.home参数对应的路径请酌情修改。

**Step 4：** 远程服务器添加crontab计划任务。

	crontab -e

crontab 任务如下。

	crontab -l

> 10 00 * * * bash YOUR_PATH/auto_gen_testing_reports.sh 
> */1 * * * * ntpdate pool.ntp.org

该任务定义了凌晨0点10分自动化生成测试报告。

**Step 5：** 早晨上班就可以看到昨晚生成的测试报告了，如果有问题，把日志给开发人员，再做调试。So easy, 妈妈再也不用担心我加班了！:)

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
