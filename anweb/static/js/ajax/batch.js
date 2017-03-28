/**
 * Created by Dski_ on 2017/3/20.
 */
//
//Function for get app version
//
function Batch9GetVersion(appname){
    var list=[];
    postdata={"appname":appname};
    $.ajax({
        async:false,
        url:'softversion/',
        type:"GET",
        data:postdata,
        dataType:"json",
        success:function(host_list){
            list=host_list;
        }
    });
    return list;
}

//
//Function for init Data First
//
function Batch9DataInit(){
    Host9FlushGroupList();
}

//
//Function for Pick up Group
//
function Batch9PickGroup(){
    var groupid=ListPickUp('host-grouplist')
    var list = Host9GetBackData(groupid);
    Batch9FlushPage(list);
}

//
//Function for Flush host list
//
function Batch9FlushPage(host_list){
    /*
    <li class="todo-done"><div class="todo-content"><h4 class="todo-name">Meet Adrian at 6pm</h4>Times Square</div></li>
    * */
    var string="";
    if(host_list.length==0){
    }
    else{
        for(var i in host_list){
            for(var j=0;j<host_list[i].length;j++){
                var temp=JSON.parse(host_list[i][j]);
                string+='<li><div class="todo-icon fui-dropbox"></div><div class="todo-content"><h4 class="todo-name">'+
                    temp['hostname']+'</h4>'+temp['sship']+'</div></li>';
            }
        }
    }
    $('#batch-host').html(string);
    $('[data-toggle="checkbox"]').radiocheck();//数据样式变更
}

//
//Function for flush tomcat version
//
function Batch9Version(version_list,modallist){
    string='<option value=\"0\" selected>No Selected</option>';
    for(var i in version_list){
        for(var j=0;j<version_list[i].length;j++){
            var temp=JSON.parse(version_list[i][j]);
            string+="<option value=\""+temp['id']+"\">"+temp['soft_version']+ "</option>";
        }
    }
    $(modallist).html(string);
    if ($('[data-toggle="select"]').length) {
            $('[data-toggle="select"]').select2();
    };
}


//
//Function get postdata
//
function Batch9GetPostIPData(){
    var list=[];
    var objHostlist=document.getElementsByClassName('todo-done');
    if(objHostlist.length==0){
        return list;
    }
    for(var i=0;i<objHostlist.length;i++){
        var sship=objHostlist[i].firstElementChild.nextElementSibling.lastChild;
        list.push(sship.data);
    }
    return list
}

//
//Function for tomcat modal data get
//
function Batch9TomcatModalGet() {
    var postdata={};
    var iplist=Batch9GetPostIPData();
    var javaversion=ListPickUp("batch-version-jdk");
    var tomcatversion=ListPickUp("batch-version-tomcat");
    var javaprefix=document.getElementById("batch-prefix-java").value;
    var tomcatprefix=document.getElementById("batch-prefix-tomcat").value;
    if(javaversion=="0"||tomcatversion=="0"||javaprefix.length==0||tomcatprefix.length==0){
        alert("未选择");
        return ;
    }
    //
    postdata['iplist[]']=iplist;
    postdata['javaversion']=javaversion;
    postdata['tomcatversion']=tomcatversion;
    postdata['javaprefix']=javaprefix;
    postdata['tomcatprefix']=tomcatprefix;
    return postdata;
}

//
//Function for post the tomcat install
//
function Batch9PostTomcat(){
    var postdata=Batch9TomcatModalGet();
    console.log(postdata);
    if(postdata.length==0){
        return ;
    }
    $.ajax({
        async:false,
        url:'batchtomcat/',
        type:"POST",
        data:postdata,
        success:function(status){
            return ;
        }
    });
}

//
//Function OpenBatchModal4Tomcat
//
function OpenBatchModal4Tomcat(modal){
    var iplist=Batch9GetPostIPData();
    if(iplist.length==0) {
        alert("未选择");
        return ;
    }
    $(function() {
        $(modal).modal({
            keyboard: true
        })
    });
    javaversionlist=Batch9GetVersion("java");//获得数据
    Batch9Version(javaversionlist,'#batch-version-jdk');//刷新数据
    tomcatversionlist=Batch9GetVersion("tomcat");
    Batch9Version(tomcatversionlist,'#batch-version-tomcat');
}

//
//Function OpenBatchModal4MySQL
//
function OpenBatchModal4MySQL(modal){
    var iplist=Batch9GetPostIPData();
    if(iplist.length==0) {
        alert("未选择");
        return ;
    }
    $(function() {
        $(modal).modal({
            keyboard: true
        })
    });
    mysqlversion=Batch9GetVersion("mysql");
   // javaversionlist=Batch9GetVersion("java");//获得数据
    Batch9Version(mysqlversion,'#batch-version-mysql');//刷新数据
}

//
//Function for mysql modal data get
//
function Batch9MySQLModalGet() {
    var postdata={};
    var iplist=Batch9GetPostIPData();
    var mysqlversion=ListPickUp("batch-version-mysql");
    var mysqlprefix=document.getElementById("batch-prefix-mysql").value;
    var mysqlpasswd=document.getElementById("batch-passwd-mysql").value;
    var mysqldatadir=document.getElementById("batch-datadir-mysql").value;
    var mysqlport=document.getElementById("batch-port-mysql").value;
    var mysqltmp=document.getElementById("batch-tmp-mysql").value;
    if(mysqlversion=="0"||mysqlprefix.length==0||mysqlport.length==0||mysqltmp.length==0){
        alert("未选择");
        return ;
    }
    //
    postdata['iplist[]']=iplist;
    postdata['mysqlversion']=mysqlversion;
    postdata['mysqlprefix']=mysqlprefix;
    postdata['mysqlpasswd']=mysqlpasswd;
    postdata['mysqldatadir']=mysqldatadir;
    postdata['mysqlport']=mysqlport;
    postdata['mysqltmp']=mysqltmp;
    return postdata;
}

//
//Function
//
function Batch9PostMySQL(){
    var postdata=Batch9MySQLModalGet();
    if(postdata.length==0){
        return ;
    }
    $.ajax({
        async:false,
        url:'batchmysql/',
        type:"POST",
        data:postdata,
        success:function(status){
            return ;
        }
    });
}

//
//Function
//
function Batch9PostRedis(){
    var postdata=Batch9RedisModalGet();
    if(postdata.length==0){
        return ;
    }
    $.ajax({
        async:false,
        url:'batchredis/',
        type:"POST",
        data:postdata,
        success:function(status){
            return ;
        }
    });
}

//
//Function for mysql modal data get
//
function Batch9RedisModalGet() {
    var postdata={};
    var iplist=Batch9GetPostIPData();
    var redisversion=ListPickUp("batch-version-redis");
    var redisprefix=document.getElementById("batch-prefix-redis").value;
    var redisport=document.getElementById("batch-port-redis").value;
    var redispasswd=document.getElementById("batch-passwd-redis").value;
    if(redisversion.length==0||redisprefix.length==0||redisport.length==0){
        alert("未选择");
        return ;
    }
    //
    postdata['iplist[]']=iplist;
    postdata['redisversion']=redisversion;
    postdata['redisprefix']=redisprefix;
    postdata['redisport']=redisport;
    postdata['redispasswd']=redispasswd;
    return postdata;
}

//
//Function OpenBatchModal4Redis
//
function OpenBatchModal4Redis(modal){
    var iplist=Batch9GetPostIPData();
    if(iplist.length==0) {
        alert("未选择");
        return ;
    }
    $(function() {
        $(modal).modal({
            keyboard: true
        })
    });
    redisversion=Batch9GetVersion("redis");
    Batch9Version(redisversion,'#batch-version-redis');//刷新数据
}