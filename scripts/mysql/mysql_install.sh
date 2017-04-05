#!/bin/bash
#Time 2017-1-9 20:42
#Author Yo
PATH=/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
VERSION="10.1.12"
PREFIX=/usr/local
SYSTEM=`uname -a |awk '{print $13}'`
USER=mysql
BASEDIR=${PREFIX}/mysql
DATADIR=${BASEDIR}/data/
SHELL=/sbin/nologin
function Confirm()
{
cat <<_ACEOF
	Version:	${VERSION}
	Prefix:		${PREFIX}
	User:		${USER}
	Datadir:	${DATADIR}
_ACEOF
}
function IsAlready()
{
	if [ -d "/usr/local/mysql" ];then
		echo "已安装"
		exit 2
	fi
}
function Help()
{
cat <<_ACEOF
configure nginx_install bash script.
Usage $0 [OPTION]... [VAR=VALUE]...
	--help		display this help and exit
	-v,--version	modify the version of mysql.Default 10.1.12
	-f,--prefix	modify the prefix.Default /usr/local
	-u,--user	modify the user of mysql.Default mysql 
	-d,--datadir	modify the datadir of mysql.Default /usr/local/mysql/data
	-y		answer question with yes
_ACEOF
}
function Avrg()
{
	ARGS=`getopt -o yv:f:u:d: --long version:,prefix:,user:,datadir: -n 'mysql_install' -- "$@"`
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
			-d|--datadir)
				DATADIR=$2
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
				echo "参数错误"
				exit 2
				;;
		esac
	done	
}
IsAlready

Avrg $@
FILENAME=mariadb-${VERSION}-linux-${SYSTEM}

tar -xvzf ${FILENAME}.tar.gz -C ${PREFIX} &>/dev/null

mv ${PREFIX}/${FILENAME}/ ${BASEDIR}
if [ `cat /etc/passwd |grep mysql|wc -l` == "0" ];then
	groupadd ${USER}
	useradd -s ${SHELL} -g ${USER} ${USER}
fi

#Confirm > ${BASEDIR}/INSTALL.info

mkdir -p ${DATADIR}
chown -R ${USER}:${USER} ${DATADIR}
chown -R ${USER}:${USER} ${BASEDIR}

${BASEDIR}/scripts/mysql_install_db --basedir=${BASEDIR} --datadir=${DATADIR} --user=${USER} &>/dev/null

cp ${BASEDIR}/support-files/mysql.server /etc/init.d/mysqld
cp ${BASEDIR}/bin/mysql /usr/bin/mysql
cp ${BASEDIR}/support-files/my-large.cnf /etc/my.cnf
/sbin/chkconfig --add mysqld
echo "002000000"
