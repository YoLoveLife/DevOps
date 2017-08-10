#!/bin/bash
# Author Yo
# Email YoLoveLife@outlook.com
# Time 2017-04-05 16:19
ONLINE=`ps aux |grep mysql |wc -l`
if [ "${ONLINE}" == "3" ];then
    echo "1"
else
    echo "0"
fi