#!/bin/bash
#Time 2017-1-13 15:36
#Author Yo
PATH=/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
PREFIX=/usr/local
BASEDIR=${PREFIX}/redis
LOGFILE="${BASEDIR}/redis.log"
DATADIR="${BASEDIR}/data/"
USER="redis"
function Help()
{
cat <<_ACEOF
configure redis_remove bash script.
Usage $0 [OPTION]... [VAR=VALUE]...
	--help	display this help and exit
        -f,--prefix     modify the prefix.Default /usr/local
	    -l,--logfile    modify the logfile of redis-server.Default /usr/local/redis/redis.log
        -d,--datadir	modify the datadir of redis-server.Default /usr/local/redis/data/
        -u,--user       modify the user of redis.Default redis
_ACEOF
}
function Avrg()
{
	ARGS=`getopt -o f:d:l:u: --long prefix:,datadir:,logfile:,user: -n 'redis_remove.sh' -- "$@"`
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
			-l|--logfile)
				LOGFILE=$2
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

Avrg $@
DIRNAME=${PREFIX}/redis
rm -rf ${LOGFILE} ${DATADIR} ${DIRNAME}

echo "001000000"

