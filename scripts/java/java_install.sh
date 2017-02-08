#!/bin/bash
#Time 2017-1-9 20:42
#Author Yo
PATH=/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
VERSION="7u79"
PREFIX=/usr/local
SYSTEM=`uname -a |awk '{print $13}'`
function Confirm()
{
cat <<_ACEOF
	Version:	${VERSION}
	Prefix:		${PREFIX}
_ACEOF
}
function IsAlready()
{
	if [ -d "/usr/local/java" ];then
		echo "003001002"
		exit 2
	fi
}
function Help()
{
cat <<_ACEOF
configure java_install bash script.
Usage $0 [OPTION]... [VAR=VALUE]...
	--help	    	display this help and exit
	-v,--version	modify the version of java.Default 7u79
	-f,--prefix	    modify the prefix.Default /usr/local
	-y		        answer question with yes
_ACEOF
}
function Avrg()
{
	ARGS=`getopt -o yv:f: --long version:,prefix: -n 'java_install' -- "$@"`
	if [ ! $? -eq 0 ];then
		echo "003002002"
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
			-y)
				YESFLAG="1"
				shift
				;;
			--)
				shift
				break
				;;
			*)
				echo "002002002"
				exit 2
				;;
		esac
	done
}
BVERSION=`echo ${VERSION}|cut -d"u" -f1`
MVERSION=`echo ${VERSION}|cut -d"u" -f2`
IsAlready
if [ "$1" == "--help" ];then
	Help
	exit 2
fi
Avrg $@
FILENAME=jdk-${VERSION}-linux-x64
if [ -f "./${FILENAME}" ];then
	echo "003004001"
	exit 1
fi
tar -xvzf ${FILENAME}.tar.gz -C ${PREFIX} &>/dev/null
BASEDIR=${PREFIX}/java

mv ${PREFIX}/jdk1.${BVERSION}.0_${MVERSION}/ ${BASEDIR}
Confirm > ${BASEDIR}/INSTALL.info

#find ${BASEDIR}/bin -perm -u=x -type f -exec ln -s {} /usr/bin \;
find ${BASEDIR}/bin -perm -u=x -type f -exec cp {} /usr/bin \;
echo "003000000"
