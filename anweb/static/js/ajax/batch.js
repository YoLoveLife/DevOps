/**
 * Created by Dski_ on 2017/3/20.
 */
//
//Function for get app version
//
function Batch9GetAppVersion(appid){
    var list=[];
    postdata={"app_id":appid};
    $.ajax({
        async:false,
        url:'batchgetappversion/',
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
//Function for get App Type
//
function Batch9GetAppType(){
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