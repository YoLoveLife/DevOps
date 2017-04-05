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
		echo "已安装"
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
		echo "参数错误"
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
				echo "参数错误"
				exit 2	
			esac
	done
}
IsAlready

Avrg $@

tar -xvzf redis-${VERSION}.tar.gz -C ${PREFIX} &>/dev/null
mv ${PREFIX}/redis-${VERSION} ${PREFIX}/redis
BASEDIR=${PREFIX}/redis

#Confirm > ${PREFIX}/redis/INSTALL.info

make --directory=${BASEDIR} &>/dev/null

mkdir ${BASEDIR}/bin
find ${BASEDIR}/src -perm -u=x -type f -exec ln -s {} ${BASEDIR}/bin \;
echo "001000000"
