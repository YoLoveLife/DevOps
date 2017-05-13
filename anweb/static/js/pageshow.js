/**
 * @Time: 2017-4-19
 * @Author: Yo
 * @Email: YoLoveLIfe@outlook.com
 * @Desc: Function for DOM
 * */

/**
 * @Type: Object
 * @Desc: $.pageShow is the page-show for the app.
 * */
$.pageShow={};

/*----------TimeLine Page Data JS---------*/
/**
 * @Type: Function
 * @Return: Null
 * @Usage: $.pageShow.timeLineInit()
 * @Desc: Function for init the timeline page.
 * */
$.pageShow.timeLineInit=function(){
    var list=$.dataRecv.historyGetBkData();
    $.pageShow.timeLineDataFlush(list);
}

/**
 * @Type: Function
 * @Argv: list - list of timeLine
 * @Return: Null
 * @Usage: $.pageShow.timeLineDataFlush(list)
 * */
/*
               <li class="time-label"><span>Start</span></li>
                <li>
                    <i class="fa fa-envelope"></i>
                    <div class="timeline-item">
                        <span class="time"><i class="fa fa-clock-o"></i> 12:05</span>

                        <h3 class="timeline-header"><a href="#">Support Team</a> sent you an email</h3>

                        <div class="timeline-body">
                            Etsy doostang zoodles disqus groupon greplin oooj voxy zoodles,
                            weebly ning heekya handango imeem plugg dopplr jibjab, movity
                            jajah plickers sifteo edmodo ifttt zimbra. Babblely odeo kaboodle
                            quora plaxo ideeli hulu weebly balihoo...
                        </div>
                        <div class="timeline-footer">
                        </div>
                    </div>
                </li>
                <li>
                    <i class="fa fa-clock-o bg-gray"></i>
                </li>
* */
$.pageShow.timeLineDataFlush=function(history_list){
    var string="<li class='time-label'></li>";
    var end="<li><i class='fa fa-clock-o'></i></li>";
    var item="";
    var title,state;
    for(var i in history_list){
        for(var j=history_list[i].length-1;j>=0;j--){
            var temp=JSON.parse(history_list[i][j]);
            if(parseInt(temp['oper_type'])>=1&&parseInt(temp['oper_type'])<=2){
                title='Manager Operation';
            }else{
                title='Ansible Operation';
            }
            if(parseInt(temp['oper_result'])==1)
            {
                state="<span class='label label-primary'>Running</span>";
            }else if(parseInt(temp['oper_result'])==2){
                state="<span class='label label-success'>Done</span>";
            }else{
                state="<span class='label label-danger'>Error</span>";
            }
            item="<li><i class='fa fa-envelope'></i><div class='timeline-item'><span class='time'><i class='fa fa-clock-o'></i>"+temp['oper_time']+"</span><h3 class='timeline-header'><a>"+title+"</a></h3><div class='timeline-body'>"+temp['oper_info']+"</div><div class='timeline-footer'>"+state+"</div></div></li>";
            string+=item;
        }
    }
    string=string+end;
    $('.timeline').html(string);
}

/*-----------Group Page Data JS-----------*/
/**
 * @Type: Function
 * @Return: Null
 * @Usage: $.pageShow.groupInit()
 * @Desc: Function for init the group page.When you want to flush the page.
 * */
$.pageShow.groupInit=function(){
    var list=$.dataRecv.groupGetBkData();
    $.pageShow.groupTabDataFlush(list);
}

/**
 * @Type: Function
 * @Return: Null
 * @Usage: $.pageShow.groupTabDataFlush(group_list)
 * @Desc: group_list - js list of the group
 * */
$.pageShow.groupTabDataFlush=function(group_list){
    var string="<tr><th>#</th><th>GID</th><th>GName</th><th>GRemark</th><th>Status</th></tr>";
    var alive="<td><span class='label label-success'>Alived</span></td>";
    for(var i in group_list){
        for(var j=0;j<group_list[i].length;j++){
            var temp=JSON.parse(group_list[i][j]);
            if(temp['id']==1){
                continue;
            }
            string+="<tr class='grp-list'><td><input type='radio' name='radiogp' class='minimal' checked></td><td>"+temp['id']+"</td><td>"+temp['name']+"</td><td>"+temp['remark']+"</td>"+alive+"</tr>";
        }
    }
    $('table').html(string);
}

/**
 * @Type: Function
 * @Argv: if type==1 add.elif type==2 modify
 * @Return: Null
 * @Usage: $.pageShow.groupModalPutInfo()
 * @Desc: Input the selected group info to the modal
 * */
$.pageShow.groupModalPutInfo=function(type){
    var GID=document.getElementById('grpID');
    var GNAME=document.getElementById('grpName');
    var GREMARK=document.getElementById('grpRemark');
    if(type==2){
        var Element=$.devEops.searchChecked('grp-list');
        GID.value=Element.childNodes[1].innerHTML;
        GNAME.value=Element.childNodes[2].innerHTML
        GREMARK.value=Element.childNodes[3].innerHTML;
    }
    else{
        GID.value='#NEW';
        GNAME.removeAttribute('value');
        GREMARK.removeAttribute('value');
    }
    return ;
}

/**
 * @Type: Function
 * @Argv: Null
 * @Return: Null
 * @Usage: $.pageShow.groupModalPostInfo()
 * @Desc:
 * */
$.pageShow.groupModalPostInfo=function(){
    var GID=document.getElementById('grpID');
    var GNAME=document.getElementById('grpName');
    var GREMARK=document.getElementById('grpRemark');
    var postdata;
    if(GID.value=='#NEW')
    {
        postdata={"groupid":1,"groupname":GNAME.value,"groupremark":GREMARK.value};
    }
    else{
        postdata={"groupid":GID.value,"groupname":GNAME.value,"groupremark":GREMARK.value};
    }
    $.dataRecv.groupModifyDatabase(postdata);
    $.pageShow.groupInit();
}
/*-----------Host Page Data JS-----------*/
/**
 * @Type: Function
 * @Argv: Null
 * @Return: Null
 * @Usage: $.pageShow.hostInit()
 * @Desc: Function for init the host page.When you want to flush the page.
 * */
$.pageShow.hostInit=function() {
    var objS=document.getElementById('groupselect');
    objS.options.length=0;
    var list=$.dataRecv.groupGetBkData();
    for(var i in list){
        for(var j=0;j<list[i].length;j++){
            var temp=JSON.parse(list[i][j]);
            if(temp['id']==1){
                var op=new Option(temp['name'],temp['id'])
                objS.options.add(op);
                op.selected=true;
                continue;
            }
            objS.options.add(new Option(temp['name'],temp['id']));
        }
    }
}
/**
 * @Type: Function
 * @Argv: Null
 * @Return: Null
 * @Usage: $.pageShow.ChoseGroup()
 * @Desc: Function for chose group.
 * */
$.pageShow.ChoseGroup=function(){
    var ar=$.devEops.SelectPickUp('groupselect');
    var id=ar[0];
    var list=$.dataRecv.hostGetBkData(id);
    $.pageShow.hostTabDataFlush(list);
}

/**
 * @Type: Function
 * @Return: Null
 * @Usage: $.pageShow.hostTabDataFlush(host_list)
 * @Desc: host_list - js list of the group
 * */
$.pageShow.hostTabDataFlush=function(host_list){
    var string="";
    for(var i in host_list){
        for(var j=0;j<host_list[i].length;j++){
            var temp=JSON.parse(host_list[i][j]);
            if(temp['id']==1){
                continue;
            }
            string+="<tr class='hst-list'><td><input type='radio' name='radiohst' class='minimal' checked></td><td>"+temp['id']+"</td><td>"+temp['name']+"</td><td>"+temp['sship']+"</td><td><button data-toggle='modal' data-target='#Hostarv'><i class='fa fa-info'></i></button></td><tr>";
        }
    }
    $('tbody').html(string);
}

/**
 * @Type: Function
 * @Argv: arv - if arv==1 add elif arv=2 modify
 * @Return: Null
 * @Usage: $.pageShow.hostModalModify()
 * @Desc: @Argv
 * */
$.pageShow.hostModalModify=function(arv){
    var ar=$.devEops.SelectPickUp('groupselect');
    $.pageShow.rangeSelectInsert($.dataRecv.groupGetBkData(),'group_chose');
    var selectGroup=document.getElementById('group_chose');
    for(var i=0;i<selectGroup.options.length;i++){
        if(selectGroup.options[i].label==ar[1]){
            selectGroup.selectedIndex=i;
            break;
        }
    }
    var IP = document.getElementById('hstIP');
    if(arv==1) {
        IP.removeAttribute('disabled');
        IP.value = '';
    }else{
        var Element = $.devEops.searchChecked('hst-list');
        IP.setAttribute('disabled',true);
        IP.value = Element.childNodes[3].innerHTML;
    }
    return ;
}

/**
 * @Type: Function
 * @Argv: Null
 * @Return: Null
 * @Usage: $.pageShow.hostUpdateInfo()
 * @Desc: Update User Info Bk.
 * */
$.pageShow.hostUpdateInfo=function(){
    var IP = document.getElementById('hstIP');
    var ar=$.devEops.SelectPickUp('group_chose');
    $.dataRecv.hostUpdateInfo(IP.value,ar[0]);
}

/*-----------Search Page Data JS-----------*/
/**
 * @Type: Function
 * @Argv:
 * @Return: Null
 * @Usage: $.pageShow.SearchInfoResult()
 * */
$.pageShow.SearchInfoResult=function() {
    var NodeList=document.getElementsByClassName('manager-search-input');
    var Element=NodeList[NodeList.length-1];
    var string=Element.value;
    $.devEops.analyzeSearchItem(string);
}


/*-----------Batch Page Data JS-----------*/
/**
 * @Type: Argv
 * @Desc: the ip list for ansible
 * */
$.pageShow.AnsibleHostIDList={};

/**
 * @Type: Function
 * @Argv: soft_name - soft name
 * @Return: Null
 * @Usage: $.pageShow.versionFlush(appname);
 * @Desc: Use this function flush the version selected
 * */
$.pageShow.versionFlush=function(soft_name,select_id){
    var objS=document.getElementById(select_id);
    list=$.dataRecv.batchGetSoftVersion(soft_name);
    for(var i in list){
        for(var j=0;j<list[i].length;j++){
            var temp=JSON.parse(list[i][j]);
            objS.options.add(new Option(temp['soft_version'],temp['id']));
        }
    }
}

/**
 * @Type: Function
 * @Argv: inputclass - name of input tab's class
 * @Return: Null
 * @Usage: $.pageShow.clearBatchInputBox('mysqlinput')
 * @Desc: Clear the page input box.
 * */
$.pageShow.clearBatchInputBox=function(inputclass){
    var NodeList=document.getElementsByClassName(inputclass);
    if(NodeList.length==0){
        return;
    }else{
        for(var i=0;i<NodeList.length;i++){
            if(NodeList[i].value=="/usr/local"){
                continue;
            }
            NodeList[i].value="";
        }
    }
}

/**
 * @Type: Function
 * @Argv: list - list insert the select tab;select-id - select id
 * @Return: Null
 * @Usage: $.pageShow.rangeSelectInsert(list,select_id)
 * @Desc: Insert group or host data into the select table.
 */
$.pageShow.rangeSelectInsert=function(list,select_id){
    var objS=document.getElementById(select_id);
    objS.options.length=0;
    for(var i in list){
        for(var j=0;j<list[i].length;j++){
            var temp=JSON.parse(list[i][j]);
            if(temp['id']==1){
                continue;
            }
            objS.options.add(new Option(temp['name'],temp['id']));
        }
    }
    return ;
}


/**
 * @Type: Function
 * @Argv: NULL
 * @Return: NULL
 * @Usage: $.pageShow.rangeSelectGroup()
 * @Desc: Onchange Env for Group Select
 */
$.pageShow.rangeSelectGroup=function(){
    var objS=document.getElementById('range-group');
    var groupid=objS.options[objS.selectedIndex].value;
    var hostlist=$.dataRecv.hostGetBkData(groupid);
    $.pageShow.rangeSelectInsert(hostlist,'range-host');
}

/**
 * @Type: Function
 * @Argv: hostname Selected
 * @Return: Null
 * @Usage: $.pageShow.rangeSelected(hostname)
 * @Desc: like rangeSelectInsert.But not clear the all select options
 * */
$.pageShow.rangeSelectd=function(hostname,hostid){
    var objS=document.getElementById('range-selected');
    objS.options.add(new Option(hostname,hostid));
}

/**
 * @Type: Function
 * @Argv: inputclass - name of input tab's class
 * @Return: Null
 * @Usage: $.pageShow.clearBatchInputBox('mysqlinput')
 * @Desc: Clear the page input box.
 * */
$.pageShow.rangeSelectHost=function(){
    var objS=document.getElementById('range-host');
    var hostid=objS.options[objS.selectedIndex].value;
    var hostname=objS.options[objS.selectedIndex].label;
    if(!$.pageShow.AnsibleHostIDList.hasOwnProperty(hostname))//key not exsist
    {
        $.pageShow.AnsibleHostIDList[hostname]=hostid;
        $.pageShow.rangeSelectd(hostname,hostid);
    }
    return ;
}

/**
 * @Type: Function
 * @Argv: Null
 * @Return: Null
 * @Usage: $.pageShow.rangeSelectedRemove()
 * @Desc: Remove the select host
 * */
$.pageShow.rangeSelectedRemove=function () {
    var objS=document.getElementById('range-selected');
    var index=objS.selectedIndex;
    var hostid=objS.options[index].value;
    var hostname=objS.options[index].label;
    delete $.pageShow.AnsibleHostIDList[hostname];
    objS.options.remove(index);
    return ;
}

/**
 * @Type: Function
 * @Argv: Null
 * @Return: Null
 * @Usage: $.pageShow.redisBatch()
 * @Desc: 批量部署redis
 * */
$.pageShow.redisBatch=function(){
    var iplist=$.devEops.object2List($.pageShow.AnsibleHostIDList);
    var redisprefix,redisport,redispasswd,redisversion,redisdatadir;
    var NodeList=document.getElementsByClassName('batch-redis-input');
    redisversion=$.devEops.SelectPickUp('batch_version')[0];
    redisprefix=NodeList[0].value;
    redisport=NodeList[1].value;
    redispasswd=NodeList[2].value;
    redisdatadir=NodeList[3].value;
    $.dataRecv.batchRedis(iplist,redisversion,redisprefix,redisport,redispasswd,redisdatadir);
    delete $.pageShow.AnsibleHostIDList;
}

/**
 * @Type: Function
 * @Argv: Null
 * @Return: Null
 * @Usage: $.pageShow.mysqlBatch()
 * @Desc:批量部署mysql
 * */
$.pageShow.mysqlBatch=function(){
    var iplist=$.devEops.object2List($.pageShow.AnsibleHostIDList);
    var mysqlversion,mysqlprefix,mysqlpasswd,mysqldatadir,mysqlport,mysqlsocket;
    var NodeList=document.getElementsByClassName('batch-mysql-input');
    mysqlversion=$.devEops.SelectPickUp('batch_version')[0];
    mysqlprefix=NodeList[0].value;
    mysqlpasswd=NodeList[1].value;
    mysqldatadir=NodeList[2].value;
    mysqlport=NodeList[3].value;
    mysqlsocket=NodeList[4].value;
    $.dataRecv.batchMySQL(iplist,mysqlversion,mysqlprefix,mysqlpasswd,mysqldatadir,mysqlport,mysqlsocket);
    delete $.pageShow.AnsibleHostIDList;
}

/**
 * @Type: Function
 * @Argv: Null
 * @Return: Null
 * @Usage: $.pageShow.tomcatBatch()
 * @Desc: 批量部署tomcat
 * */
$.pageShow.tomcatBatch=function(){
    var iplist=$.devEops.object2List($.pageShow.AnsibleHostIDList);
    var javaversion,javaprefix,tomcatversion,tomcatprefix;
    var NodeList=document.getElementsByClassName('batch-tomcat-input');
    javaversion=$.devEops.SelectPickUp('batch_version_java')[0];
    javaprefix=NodeList[0].value;
    tomcatversion=$.devEops.SelectPickUp('batch_version_tomcat')[0];
    tomcatprefix=NodeList[1].value;
    $.dataRecv.batchTomcat(iplist,javaversion,javaprefix,tomcatversion,tomcatprefix);
    delete $.pageShow.AnsibleHostIDList;
}

/**
 * @Type: Function
 * @Argv: Null
 * @Return: Null
 * @Usage: $.pageShow.nginxBatch()
 * @Desc: 批量部署nginx
 * */
$.pageShow.nginxBatch=function(){
    var iplist=$.devEops.object2List($.pageShow.AnsibleHostIDList);
    var nginxversion,nginxprefix,nginxpid;
    var NodeList=document.getElementsByClassName('batch-nginx-input');
    nginxversion=$.devEops.SelectPickUp('batch_version')[0];
    nginxprefix=NodeList[0].value;
    nginxpid=NodeList[1].value;
    console.log(nginxversion,nginxprefix,nginxpid);
    $.dataRecv.batchNginx(iplist,nginxversion,nginxprefix,nginxpid);
    delete $.pageShow.AnsibleHostIDList;
}