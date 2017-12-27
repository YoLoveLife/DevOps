import os, re, sys, json, subprocess,time, stat
import MySQLdb
import base64
def getAllbinlogfile():
    dbHost = '10.200.76.13'
    dbPort = 3306
    dbUser = 'root'
    dbPassword = base64.b64decode('WkJjbSQ2NDIwJkRCMjQ=')
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

if __name__ == '__main__':
    print(getAllbinlogfile())
