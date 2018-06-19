#!/usr/bin/env python
#encoding:utf-8
# Author: Robin Wen
# Date: 11/25/2014 10:51:54
# Desc: Auto deploy core and auth platform to remote server.

# Import necessary packages.
import os
import sys, getopt
import socket
import string
import shutil
import getopt
import errno
import logging
import tempfile
import datetime
import subprocess
import json
import ConfigParser
import ctypes

from operator import itemgetter
from functools import wraps
from getpass import getpass, getuser
from glob import glob
from contextlib import contextmanager

from fabric.api import env, cd, prefix, sudo, run, hide, local, put
from fabric.contrib.files import exists, upload_template
from fabric.colors import yellow, green, blue, red

try:
    import json
except importError:
    import simplejson as json

# Print Color configuration
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# Text Color
FOREGROUND_BLACK = 0x00 # black.
FOREGROUND_DARKBLUE = 0x01 # dark blue.
FOREGROUND_DARKGREEN = 0x02 # dark green.
FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue.
FOREGROUND_DARKRED = 0x04 # dark red.
FOREGROUND_DARKPINK = 0x05 # dark pink.
FOREGROUND_DARKYELLOW = 0x06 # dark yellow.
FOREGROUND_DARKWHITE = 0x07 # dark white.
FOREGROUND_DARKGRAY = 0x08 # dark gray.
FOREGROUND_BLUE = 0x09 # blue.
FOREGROUND_GREEN = 0x0a # green.
FOREGROUND_SKYBLUE = 0x0b # skyblue.
FOREGROUND_RED = 0x0c # red.
FOREGROUND_PINK = 0x0d # pink.
FOREGROUND_YELLOW = 0x0e # yellow.
FOREGROUND_WHITE = 0x0f # white.

# Background color
BACKGROUND_BLUE = 0x10 # dark blue.
BACKGROUND_GREEN = 0x20 # dark green.
BACKGROUND_DARKSKYBLUE = 0x30 # dark skyblue.
BACKGROUND_DARKRED = 0x40 # dark red.
BACKGROUND_DARKPINK = 0x50 # dark pink.
BACKGROUND_DARKYELLOW = 0x60 # dark yellow.
BACKGROUND_DARKWHITE = 0x70 # dark white.
BACKGROUND_DARKGRAY = 0x80 # dark gray.
BACKGROUND_BLUE = 0x90 # blue.
BACKGROUND_GREEN = 0xa0 # green.
BACKGROUND_SKYBLUE = 0xb0 # skyblue.
BACKGROUND_RED = 0xc0 # red.
BACKGROUND_PINK = 0xd0 # pink.
BACKGROUND_YELLOW = 0xe0 # yellow.
BACKGROUND_WHITE = 0xf0 # white.

# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool

def resetColor():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

# Green
def printGreen(mess):
    set_cmd_text_color(FOREGROUND_GREEN)
    sys.stdout.write(mess)
    resetColor()

# Red
def printRed(mess):
    set_cmd_text_color(FOREGROUND_RED)
    sys.stdout.write(mess)
    resetColor()

# Configuration file name.
config_file='config.conf'

# Get configuration from the Config 
def getConfig(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/'+config_file
    config.read(path)
    return config.get(section, key)

# Log path
log_path=getConfig("other", "remote_log_path")

# Remote server hosts.
hosts=getConfig("remote", "remote_usr")+"@"+getConfig("remote", "remote_ip")+":"+getConfig("remote", "remote_port")

# Remote server password.
password=getConfig("remote", "remote_pwd")

env.hosts=[hosts,]
env.password = password

# Remote server ip.
remote_ip=getConfig("remote", "remote_ip")

# Remote server username.
remote_usr=getConfig("remote", "remote_usr")

# Remote server password.
remote_pwd=getConfig("remote", "remote_pwd")

# Declare multiple variables.

# Core platform path.
core_platform_path=getConfig("core_path", "core_platform_path")

# Core platform configuration file path.
core_platform_config_path=getConfig("core_path", "core_platform_config_path")

# Auth platform path.
auth_path=getConfig("auth_path", "auth_path")

# Auth platform configuration path.
auth_platform_config_path=getConfig("auth_path", "auth_platform_config_path")

# Core platform config api path
core_platform_config_api_path=getConfig("core_path", "core_platform_config_api_path")

# Core platform config auth path
core_platform_config_auth_path=getConfig("core_path", "core_platform_config_auth_path")

# Auth platform configuration api path.
auth_platform_config_api_path=getConfig("auth_path", "auth_platform_config_api_path")

# Auth platform configuration auth path.
auth_platform_config_auth_path=getConfig("auth_path", "auth_platform_config_auth_path")

# Svn main directory of newarkstg repo.
svn_ns_dir=getConfig("svn_path", "svn_ns_dir")

# Svn core platform path.
svn_core_platform_path=getConfig("svn_path", "svn_core_platform_path")

# Svn core platform target path.
svn_core_platform_target_path=getConfig("svn_path", "svn_core_platform_target_path")

# Database address.
db_addr=getConfig("database", "db_addr")

# Database username.
db_usr=getConfig("database", "db_usr")

# Datbase password.
db_pwd=getConfig("database", "db_pwd")

# Database port.
db_port=getConfig("database", "db_port")

# SVN username.
svn_username=getConfig("svn", "svn_username")

# SVN password.
svn_password=getConfig("svn", "svn_password")

# SVN url.
svn_url=getConfig("svn", "svn_url")

# Memcached server ip.
memcached_ip=getConfig("memcached", "memcached_ip")

# Memcached server port.
memcached_port=getConfig("memcached", "memcached_port")

# Local ip address. Deploy the application on the localhost by default.
ip_addr=getConfig("remote", "remote_ip")

# Core platform version.
core_version=getConfig("other", "core_version")

# Api port
api_port=getConfig("other", "api_port")

# Core platform bundles path
core_platform_bundles_path=getConfig("core_path", "core_platform_bundles_path")

# Auth platform bundles path
auth_platform_bundles_path=getConfig("auth_path", "auth_platform_bundles_path")

# Core platform jar name
core_platform_jar=getConfig("other", "core_platform_jar")

# Auth platform jar name
auth_platform_jar=getConfig("other", "auth_platform_jar")

# Core jar
core_jar=getConfig("other", "core_jar")

# Auth jar
auth_jar=getConfig("other", "auth_jar")

"""
-----------------------------------------------------------------------------
Auto deploy core-platform and auth to tomcat.

Use the -h or the --help flag to get a listing of options.

Program: Deploy application
Author: Robin Wen
Date: November 25, 2014
Revision: 1.0
"""
# Checkout the newarkstg repo via svn function.
def svn_co():
    print('Checkout the newarkstg repo via svn.')
    
    # Create necessary directory
    run('mkdir -p '+svn_ns_dir+' 2>/dev/null >/dev/null')

    #run('ls -l '+path+'')
    with cd(svn_ns_dir):
        run('svn co --username '+svn_username+' --password '+svn_password+' '+svn_url+' '+svn_ns_dir+'')

    print('Checkout finished!')

# Update the newarkstg repo via svn function.
def svn_update():
    print('Update the newarkstg repo via svn.')

    # Create necessary directory
    run('mkdir -p '+svn_ns_dir+' 2>/dev/null >/dev/null')

    with cd(svn_ns_dir):
        run('svn update --username '+svn_username+' --password '+svn_password+' '+svn_ns_dir+'')

    print('Update finished!')

# Shutdown the core platform via the stop.sh scripts function.
def shutdown_core():
    print('Shutdown the core platform via the stop.sh scripts.')
    
    run('cd '+core_platform_path+' && ./stop.sh')
    
    print('Shutdown the core platform finished!')

# Startup the core platform via the startup.sh scripts function.
def startup_core():
    print('Startup the core platform via the startup.sh scripts.')

    run('cd '+core_platform_path+' && ./startup.sh')

    print('Startup the core platform finished!')

# Restart the core platform via the startup.sh scripts function.
def restart_core():
    print('Restart the core platform via the restart.sh scripts.')

    run('cd '+core_platform_path+' && ./restart.sh')

    print('Restart the core platform finished!')

# Shutdown the auth platform via the stop.sh scripts function.

def shutdown_auth():
    print('Shutdown the auth platform via the stop.sh scripts.')

    run('cd '+auth_path+' && ./stop.sh &')

    print('Shutdown the auth platform finished!')

# Startup the auth platform via the startup.sh scripts function.
def startup_auth():
    print('Startup the auth platform via the startup.sh scripts.')

    run('cd '+auth_path+' && ./startup.sh &')

    print('Startup the authplatform finished!')

# Restart the auth platform via the startup.sh scripts function.
def restart_auth():
    print('Restart the core platform via the restart.sh scripts.')
    
    run('cd '+auth_path+' && ./restart.sh &')

    print('Restart the core platform finished!')

# Deploy core platform via mvn function.
def deploy_core_platform():
    print('Deploy core platform via mvn.')

    # Create necessary directory
    run('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    run('mkdir -p '+svn_core_platform_path+' 2>/dev/null >/dev/null')
    run('mkdir -p '+svn_core_platform_target_path+' 2>/dev/null >/dev/null')
    run('mkdir -p '+core_platform_path+' 2>/dev/null >/dev/null')

    with cd(svn_core_platform_path):
        # Print waiting info.
        print ''
        printRed('Please wait the deploy process until it automatically exit...')
 
        # Install the necessary jar.

        # Clear the core platform deploy log.
        run('echo "" > '+log_path+'/core_deploy.log')
        run('mvn install:install-file -Dfile='+svn_core_platform_path+'/lib/org.eclipse.osgi_3.10.0.v20140606-1445.jar -DgroupId=org.eclipse.osgi -DartifactId=org.eclipse.osgi -Dversion=3.10.0.v20140606 -Dclassifier=1445 -Dpackaging=jar > '+log_path+'/core_deploy.log')

        run('mvn install:install-file -Dfile='+svn_core_platform_path+'/lib/org.eclipse.osgi.services_3.4.0.v20140312-2051.jar -DgroupId=org.eclipse.osgi -DartifactId=org.eclipse.osgi.services -Dversion=3.4.0.v20140312 -Dclassifier=2051 -Dpackaging=jar >> '+log_path+'/core_deploy.log')

        # Pack the core platform use mvn command.
        run('mvn clean install >> '+log_path+'/core_deploy.log')

        # Remove the useless directory.
        run('rm -rf '+svn_core_platform_target_path+'/'+'classes')
        run('rm -rf '+svn_core_platform_target_path+'/'+'maven-archiver')
        run('rm -rf '+svn_core_platform_target_path+'/'+'maven-status')
    
    # Copy the packed core platform to the deploy directory.
    run('cp -r '+svn_core_platform_target_path+'/'+'* '+core_platform_path)

    # Change the privileges of scripts. Make it executable.
    run('chmod +x '+core_platform_path+'/'+'*.sh')

    # Update the service address. Use the local ip address by default.
    run("sed -i 's/^service_addr=.*$/service_addr=http:\/\/"+ip_addr+":8789\/auth\//g' "+core_platform_config_auth_path+"/osgi-auth-config.properties")

    # Update the database url.
    run("sed -i 's/^url=.*$/url=jdbc:mysql:\/\/"+db_addr+":"+db_port+"\/cmms_auth/g' "+core_platform_config_auth_path+"/osgi-auth-config.properties")

    # Update the database username.
    run("sed -i 's/^username=.*$/username="+db_usr+"/g' "+core_platform_config_auth_path+"/osgi-auth-config.properties")
    # Update the database password.
    run("sed -i 's/^password=.*$/password="+db_pwd+"/g' "+core_platform_config_auth_path+"/osgi-auth-config.properties")

    # Update the authentication server host.
    run("sed -i 's/^authentication_server_host_name=.*$/authentication_server_host_name="+ip_addr+"/g' "+core_platform_config_api_path+"/osgi-util-config.properties")

    # Update the memcached server ip.
    run("sed -i 's/^memcached_server_name=.*$/memcached_server_name="+memcached_ip+"/g' "+core_platform_config_api_path+"/osgi-util-config.properties")

    # Update the memcached server port.
    run("sed -i 's/^memcached_server_port=.*$/memcached_server_port="+memcached_port+"/g' "+core_platform_config_api_path+"/osgi-util-config.properties")

    # Update the memcached server ip.
    run("sed -i 's/^memcached_server_name=.*$/memcached_server_name="+memcached_ip+"/g' "+core_platform_config_auth_path+"/osgi-auth-config.properties")

    # Update the memcached server port.
    run("sed -i 's/^memcached_server_port=.*$/memcached_server_port="+memcached_port+"/g' "+core_platform_config_auth_path+"/osgi-auth-config.properties")

    # Update the bundles directory.
    run("sed -i 's/^platform\.bundles\.root\.dir=.*$/platform\.bundles\.root\.dir="+core_platform_bundles_path+"/g' "+core_platform_config_path+"/osgi-container.properties")

    # Update the api service configuration.
    run("sed -i 's/address=.*$/address=\"http:\/\/"+ip_addr+":"+api_port+"\" \>/g' "+core_platform_config_api_path+"/api-service.xml")

    # Remove the end of configuration file. ^M mark.
    run("dos2unix "+core_platform_config_auth_path+"/osgi-auth-config.properties")
    run("dos2unix "+core_platform_config_api_path+"/osgi-util-config.properties")
    run("dos2unix "+core_platform_config_path+"/osgi-container.properties")

    # Remove the auth directory.
    run("rm -rfv "+core_platform_config_path+"/auth")

    print('Congratulations! Deploy core platform finished!')

# Update the database setting function.
def update_database_setting():

    print('Update the database setting.')
    # Create the temp dir.
    run('mkdir -p ~/temp 2>/dev/null >/dev/null')

    # Copy the dao jar.
    run("cp -v "+core_platform_path+"/bundles/busi/service_impl/com.newarkstg.cmms.dao_"+core_version+".jar ~/temp")

    # Unzip the dao jar.
    run("cd ~/temp && jar xvf ~/temp/com.newarkstg.cmms.dao_"+core_version+".jar")

    # Update the database configuration in the hibernate.cfg.xml.
    run("sed -i 's/jdbc:mysql:\/\/.*$/jdbc:mysql:\/\/"+db_addr+":"+db_port+"\/cmms\<\/property\>/g' ~/temp/hibernate.cfg.xml")

    # Update the database configuration in the persistence.xml.
    run("sed -i 's/jdbc:mysql:\/\/.*$/jdbc:mysql:\/\/"+db_addr+":"+db_port+"\/cmms\"\/\>/g' ~/temp/META-INF/persistence.xml")

    # Remove the old jar.
    run("rm -rf ~/temp/com.newarkstg.cmms.dao_"+core_version+".jar")

    # Convert the configuration file.
    run("dos2unix ~/temp/hibernate.cfg.xml")
    run("dos2unix ~/temp/META-INF/persistence.xml")

    # Create the dao jar.
    run("cd ~/temp && jar cvfM com.newarkstg.cmms.dao_"+core_version+".jar com hibernate.cfg.xml META-INF")

    # Copy the jar to the core platform.
    run("cp -v ~/temp/com.newarkstg.cmms.dao_"+core_version+".jar"+" "+core_platform_path+"/bundles/busi/service_impl")

    # Remove the temp directory.
    run("rm -rfv ~/temp")

    print('Update the database setting finished!')

# Deploy auth platform via mvn.
def deploy_auth_platform():
    print('Deploy auth platform via mvn.')

    # Create necessary directory
    run('mkdir -p '+svn_core_platform_target_path+' 2>/dev/null >/dev/null')
    run('mkdir -p '+auth_path+' 2>/dev/null >/dev/null')

    # Copy the packed core platform to the deploy directory.
    run("cp -r "+svn_core_platform_target_path+"/"+"* "+auth_path)

    # Change the privileges of scripts. Make it executable.
    run("chmod +x "+auth_path+"/"+"*.sh")

    # Remove the busi directory.
    run("rm -rf "+auth_path+"/bundles/busi")

    # Update the service address. Use the local ip address by default.
    run("sed -i 's/^service_addr=.*$/service_addr=http:\/\/"+ip_addr+":8789\/auth\//g' "+auth_platform_config_auth_path+"/osgi-auth-config.properties")

    # Update the database url.
    run("sed -i 's/^url=.*$/url=jdbc:mysql:\/\/"+db_addr+":3306\/cmms_auth/g' "+auth_platform_config_auth_path+"/osgi-auth-config.properties")

    # Update the database username.
    run("sed -i 's/^username=.*$/username="+db_usr+"/g' "+auth_platform_config_auth_path+"/osgi-auth-config.properties")

    # Update the database password.
    run("sed -i 's/^password=.*$/password="+db_pwd+"/g' "+auth_platform_config_auth_path+"/osgi-auth-config.properties")

    # Update the authentication server host.
    run("sed -i 's/^authentication_server_host_name=.*$/authentication_server_host_name="+ip_addr+"/g' "+auth_platform_config_api_path+"/osgi-util-config.properties")

    # Update the memcached server ip.
    run("sed -i 's/^memcached_server_name=.*$/memcached_server_name="+memcached_ip+"/g' "+auth_platform_config_api_path+"/osgi-util-config.properties")

    # Update the memcached server port.
    run("sed -i 's/^memcached_server_port=.*$/memcached_server_port="+memcached_port+"/g' "+auth_platform_config_api_path+"/osgi-util-config.properties")

    # Update the memcached server ip.
    run("sed -i 's/^memcached_server_name=.*$/memcached_server_name="+memcached_ip+"/g' "+auth_platform_config_auth_path+"/osgi-auth-config.properties")

    # Update the memcached server port.
    run("sed -i 's/^memcached_server_port=.*$/memcached_server_port="+memcached_port+"/g' "+auth_platform_config_auth_path+"/osgi-auth-config.properties")

    # Update the bundles directory.
    run("sed -i 's/^platform\.bundles\.root\.dir=.*$/platform\.bundles\.root\.dir="+auth_platform_bundles_path+"/g' "+auth_platform_config_path+"/osgi-container.properties")

    # Rename the jar.
    with cd(auth_path):
        sudo('./rename.sh '+core_platform_jar+' '+auth_platform_jar+'')

    # Optimize the stop scripts
    run("sed -i 's/"+core_jar+"/"+auth_jar+"/g' "+auth_path+"/stop.sh")

    # Remove the end of configuration file. ^M mark.
    run("dos2unix "+auth_platform_config_auth_path+"/osgi-auth-config.properties")
    run("dos2unix "+auth_platform_config_api_path+"/osgi-util-config.properties")
    run("dos2unix "+auth_platform_config_path+"/osgi-container.properties")

    # Remove the api directory.
    run("rm -rf "+auth_platform_config_path+"/api")

    # Remove the newarkstg-osgi-auth_version.jar.
    run('rm -rf '+core_platform_path+'/bundles/platform/newarkstg-osgi-auth_'+core_version+'.jar')

    # Remove the newarkstg-osgi-util_version.jar.
    run('rm -rf '+auth_path+'/bundles/platform/newark-osgi-util_'+core_version+'.jar')

    print('Congratulations! Deploy auth platform finished!')

def deploy_prepare():
    print('Deploy prepared. Run as root.')
    
    # Install jdk 1.8.25.
    printRed('This program require jdk 1.8.25. Make sure jdk and tomcat work out before all of your operations.')

    # Install maven.
    print('Insall maven.')
    run("wget http://apache.fayea.com/apache-mirror/maven/maven-3/3.2.3/binaries/apache-maven-3.2.3-bin.zip")
    run("unzip -q apache-maven-3.2.3-bin.zip")
    run("mv apache-maven-3.2.3 /usr/local/maven")
    run("echo 'export M2_HOME=/usr/local/maven' >> /etc/profile")
    run("echo 'export PATH=$PATH:$M2_HOME/bin' >> /etc/profile")
    run("source /etc/profile")
    run("rm -rf apache-maven-3.2.3-bin.zip apache-maven-3.2.3")
    run("mvn -version")
    
    log_path='~/logs'
    
    run('mkdir -p '+log_path+' 2>/dev/null >/dev/null')

    # Clear the install_requirement.log
    run('echo "" > '+log_path+'/install_requirement.log')

    # Install Python and fabric on the remote server.
    run("apt-get install dos2unix python python-pip python-dev subversion subversion-tools -y > "+log_path+"/install_requirement.log")
    run("pip install fabric >> "+log_path+"/install_requirement.log")

    # Install Python and fabric on the local server.
    os.system("apt-get install dos2unix python python-pip python-dev subversion subversion-tools -y > "+log_path+"/install_requirement.log")
    os.system("pip install fabric >> "+log_path+"/install_requirement.log")

    # Install sshpass.
    print('Install sshpass.')
    os.system("wget http://jaist.dl.sourceforge.net/project/sshpass/sshpass/1.05/sshpass-1.05.tar.gz")
    os.system("tar -zxf sshpass-1.05.tar.gz")
    os.system("cd sshpass-1.05 && ./configure && make && make install")

    print('Deploy prepared finished.')
