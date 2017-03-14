/**
 * Created by Dski_ on 2017/3/10.
 */
//
//Modal For Add and Info
//
function OpenGroupModal4AddInfo(modal){
    $(function() {
        $(modal).modal({
            keyboard: true
        })
    });
}

//
//Modal For Modify Group Info
//
function OpenGroupModal4Modify(modal){
    var Element=Group9SearchChecked();
    var list=[Element.childNodes[3].innerHTML,Element.childNodes[5].innerHTML,Element.childNodes[7].innerHTML];
    ModifyModal(list);
    $(function() {
        $(modal).modal({
            keyboard: true
        })
    });
}

//
//Function for change the modal in HTML
//
function ModifyModal(group_info_list){
    document.getElementById('groupInfo-id').setAttribute('value',group_info_list[0]);
    document.getElementById('groupInfo-name').setAttribute('value',group_info_list[1]);
    document.getElementById('groupInfo-remark').setAttribute('value',group_info_list[2]);
}


//
//Search the group which is checked
//
function Group9SearchChecked() {
    var groups = document.getElementsByClassName('group-table');//这是一个NodeList以列表的形式包含列表内的每一行元素
    var groupid="";
    var groupname="";
    var groupremark="";
    for (var i = 0; i < groups.length; i++) {//遍历NodeLists中的所有元素 每一次就是一行
        if(groups[i].firstElementChild.firstElementChild.firstElementChild.checked){
            //groups[i]就是每一行 每一行的第一个元素firstElementChild就是所谓的checkbox 但是这里的checkbox由两部分组成<label><input></label>我们所需要的是input中的属性
            //如果被选中的话
            return groups[i]
        }
    }
}

//
//Function for start the modify
//
function PostGroupInfo4ModifyAdd(){
    //依据表单内容提交POST
    var groupid=document.getElementById('groupInfo-id').getAttribute('value');
    var groupname=document.getElementById('groupInfo-name').getAttribute('value');
    var groupremark=document.getElementById('groupInfo-remark').getAttribute('value');
    //POST数据
    Group9ModifyGroup(groupid,groupname,groupremark);

}

//
//Function for change the html page
//
function ModifyHTMLPage(group_info_list){
    var Element=Group9SearchChecked();
    Element.childNodes[5].innerHTML=group_info_list[1];
    Element.childNodes[7].innerHTML=group_info_list[2];
}

//
//Function use for new Group
//
function Group9ModifyGroup(groupid,groupname,groupremark){
    var list=[groupid,groupname,groupremark];
    ModifyHTMLPage(list);
    /*
    $.ajax({
        url:'groupnew/',
        type:'POST',
        data:"groupid"+groupid+"groupname="+groupname+"&groupremark="+groupremark,
        success:function(){//成功修改
            var list=[groupid,groupname,groupremark];
            ModifyHTMLPage(list);
        },
        error:function(){//修改失败

        }
    });*/
}

//
//Function use by Group page
//
function Group9GetBackData(){
    $.ajax({
        url:'groupsearch/',
        type:"GET",
        success:function(group_list){
            group_list=JSON.parse(group_list);
            var string="";
            var checkbox="<label class=\"checkbox\" for=\"checkbox2\"><input type=\"checkbox\" value=\"\" id=\"checkbox2\" data-toggle=\"checkbox\"></label>";
            for(var i in group_list){
                for(var j=0;j<group_list[i].length;j++){
                    var temp=JSON.parse(group_list[i][j]);
                    string+='<tr><td>'+checkbox+'</td><td>'+temp['id']+
                        '</td><td>'+temp['group_name']+'</td><td>'
                        + temp['remark']+'</td>';
                }
            }
            $('tbody').html(string);
        }
    });
}


