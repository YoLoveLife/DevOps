#!/bin/bash
# Author Yo
# Email YoLoveLife@outlook.com
# Time 2017-03-07 08:56
ONLINE=`ps aux |grep redis-server|wc -l`
if [ "${ONLINE}" == "2" ];then
    echo "1"
else
    echo "0"
fi