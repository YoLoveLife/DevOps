#!/bin/bash
# Author Yo
# Email YoLoveLife@outlook.com
# Time 2017-02-07 09:09
PATH=/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
VERSION="7.0.72"
PREFIX="/usr/local"
YESFLAG="0"
function Confirm()
{
cat <<_ACEOF
	Version:	${VERSION}
	Prefix:		${PREFIX}
_ACEOF
}
function IsAlready()
{
	if [ -d "/usr/local/tomcat" ];then
		echo "004001002"
		exit 2
	fi
}
function Help()
{
cat <<_ACEOF
configure tomcat_install bash script.
Usage $0 [OPTION]... [VAR=VALUE]...
        --help          display this help and exit
        -v,--version    modify the version of tomcat.Default 3.2.4
        -f,--prefix     modify the prefix.Default /usr/local
_ACEOF
}
function Avrg()
{
	ARGS=`getopt -o v:u:f: --long version:,prefix: -n 'tomcat_install.sh' -- "$@"`
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

tar -xvzf apache-tomcat-${VERSION}.tar.gz -C ${PREFIX} &>/dev/null
mv ${PREFIX}/apache-tomcat-${VERSION} ${PREFIX}/tomcat
BASEDIR=${PREFIX}/redis

#Confirm > ${PREFIX}/tomcat/INSTALL.info

echo "004000000"