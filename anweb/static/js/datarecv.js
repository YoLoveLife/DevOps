/**
 * @Time: 2017-4-18
 * @Author: Yo
 * @Email: YoLoveLIfe@outlook.com
 * */

/**
 * @Type: Object
 * @Desc: $.dataRecv is the data-recv for the app.
 * */
$.dataRecv={};

/**
* @Type: Object
* @Desc: all options in this project.
* */
$.dataRecv.options={
    prefix:'/usr/local',
    redis_port:'6379',
    redis_passwd:'000000',
    redis_version:'NULL',
    mysql_passwd:'000000',
    mysql_datadir:'/storage/mysql',
    mysql_port:'3306',
    mysql_socket:'/tmp/mysql.sock',
    java_version:'NULL',
    tomcat_version:'NULL',
    nginx_version:'NULL'
}

/**
 * @Type: Function
 * @Return: true/false
 * @Usage: $.dataRecv.lofinValidate(username,userpasswd)
 * @Desc: Ajax.DataBase search the login user
 * */
$.dataRecv.loginValidate=function(username,userpasswd){
    if(1){
        return true;
    }else{
        return false;
    }
}
/*----------TimeLine Page Data Js---------*/
/**
 * @Type: Function
 * @Return: history_list
 * @Usage: $.dataRecv.historyGetBkData()
 * @Desc: Get the all History from the database.json data
 * */
$.dataRecv.historyGetBkData=function(){
    return $.devEops.ajaxBkDataAsync('historyget/',false,'GET',{})
}

/*-----------Group Page Data JS-----------*/
/**
 * @Type: Function
 * @Return: group_list
 * @Usage: $.dataRecv.groupGetBkData()
 * @Desc: Get the All Group from the database.json data.
 * */
$.dataRecv.groupGetBkData=function(){
    return $.devEops.ajaxBkDataAsync('groupsearch/',false,"GET",{});
}

/**
 * @Type: Function
 * @Return: null
 * @Usage: $.dataRecv.groupModifyDatabase(group)
 * @Desc: group is a object.
 * */
$.dataRecv.groupModifyDatabase=function(postdata) {
    //var postdata={"groupid":group.groupid,"groupname":group.groupname,"groupremark":group.groupremark};
    $.devEops.ajaxBkDataAsync('groupmodify/',false,"POST",postdata);
}


/*-----------Host Page Data JS-----------*/
/**
 * @Type: Function
 * @Return: host_list
 * @Usage: $.dataRecv.hostGetBkData(group_id)
 * @Desc: Get the host list for group_id
 * */
$.dataRecv.hostGetBkData=function(group_id){
    var list=[];
    var postdata={'id':group_id};
    list=$.devEops.ajaxBkDataAsync('hostsearch/',false,'GET',postdata);
    return list;
}
/**
 * @Type: Function
 * @Argv: ipaddress,groupid
 * @Return: Null
 * @Usage: $.dataRecv.hostUpdateInfo(ipaddress,groupid)
 * @Desc:
 * */
$.dataRecv.hostUpdateInfo=function(ipaddress,groupid){
    postdata={'ipaddress':ipaddress,'group':groupid};
    $.devEops.ajaxBkDataAsync('hostupdate/',true,'GET',postdata);
}

/*-----------Batch Page Data JS-----------*/
/**
 * @Type: Function
 * @Arvg: softname - name of soft
 * @Return: version_list
 * @Usage: $.dataRecv.batchGetSoftVersion(softname)
 * @Desc: Get the soft version
 * */
$.dataRecv.batchGetSoftVersion=function(softname){
    var list=[];
    postdata={'appname':softname};
    list=$.devEops.ajaxBkDataAsync('softversion/',false,'GET',postdata);
    return list;
}

/**
 * @Type: Function
 * @Argv: Null
 * @Return: Null
 * @Usage: $.dataRecv.batchRedis()
 * */
$.dataRecv.batchRedis=function(iplist,redisversion,redisprefix,redisport,redispasswd,redisdatadir){
    var postdata={'iplist':iplist,'version':redisversion,'prefix':redisprefix,'port':redisport,'passwd':redispasswd,'datadir':redisdatadir};
    $.devEops.ajaxBkDataAsync('batchredis/',true,'POST',postdata);
}

/**
 * @Type: Function
 * @Argv: Null
 * @Return: Null
 * @Usage: $.dataRecv.batchMySQL()
 * */
$.dataRecv.batchMySQL=function(iplist,mysqlversion,mysqlprefix,mysqlpasswd,mysqldatadir,mysqlport,mysqlsocket){
    var postdata={'iplist':iplist,'version':mysqlversion,'prefix':mysqlprefix,'datadir':mysqldatadir,'port':mysqlport,'passwd':mysqlpasswd,'socket':mysqlsocket};
    $.devEops.ajaxBkDataAsync('batchmysql/',true,'POST',postdata);
}

/**
 * @Type: Function
 * @Argv: Null
 * @Return: Null
 * @Usage: $.dataRecv.batchTomcat()
 * */
$.dataRecv.batchTomcat=function (iplist,javaversion,javaprefix,tomcatversion,tomcatprefix) {
    var postdata={'iplist':iplist,'javaversion':javaversion,'javaprefix':javaprefix,'tomcatversion':tomcatversion,'tomcatprefix':tomcatprefix};
    $.devEops.ajaxBkDataAsync('batchtomcat/',true,'POST',postdata);
}

/**
 * @Type: Function
 * @Argv: Null
 * @Return: Null
 * @Usage: $.dataRecv.batchNginx()
 * */
$.dataRecv.batchNginx=function(iplist,nginxversion,nginxprefix,nginxpid){
    var postdata={'iplist':iplist,'version':nginxversion,'prefix':nginxprefix,'pid':nginxpid};
    $.devEops.ajaxBkDataAsync('batchnginx/',true,'POST',postdata);
}

/**
 * @Type: Function
 * @Argv: Null
 * @Return: Null
 * @Usage: $.dataRecv.confGet()
 * */
$.dataRecv.confGet=function(iplist,cnf){
    var postdata={'iplist':iplist,'cnf':cnf};
    var conf=$.devEops.ajaxBkDataAsync('confget/',false,'GET',postdata);
    return conf;
}

/**
 * @Type: Function
 * @Argv: Null
 * @Return: Null
 * @Usage:$.dataRecv.confModify()
 * */
$.dataRecv.confModify=function (iplist,tmpconf,newstr,cnf) {
    var postdata={'iplist':iplist,'tmp':tmpconf,'newstr':newstr,'cnf':cnf};
    $.devEops.ajaxBkDataAsync('confmodify/',false,'GET',postdata);
}

/*-----------Control Page Data JS-----------*/
/**
 * @Type: Function
 * @Argv: appname - name of app
 * @Return: NUll
 * @Usage: $.dataRecv.appListGet()
 * */
$.dataRecv.appListGet=function(appname){
    var postdata={'appname':appname};
    var list=$.devEops.ajaxBkDataAsync('appget/',false,'GET',postdata);
    return list;
}

/**
 * @Type: Function
 * @Argv: hostid - hostid;type- 1start:2stop:3restart;appname - name of app
 * @Return: Null
 * @Usage: $.dataRecv.controlApp(hostid,type,appname)
 * */
$.dataRecv.controlApp=function(hostid,type,appname){
    var postdata={'hostid':hostid,'type':type,'appname':appname};
    console.log(postdata);
    $.devEops.ajaxBkDataAsync('appcontrol/',false,'GET',postdata);
}
