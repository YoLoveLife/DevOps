/**
 * Created by Dski_ on 2017/3/15.
 */

//
//Function use by Host page
//
function Host9GetBackData(groupid){
    var host_list;
    postdata={"groupid":groupid};
    $.ajax({
        url:'hostsearch/',
        type:"GET",
        data:postdata,
        success:function(host_list){
            host_list=JSON.parse(host_list);
        }
    });
    return host_list;
}

function Host9FlushPage(host_list){
    var string="";
    if(host_list={}){
    }
    else{

        for(var i in group_list){
            for(var j=0;j<group_list[i].length;j++){
                var checkbox="<label class=\"checkbox\" for=\"checkbox"+j+"\"><input type=\"checkbox\" value=\"\" id=\"checkbox"+j+"\"data-toggle=\"checkbox\"></label>";
                var temp=JSON.parse(group_list[i][j]);
                string+='<tr class="group-table"><td>'+checkbox+'</td><td>'+temp['id']+
                    '</td><td>'+temp['hostname']+
                        '</td><td>'+temp['apptype']+'</td>'
            }
        }
    }
    $('tbody').html(string);
    $('[data-toggle="checkbox"]').radiocheck();//数据样式变更
        if ($('[data-toggle="select"]').length) {
            $('[data-toggle="select"]').select2();
        }
}

/*
            var string="";
            for(var i in host_list){
                for(var j=0;j<host_list[i].length;j++){
                    var checkbox="<label class=\"checkbox\" for=\"checkbox"+j+"\"><input type=\"checkbox\" value=\"\" id=\"checkbox"+j+"\"data-toggle=\"checkbox\"></label>";
                    var temp=JSON.parse(host_list[i][j]);
                    string+="";
                }
            }
            $('tbody').html(string);
            $('[data-toggle="checkbox"]').radiocheck();//数据样式变更
*/