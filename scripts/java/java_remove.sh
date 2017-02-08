#!/bin/bash
#Time 2017-2-6 17:24
#Author Yo
PATH=/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
PREFIX=/usr/local
function Confirm()
{
cat <<_ACEOF
	Prefix:		${PREFIX}
_ACEOF
}
function Help()
{
cat <<_ACEOF
configure java_install bash script.
Usage $0 [OPTION]... [VAR=VALUE]...
	--help	    	display this help and exit
	-f,--prefix	    modify the prefix.Default /usr/local
	-y		        answer question with yes
_ACEOF
}
function Avrg()
{
	ARGS=`getopt -o yf: --long prefix: -n 'java_remove' -- "$@"`
	if [ ! $? -eq 0 ];then
		echo "003002002"
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
			-y)
				YESFLAG="1"
				shift
				;;
			--)
				shift
				break
				;;
			*)
				echo "003002002"
				exit 2
				;;
		esac
	done
}
if [ "$1" == "--help" ];then
	Help
	exit 2
fi
Avrg $@

rm -rf ${PREFIX}/java

echo "003000000"
