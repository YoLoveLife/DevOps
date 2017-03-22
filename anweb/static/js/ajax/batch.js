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
    var objSelect = document.getElementById('host-grouplist');
    var groupid = objSelect.options[objSelect.selectedIndex].value;
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
                string+='<li class="todo-done"><div class="todo-icon fui-dropbox"></div><div class="todo-content"><h4 class="todo-name">'+
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
//Function for post the tomcat install
//
function Batch9PostTomcat(){
    //数据获取
    //
    var list=[];
    $.ajax({
        async:false,
        url:'batchgetapptype/',
        type:"GET",
        dataType:"json",
        success:function(host_list){
            list=host_list;
        }
    });
    return list;
}

//
//Function OpenBatchModal4Tomcat
//
function OpenBatchModal4Tomcat(modal){
    $(function() {
        $(modal).modal({
            keyboard: true
        })
    });
    javaversionlist=Batch9GetVersion("java");//获得数据
    Batch9Version(javaversionlist,'#batch-jdkversion');//刷新数据
    tomcatversionlist=Batch9GetVersion("tomcat");
    Batch9Version(tomcatversionlist,'#batch-tomcatversion');
}