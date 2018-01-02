# -*-coding: utf-8-*-

import os, re, sys, json, subprocess,time, stat
import MySQLdb
import threading

reload(sys)
sys.setdefaultencoding('utf-8')

from app.models import *
from app import app, db, mail
from flask import redirect
from flask_mail import Message
from threading import Thread
from datetime import date, timedelta
import base64

base_dir = os.path.dirname(__file__)
config = app.config

mailonoff=config.get('MAIL_ON_OFF')

inception_host = config.get('INCEPTION_HOST')
inception_port = int(config.get('INCEPTION_PORT'))

inception_remote_backup_host = config.get('INCEPTION_REMOTE_BACKUP_HOST')
inception_remote_backup_port = int(config.get('INCEPTION_REMOTE_BACKUP_PORT'))
inception_remote_backup_user = config.get('INCEPTION_REMOTE_BACKUP_USER')
inception_remote_backup_password = config.get('INCEPTION_REMOTE_BACKUP_PASSWORD')



def criticalDDL(sqlContent):
    '''
    识别DROP DATABASE, DROP TABLE, TRUNCATE PARTITION, TRUNCATE TABLE等高危DDL操作，因为对于这些操作，inception在备份时只能备份METADATA，而不会备份数据！
    如果识别到包含高危操作，则返回“审核不通过”
    '''
    if re.match(
            r"([\s\S]*)drop(\s+)database(\s+.*)|([\s\S]*)drop(\s+)table(\s+.*)|([\s\S]*)truncate(\s+)partition(\s+.*)|([\s\S]*)truncate(\s+)table(\s+.*)",
            sqlContent.lower()):
        return ((
                '', '', 2, '', '不能包含【DROP DATABASE】|【DROP TABLE】|【TRUNCATE PARTITION】|【TRUNCATE TABLE】关键字！', '', '', '',
                '', ''),)
    else:
        return None


def getAlldbByDbconfig(dbConfigName):
    dbConfig = Dbconfig.query.filter(Dbconfig.name == dbConfigName).first()
    if not dbConfig:
        print("Error: 数据库配置不存在")
    dbHost = dbConfig.host
    dbPort = dbConfig.port
    dbUser = dbConfig.user
    dbPassword = base64.b64decode(dbConfig.password)
    listDb = []
    conn = None
    cursor = None

    try:
        conn = MySQLdb.connect(host=dbHost, port=dbPort, user=dbUser, passwd=dbPassword,
                               charset='utf8')
        cursor = conn.cursor()
        sql = "show databases"
        n = cursor.execute(sql)
        listDb = [row[0] for row in cursor.fetchall()
                  if row[0] not in ('information_schema', 'performance_schema', 'mysql', 'test')]
    except MySQLdb.Warning as w:
        print(str(w))
    except MySQLdb.Error as e:
        print(str(e))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.commit()
            conn.close()
    return listDb

#add by xucl to rollback
def getAllbinlogfile(dbConfigName):
    dbConfig = Dbconfig.query.filter(Dbconfig.name == dbConfigName).first()
    if not dbConfig:
        print("Error: 数据库配置不存在")
    dbHost = dbConfig.host
    dbPort = dbConfig.port
    dbUser = dbConfig.user
    dbPassword = base64.b64decode(dbConfig.password)
    listbinlog = []
    conn = None
    cursor = None

    try:
        conn = MySQLdb.connect(host=dbHost, port=dbPort, user=dbUser, passwd=dbPassword,
                               charset='utf8')
        cursor = conn.cursor()
        sql = "show binary logs"
        n = cursor.execute(sql)
	for row in cursor.fetchall():
            listbinlog.append(row[0])
    except MySQLdb.Warning as w:
        print(str(w))
    except MySQLdb.Error as e:
        print(str(e))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.commit()
            conn.close()
    return listbinlog

def mysqladvisorcheck(sqlContent, dbConfigName, dbUse):
    dbConfig = Dbconfig.query.filter(Dbconfig.name == dbConfigName).first()
    if not dbConfig:
        print("Error: 数据库配置不存在")
    dbHost = dbConfig.host
    dbPort = dbConfig.port
    dbUser = dbConfig.user
    dbPassword = base64.b64decode(dbConfig.password)
    p=subprocess.Popen(base_dir+'/sqladvisor/sqladvisor -h '+str(dbHost)+' -P '+str(dbPort)+' -u '+str(dbUser)+' -p '+str(dbPassword)+' -d '+str(dbUse)+' -q "'+str(sqlContent)+'" -v 1', stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    if stdout:
        return stdout
    return stderr
def sqlautoReview(sqlContent, dbConfigName, isBackup=False):
    '''
    将sql交给inception进行自动审核，并返回审核结果。
    '''
    dbConfig = Dbconfig.query.filter(Dbconfig.name == dbConfigName).first()
    if not dbConfig:
        print("Error: 数据库配置不存在")
    dbHost = dbConfig.host
    dbPort = dbConfig.port
    dbUser = dbConfig.user
    dbPassword = base64.b64decode(dbConfig.password)

    # 这里无需判断字符串是否以；结尾，直接抛给inception enable check即可。
    # if sqlContent[-1] != ";":
    # sqlContent = sqlContent + ";"
    criticalddl = config.get('CRITICAL_DDL_ON_OFF')
    if criticalddl == "ON":
        criticalDDL_check = criticalDDL(sqlContent)
    else:
        criticalDDL_check = None
    if criticalDDL_check is not None:
        result = criticalDDL_check
    else:
        sql = "/*--user=%s;--password=%s;--host=%s;--enable-check=1;--port=%s;*/\
              inception_magic_start;\
              %s\
              inception_magic_commit;" % (dbUser, dbPassword, dbHost, str(dbPort), sqlContent)
        result = fetchall(sql, inception_host, inception_port, '', '', '')

    return result


def executeFinal(id):
    '''
    将sql交给inception进行最终执行，并返回执行结果。
    '''
    work = Work.query.filter(Work.id == id).first()
    if work.status == 3 or work.status == 0:
        return redirect('audit_work')
    work.status = 3
    work.man_review_time = datetime.now()
    db.session.commit()
    dbConfig = Dbconfig.query.filter(Dbconfig.name == work.db_config).first()
    if not dbConfig:
        print("Error: 数据库配置不存在")
    dbHost = dbConfig.host
    dbPort = dbConfig.port
    dbUser = dbConfig.user
    dbPassword = base64.b64decode(dbConfig.password)

    strBackup = ""
    if work.backup == True:
        strBackup = "--enable-remote-backup;"
    else:
        strBackup = "--disable-remote-backup;"

    # 根据inception的要求，执行之前最好先split一下
    sqlSplit = "/*--user=%s; --password=%s; --host=%s; --enable-execute;--port=%s; --enable-ignore-warnings;--enable-split;*/\
             inception_magic_start;\
             %s\
             inception_magic_commit;" % (dbUser, dbPassword, dbHost, str(dbPort), work.sql_content)
    splitResult = fetchall(sqlSplit, inception_host, inception_port, '', '', '')
    tmpList = []

    # 对于split好的结果，再次交给inception执行.这里无需保持在长连接里执行，短连接即可.
    for splitRow in splitResult:
        sqlTmp = splitRow[1]
        sqlExecute = "/*--user=%s;--password=%s;--host=%s;--enable-execute;--port=%s; --enable-ignore-warnings;%s*/\
                    inception_magic_start;\
                    %s\
                    inception_magic_commit;" % (dbUser, dbPassword, dbHost, str(dbPort), strBackup, sqlTmp)

    executeResult = fetchall(sqlExecute, inception_host, inception_port, '', '', '')
    tmpList.append(executeResult)

    # 二次加工一下，目的是为了和sqlautoReview()函数的return保持格式一致，便于在detail页面渲染.
    finalStatus = 0
    finalList = []
    for splitRow in tmpList:
        for sqlRow in splitRow:
            # 如果发现任何一个行执行结果里有errLevel为1或2，并且stagestatus列没有包含Execute Successfully字样，则判断最终执行结果为有异常.
            if (sqlRow[2] == 1 or sqlRow[2] == 2) and re.match(r"\w*Execute Successfully\w*", sqlRow[3]) is None:
                finalStatus = 4
            finalList.append(list(sqlRow))

            jsonResult = json.dumps(finalList)
            work.execute_result = jsonResult
            work.finish_time = datetime.now()
            work.status = finalStatus
            db.session.commit()



def getRollbackSqlList(workId):
    work = Work.query.filter(Work.id == workId).first()
    listExecuteResult = json.loads(work.execute_result)
    listBackupSql = []
    for row in listExecuteResult:
        # 获取backup_dbname
        if row[8] == 'None':
            continue;
        backupDbName = row[8]
        sequence = row[7]
        opidTime = sequence.replace("'", "")
        sqlTable = "select tablename from %s.$_$Inception_backup_information$_$ where opid_time='%s';" % (
        backupDbName, opidTime)
        listTables = fetchall(sqlTable, inception_remote_backup_host, inception_remote_backup_port,
                                    inception_remote_backup_user, inception_remote_backup_password, '')
        if listTables is None or len(listTables) != 1:
            print("Error: returned listTables more than 1.")

        tableName = listTables[0][0]
        sqlBack = "select rollback_statement from %s.%s where opid_time='%s'" % (backupDbName, tableName, opidTime)
        listBackup = fetchall(sqlBack, inception_remote_backup_host, inception_remote_backup_port,
                                    inception_remote_backup_user, inception_remote_backup_password, '')
        if listBackup is not None and len(listBackup) != 0:
            for rownum in range(len(listBackup)):
                listBackupSql.append(listBackup[rownum][0])
    return listBackupSql

def getSlowLogList(dbId, hour):
    dbDt=(datetime.now()-timedelta(hours=hour)).strftime('%Y-%m-%d %H:%M:%S')
    dbConfig=Dbconfig.query.filter(Dbconfig.id == dbId).first()

    sql="select sql_text,count(sql_text) c from mysql.slow_log where start_time >= '%s' group by sql_text order by c asc limit 30" % (dbDt)
    slowlogList=fetchall(sql, dbConfig.host, dbConfig.port,
                         dbConfig.user, base64.b64decode(dbConfig.password), '')
    return slowlogList

def getdbReport(dbId, mem):
    dbConfig = Dbconfig.query.get(dbId)
    p = subprocess.Popen('perl '+base_dir+'/mysqltuner.pl --host '+str(dbConfig.host)+' --user '+str(dbConfig.user)+' --pass '+str(base64.b64decode(dbConfig.password))+' --port '+str(dbConfig.port)+' --forcemem '+str(mem), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    dbReport=''
    if stdout:
        stdout = stdout.replace('[\x1b[0;34m', '[')
        stdout = stdout.replace('\x1b[0m]', ']')
        stdout = stdout.replace('[\x1b[0;32m', '[')
        stdout = stdout.replace('[\x1b[0;31m', '[')
        stdout = stdout.replace('\x1b[0;32m', ' ')
        stdout = stdout.replace('\x1b[0m\x1b[0;32m', ' ')
        stdout = stdout.replace('\x1b[0m', '')
        stdout = stdout.replace('\x1b[0;31m', '')
        dbReport = stdout
    else:
        print u'错误：'+stderr
    return dbReport




def fetchall(sql, paramHost, paramPort, paramUser, paramPasswd, paramDb):
    '''
    封装mysql连接和获取结果集方法
    '''
    result = None
    conn = None
    cur = None
    sql = sql.encode('utf-8')

    try:
        conn = MySQLdb.connect(host=paramHost, user=paramUser, passwd=paramPasswd, db=paramDb, port=paramPort)
        conn.set_character_set('utf8')
        cur = conn.cursor()
        ret = cur.execute(sql)
        result = cur.fetchall()
        result = result
    except MySQLdb.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
    return result

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
def send_email(subject, body, receiver):
    msg = Message(subject, recipients=[receiver])
    msg.html = body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return u'发送成功'
def checksqladvisor():
    sqladvisordir = base_dir + '/sqladvisor'
    if not os.path.exists(sqladvisordir):
        os.makedirs(sqladvisordir)
    if os.path.exists(sqladvisordir+'/sqladvisor'):
        installtime = time.localtime(os.path.getmtime(sqladvisordir + '/sqladvisor'))
        installtime = time.strftime('%Y-%m-%d %H:%M:%S', installtime)
        return u'SQLAdvisor已安装,安装时间：' +str(installtime)
    else:
        return u'SQLAdvisor未安装'

def stoptimer(work):
    for item in threading.enumerate():
        if item.name == work.name:
            item.cancel()
def starttimer(work, executetime):
    t = threading.Timer(executetime, executeFinal, [work.id])
    t.name = work.name
    t.setDaemon(True)
    t.start()




