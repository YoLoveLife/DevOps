#!/bin/bash
# Author Yo
# Email YoLoveLife@outlook.com
# Time 2017-02-07 11:27
PATH=/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
VERSION="1.10.1"
PREFIX="/usr/local"
YESFLAG="0"
USER="nginx"
function Confirm()
{
cat <<_ACEOF
	Version:	${VERSION}
	Prefix:		${PREFIX}
_ACEOF
}
function IsAlready()
{
	if [ -d "/usr/local/nginx" ];then
		echo "001001002"
		exit 2
	fi
}
function Help()
{
cat <<_ACEOF
configure nginx_install bash script.
Usage $0 [OPTION]... [VAR=VALUE]...
        --help          display this help and exit
        -v,--version    modify the version of nginx.Default 1.10.1
        -f,--prefix     modify the prefix.Default /usr/local
        -u,--user       modify the user of nginx.Default nginx.
_ACEOF
}
function Avrg()
{
	ARGS=`getopt -o v:u:f: --long version:,prefix:,user: -n 'nginx_install.sh' -- "$@"`
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

if [ ! -f "nginx-${VERSION}.tar.gz" ];then
	echo "001004001"
	exit 1
fi

tar -xvzf nginx-${VERSION}.tar.gz &>/dev/null
cd nginx-${VERSION}
./configure --prefix=${PREFIX}/nginx &>/dev/null
make &>/dev/null
make install &> /dev/null

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
chown ${USER}:${USER} ${PREFIX}/nginx

Confirm > ${PREFIX}/nginx/INSTALL.info

echo "001000000"
