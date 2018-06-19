#!/bin/bash
# Author: Robin Wen
# Date: 15:49:45 01/30/2015
# Desc: All in one deploy scripts.
# Update:

####### Project configuraton section commence. #######
# Deploy project title.
project_title="Deploly project: "
# Deploy project prompt. Used for alerting user.
project_prompt="Select deploly project: "
# Deploy project type, include admin, api, and both of them.
project_options=("admin" "api" "all(admin & api)")
# Deploy project variable.
project_name=""
####### Project configuraton section conclude. #######

####### Deploy type configuration section commence. #######
# Deploy type title.
deploy_title="Deploy type: "
# Deploy type prompt. Used for alerting user.
deploy_prompt="Select deploly type: "
# Deploy type options, include dev, pro and test, which represts for develop, production, testing respectively.
deploy_options=("dev" "pro" "test")
# Deploy type variable.
deploy_type=""
####### Deploy type configuration section conclude. #######

####### Sever configuration section commence. #######
# Deploy server title.
server_title="Deploy server: "
# Deploy server prompt. Used for alerting user.
server_prompt="Select deploly server: "
# Deploy server ip options. You can add custom server ip by yourself.
server_options=("xxx.xxx.xxx.xxx(Dev)" "xxx.xxx.xxx.xxx(Test)" "xxx.xxx.xxx.xxx(Pro)")
# Deploy server variable.
server_ip=""
####### Sever configuration section conclude. #######

# Deploy project options function.
func_deploy_projecte_options()
{
   # Accept user input project name commence.
   echo "$project_title"
   PS3="$project_prompt "

   select opt in "${project_options[@]}"; do

      case "$REPLY" in

         1 ) 
            project_name=$opt
            echo $project_name
            break
         ;;
         2 ) 
            project_name=$opt
            echo $project_name
            break
         ;;
         3 ) 
            project_name=$opt
            echo $project_name
            break
         ;;
         *) echo "Invalid option. Try another one.";
            continue
         ;;
       esac
   done
   # Accept user input project name conclude.
}

# Deploy type options function.
func_deploy_type_options()
{
   # Accept user input deploy type commence.
   echo "$deploy_title"
   PS3="$deploy_prompt "

   select opt in "${deploy_options[@]}" ; do

      case "$REPLY" in
         1 ) 
            deploy_type=$opt
            echo $deploy_type
            break
         ;;
         2 ) 
            deploy_type=$opt
            echo $deploy_type
            break
         ;;
         3 ) 
            deploy_type=$opt
            echo $deploy_type
            break
         ;;
         *) echo "Invalid option. Try another one.";continue;;

       esac
   done
   # Accept user input deploy type conclude.
}

# Deploy server options function.
func_deploy_server_options()
{
   # Accept user input deploy server commence.
   echo "$server_title"
   PS3="$server_prompt "

   select opt in "${server_options[@]}" ; do

      case "$REPLY" in
   
         1 ) 
            server_ip=$opt
            echo $server_ip
            break
            ;;
         2 ) 
            server_ip=$opt
            echo $server_ip
            break
            ;;
         3 ) 
            server_ip=$opt
            echo $server_ip
            break
            ;;
       *) echo "Invalid option. Try another one.";continue;;
   
       esac
   done
   # Accept user input deploy server conclude.
}
####### Accept user's input commence. #######
while [ true ];
do
   # Accept user input project name commence.
   echo "$project_title"
   PS3="$project_prompt "

   select opt in "${project_options[@]}" ; do

      case "$REPLY" in  
         1 ) read -p "You picked $opt which is option $REPLY? (Y|y|N|n): " confirm
            if [ $confirm == "Y" ] || [ $confirm == "y" ]
            then
               project_name=$opt
               #echo $project_name
               break;
            else
               project_name=$(func_deploy_projecte_options)
               #echo $project_name
               break;
            fi
         ;;
         2 ) read -p "You picked $opt which is option $REPLY? (Y|y|N|n): " confirm
            if [ $confirm == "Y" ] || [ $confirm == "y" ]
            then
               project_name=$opt
               #echo $project_name
               break;
            else
               project_name=$(func_deploy_projecte_options)
               #echo $project_name
               break;
            fi
         ;;
         3 ) read -p "You picked $opt which is option $REPLY? (Y|y|N|n): " confirm
            if [ $confirm == "Y" ] || [ $confirm == "y" ]
            then
               project_name=$opt
               #echo $project_name
               break;
            else
               project_name=$(func_deploy_projecte_options)
               #echo $project_name
               break;
            fi
         ;;
       *) echo "Invalid option. Try another one.";continue;;
   
       esac
   done
   # Accept user input project name conclude.

   # Accept user input deploy type commence.
   echo "$deploy_title"
   PS3="$deploy_prompt "

   select opt in "${deploy_options[@]}" ; do

      case "$REPLY" in
   
         1 ) read -p "You picked $opt which is option $REPLY? (Y|y|N|n): " confirm
            if [ $confirm == "Y" ] || [ $confirm == "y" ]
            then
               deploy_type=$opt
               #echo $deploy_type
               break;
            else
               deploy_type=$(func_deploy_type_options)
               #echo $deploy_type
               break;
            fi
         ;;
         2 ) read -p "You picked $opt which is option $REPLY? (Y|y|N|n): " confirm
            if [ $confirm == "Y" ] || [ $confirm == "y" ]
            then
               deploy_type=$opt
               #echo $deploy_type
               break;
            else
               deploy_type=$(func_deploy_type_options)
               #echo $deploy_type
               break;
            fi
         ;;
         3 ) read -p "You picked $opt which is option $REPLY? (Y|y|N|n): " confirm
            if [ $confirm == "Y" ] || [ $confirm == "y" ]
            then
               deploy_type=$opt
               #echo $deploy_type
               break;
            else
               deploy_type=$(func_deploy_type_options)
               #echo $deploy_type
               break;
            fi
         ;;
         *) echo "Invalid option. Try another one.";continue;;
   
       esac
   done
   # Accept user input deploy type conclude.

   # Accept user input deploy server commence.
   echo "$server_title"
   PS3="$server_prompt "

   select opt in "${server_options[@]}" ; do

      case "$REPLY" in
   
         1 ) read -p "You picked $opt which is option $REPLY? (Y|y|N|n): " confirm
            if [ $confirm == "Y" ] || [ $confirm == "y" ]
            then
               server_ip=$opt
               #echo $server_ip
               break;
            else
               server_ip=$(func_deploy_server_options)
               #echo $server_ip
               break;
            fi
         ;;
         2 ) read -p "You picked $opt which is option $REPLY? (Y|y|N|n): " confirm
            if [ $confirm == "Y" ] || [ $confirm == "y" ]
            then
               server_ip=$opt
               #echo $server_ip
               break;
            else
               server_ip=$(func_deploy_server_options)
               #echo $server_ip
               break;
            fi
         ;;
         3 ) read -p "You picked $opt which is option $REPLY? (Y|y|N|n): " confirm
            if [ $confirm == "Y" ] || [ $confirm == "y" ]
            then
               server_ip=$opt
               #echo $server_ip
               break;
            else
               server_ip=$(func_deploy_server_options)
               #echo $server_ip
               break;
            fi
         ;;
         *) echo "Invalid option. Try another one.";continue;;
   
       esac
   done
   # Accept user input deploy server conclude.

   # Print testing information.
   #echo $project_name
   #echo $deploy_type
   #echo $server_ip

   # Handle server ip information.
   server_ip_new=`echo $server_ip | awk -F'(' '{print $1}'`

   # Estimate deploy type.
   if [ "$deploy_type" = "dev" ]
   then
      # Change the remote server ip to custom server ip.
      sed -i "s/^remote_ip=.*$/remote_ip=$server_ip_new/" ./scripts/python-auto-deploy-to-tomcat/config.conf
      # Estimate project name.
      if [ "$project_name" = "admin" ]
      then
         # Invoke the auto deploy mall admin scripts.
         bash ./scripts/auto_deploy_mall_admin.sh
      # Estimate project name.
      elif [ "$project_name" = "api" ]
      then
         # Invoke the auto deploy mall api scripts.
         bash ./scripts/auto_deploy_mall_api.sh
      else
         # Invoke the auto deploy mall admin and mall api scripts.
         bash ./scripts/auto_deploy_mall.sh
      fi
   # Estimate the deploy type.
   elif [ "$deploy_type" = "test" ]
   then
      # Change the remote server ip to custom server ip.
      sed -i "s/^remote_ip=.*$/remote_ip=$server_ip_new/" ./scripts/python-auto-deploy-to-tomcat-test/config.conf
      # Estimate project name.
      if [ "$project_name" = "admin" ]
      then
         # Invoke the auto deploy mall admin test scripts.
         bash ./scripts/auto_deploy_mall_admin_test.sh
      # Estimate project name.
      elif [ "$project_name" = "api" ]
      then
         # Invoke the auto deploy mall api test scripts.
         bash ./scripts/auto_deploy_mall_api_test.sh
      else
         # Invoke the auto deploy mall admin and mall api test scripts.
         bash ./scripts/auto_deploy_mall_test.sh
      fi
   else
      # If deploy_type is pro, which represents production, then Change the remote server ip to custom server ip.
      sed -i "s/^remote_ip=.*$/remote_ip=$server_ip_new/" ./scripts/python-auto-deploy-to-tomcat/config.conf
      # Estimate project name.
      if [ "$project_name" = "admin" ]
      then
         # Invoke the auto deploy mall admin scripts.
         bash ./scripts/auto_deploy_mall_admin.sh
      # Estimate project name.
      elif [ "$project_name" = "api" ]
      then
         # Invoke the auto deploy mall api scripts.
         bash ./scripts/auto_deploy_mall_api.sh
      else
         # Invoke the auto deploy mall admin and mall api scripts.
         bash ./scripts/auto_deploy_mall.sh
      fi
   fi

   # Print congratulation info, and exit the program.
   echo "Congratulations! Deploy $project_name of $deploy_type to $server_ip finished!"

   exit;
done
####### Accept user's input conclude. #######
