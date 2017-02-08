#!/bin/bash
#Time 2017-1-13 15:36
#Author Yo
PATH=/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
PREFIX=/usr/local
BASEDIR=${PREFIX}/mysql
DATADIR="${BASEDIR}/data/"
USER="mysql"
CONF=/etc/my.cnf
function Help()
{
cat <<_ACEOF
configure mysql_remove bash script.
Usage $0 [OPTION]... [VAR=VALUE]...
	--help	display this help and exit
        -f,--prefix     modify the prefix.Default /usr/local
        -d,--datadir	modify the datadir of mysql-server.Default /usr/local/mysql/data/
        -u,--user       modify the user of mysql.Default mysql
	    -c,--conf	modify the conf of mysql.Default /etc/my.cnf
_ACEOF
}
function Avrg()
{
	ARGS=`getopt -o f:d:u:c: --long prefix:,datadir:,user:,conf: -n 'mysql_remove' -- "$@"`
	if [ ! $? -eq 0 ];then
		echo "001002002"
		exit 2
	fi
	eval set -- "${ARGS}"

	while true
	do
		case "$1" in
			-f|--prefix)
				PREFIX=$2
				shift 2
				;;
			-d|--datadir)
				DATADIR=$2
				shift 2
				;;
			-u|--user)
				USER=$2
				shift 2
				;;
			-c|--conf)
				CONF=$2
				shift 2
				;;
			--)
				shift
				break
				;;
			*)
				#Help
				echo "001002002"
				exit 2	
			esac
	done
}
if [ "$1" == "--help" ];then
	Help
	exit 2
fi
Avrg $@
BASEDIR=${PREFIX}/mysql
if [ `ps -ef |grep mysql|wc -l` == "3" ];then
	echo "002005002"
	exit 
fi
rm -rf ${DATADIR} ${BASEDIR} ${CONF}
if [ "`cat /etc/passwd|grep ${USER}|wc -l`" == "1" ];then
	userdel -r ${USER}
fi

/sbin/chkconfig --del mysqld
rm -rf /etc/init.d/mysqld
if [ "$?" == "0" ];then
	echo "002000000"
fi
