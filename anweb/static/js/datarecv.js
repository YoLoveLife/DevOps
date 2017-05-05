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

/*-----------Group Page Data JS-----------*/
/**
 * @Type: Function
 * @Return: Null
 * @Usage: $.dataRecv.groupTabDataFlush(group_list)
 * @Desc: group_list - js list of the group
 * */
$.dataRecv.groupTabDataFlush=function(group_list){
    /*Code need change*/
    var string="";
    for(var i in group_list){
        for(var j=1;j<group_list[i].length;j++){
            var checkbox="<label class=\"checkbox\" for=\"checkbox"+j+"\"><input type=\"checkbox\" value=\"\" id=\"checkbox"+j+"\"data-toggle=\"checkbox\"></label>";
            var temp=JSON.parse(group_list[i][j]);
            string+='<tr class=\"group-table\"><td>'+checkbox+'</td><td>'+temp['id']+
                '</td><td>'+temp['group_name']+'</td><td>'
                + temp['remark']+'</td>';
        }
    }
    $('tbody').html(string);
    $('[data-toggle="checkbox"]').radiocheck();//数据样式变更
}

/**
 * @Type: Function
 * @Return: group_list
 * @Usage: $.dataRecv.groupGetBkData()
 * @Desc: Get the All Group from the database.json data.
 * */
$.dataRecv.groupGetBkData=function(){
    return $.devEops.ajaxBkDataAsync('grousearch/',false,"GET",{});
}

/**
 * @Type: Function
 * @Return: null
 * @Usage: $.groupModifyDatabase(group)
 * @Desc: group is a object.
 * */
$.dataRecv.groupModifyDatabase=function(group) {
    var postdata={"groupid":group.groupid,"groupname":group.groupname,"groupremark":group.groupremark};
    $.devEops.ajaxBkDataAsync('groupmodify/',true,"POST",postdata);
}


/*-----------Host Page Data JS-----------*/








