#!/bin/bash
#Install Redis
#Author Yo
PATH=/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
VERSION="3.2.4"
PREFIX="/usr/local"
SYSTEM=`uname -a |awk '{print $13}'`
USER="redis"
SHELL="/sbin/nologin"
YESFLAG="0"
function Confirm()
{
cat <<_ACEOF
	Version:	${VERSION}
	Prefix:		${PREFIX}
	User:		${USER}
_ACEOF
}
function IsAlready()
{
	if [ -d "/usr/local/redis" ];then
		echo "001001002"
		exit 2
	fi
}
function Help()
{
cat <<_ACEOF
configure redis_install bash script.
Usage $0 [OPTION]... [VAR=VALUE]...
        --help          display this help and exit
        -v,--version    modify the version of redis.Default 3.2.4
        -f,--prefix     modify the prefix.Default /usr/local
        -u,--user       modify the user of redis.Default redis
_ACEOF
}
function Avrg()
{
	ARGS=`getopt -o v:u:f:u: --long version:,prefix:,user: -n 'redis_install.sh' -- "$@"`
	if [ ! $? -eq 0 ];then
		echo "001002002"
		exit 2
	fi
	eval set -- "${ARGS}"

	while true
	do
		case "$1" in
			-v|--version)
				VERSION=$2
				shift 2
				;;
			-f|--prefix)
				PREFIX=$2
				shift 2
				;;
			-u|--user)
				USER=$2
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
IsAlready
if [ "$1" == '--help' ];then
	Help
	exit 2
fi
Avrg $@

ISGCC=`rpm -qa |grep ^gcc-[1-9].*\.${SYSTEM}|wc -l`
ISMAKE=`rpm -qa|grep ^make.*\.${SYSTEM}|wc -l`
if [ ! `id -u` -eq "0" ];then
	echo "001005003"
	exit 1
fi
if [ "${ISGCC}" == "0" ];then
	echo "001003002"
	exit 1
fi

if [ "${ISMAKE}" == "0" ];then
	echo "001003002"
	exit 1
fi
if [ ! -f "redis-${VERSION}.tar.gz" ];then
	echo "001004001"
	exit 1
fi
tar -xvzf redis-${VERSION}.tar.gz -C ${PREFIX} &>/dev/null
mv ${PREFIX}/redis-${VERSION} ${PREFIX}/redis
BASEDIR=${PREFIX}/redis

groupadd ${USER}
if [ "$?" != "0" ];then
	echo "001006001"
	exit 1
fi
useradd -s ${SHELL} -g ${USER} ${USER}
if [ "$?" != "0" ];then
	echo "001006001"
	exit 1
fi
chown -R ${USER}:${USER} $BASEDIR
Confirm > ${PREFIX}/redis/INSTALL.info 


make --directory=${BASEDIR} &>/dev/null 
if [ ! $? -eq 0 ];then
	echo "001007003"
	exit 2
fi

mkdir ${BASEDIR}/bin
find ${BASEDIR}/src -perm -u=x -type f -exec cp {} ${BASEDIR}/bin \;
echo "001000000"
