/**
 * Created by Dski_ on 2017/3/15.
 */

//
//Function for open modal
//


//
//Function use by Host page
//
function Host9GetBackData(group_id){
    var list=[];
    if(group_id=="0")
    {
        return list;
    }
    postdata={"group_id":group_id};
    $.ajax({
        async:false,
        url:'hostsearch/',
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
//Flush the HTMLPage with host_list
//
function Host9FlushPage(host_list){
    var string="";
    if(host_list.length==0){
    }
    else{
        for(var i in host_list){
            for(var j=0;j<host_list[i].length;j++){
                var checkbox="<label class=\"checkbox\" for=\"checkbox"+j+"\"><input type=\"checkbox\" value=\"\" id=\"checkbox"+j+"\"data-toggle=\"checkbox\"></label>";
                var temp=JSON.parse(host_list[i][j]);
                string+='<tr class="group-table"><td>'+checkbox+'</td><td>'+temp['id']+
                    '</td><td>'+temp['hostname']+'</td><td>'+temp['sship']+
                        '</td><td>'+temp['app_type']+'</td>';
            }
        }
    }
    $('tbody').html(string);
    $('[data-toggle="checkbox"]').radiocheck();//数据样式变更
}


//
//Function the host which is checked
//
function Host9FlushGroupList(){
    var group_list  =  Group9GetBackData();
    //string="";
    string='<option value=\"0\" selected>No Selected</option>';
    for(var i in group_list){
        for(var j=0;j<group_list[i].length;j++){
            var temp=JSON.parse(group_list[i][j]);
            string+="<option value=\""+temp['id']+"\">"+temp['group_name']+ "</option>";
        }
    }
    $('#host-grouplist').html(string);
    if ($('[data-toggle="select"]').length) {
            $('[data-toggle="select"]').select2();
    };
}

//
//Function Group Pick up and show the host table
//
function Host9PickGroup() {
    var objSelect = document.getElementById('host-grouplist');
    var groupid = objSelect.options[objSelect.selectedIndex].value;
    var list = Host9GetBackData(groupid);
    Host9FlushPage(list);
}