#!/bin/bash

# Author: Robin Wen
# Date: 18:35:26 2014-12-12
# Desc: Restart the tomcat.

# Java Home.
export JAVA_HOME=YOUR_JAVA_HOME
# CATALINA Home.
export CATALINA_HOME=YOUR_CATALINA_HOME

# Execute the shutdown.sh scripts.
YOUR_JAVA_HOME/bin/shutdown.sh
# Execute the startup.sh scripts.
YOUR_JAVA_HOME/bin/startup.sh
