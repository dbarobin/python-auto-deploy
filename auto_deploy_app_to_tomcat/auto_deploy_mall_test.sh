#!/bin/bash
# Author: Robin Wen
# Date: 14:13:27 2015-01-29
# Desc: Auto deploy test env of MallAdmin and MallPlatform
# Attention: You must make equivalent ssh authentication for user.
# Update: Add kill the tomcat-test process at 10:15:09 2015-01-30

# Origin Mall Admin Path.
origin_admin_path=YOUR_PATH

# Origin Mall Platform Path.
origin_api_path=YOUR_PATH

# Test Mall Admin Path.
test_admin_path=YOUR_PATH

# Test Mall Platform Path.
test_api_path=YOUR_PATH

# Test Tomcat Home.
test_tomcat_home=YOUR_PATH

# Test Tomcat.
test_tomcat=YOUR_PATH


echo "Remove the Old Test Mall Project."
# Remove the Old Mall Admin of Test.
ssh YOUR_SERVER_USER_NAME@YOUR_SERVER_IP "rm -rf $test_admin_path"
# Remove the Old Mall Platform of Test.
ssh YOUR_SERVER_USER_NAME@YOUR_SERVER_IP "rm -rf $test_api_path"
sleep 2
echo "Remove the Old Test Mall Project Finished!"

echo "Copy the Origin Mall Project to Test Mall Project."
# Copy the Origin Mall Admin to Test Mall Admin.
ssh YOUR_SERVER_USER_NAME@YOUR_SERVER_IP "cp -r $origin_admin_path $test_admin_path"
# Copy the Origin Mall Api to Test Mall Api.
ssh YOUR_SERVER_USER_NAME@YOUR_SERVER_IP "cp -r $origin_api_path $test_api_path"
sleep 3
echo "Copy the Origin Mall Project to Test Mall Project Finished!"

echo "Update the Database Setting of Test Mall Project."
# Update the Database Setting of Test Mall Admin.
ssh YOUR_SERVER_USER_NAME@YOUR_SERVER_IP "sed -i 's/YOUR_SERVER_USER_NAME/YOUR_SERVER_USER_NAME_test/g' $test_admin_path/WEB-INF/db.properties"
# Update the Database Setting of Test Mall Api.
ssh YOUR_SERVER_USER_NAME@YOUR_SERVER_IP "sed -i 's/YOUR_SERVER_USER_NAME/YOUR_SERVER_USER_NAME_test/g' $test_api_path/WEB-INF/db.properties"
sleep 1
echo "Update the Database Setting of Test Mall Project Finished!"

# Kill the Tomcat-Test process.
ssh YOUR_SERVER_USER_NAME@YOUR_SERVER_IP "ps -ef | grep tomcat-test | grep -v grep | cut -c 9-15 | xargs kill -9"

# Restart Test Tomcat Remotely.
