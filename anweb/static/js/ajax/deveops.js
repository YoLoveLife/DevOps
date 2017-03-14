/**
 * Created by Dski_ on 2017/3/8.
 */
$(document).ready(function(){
    var ajax_url=location.hash.replace(/^#/, '');
    if(ajax_url.length<1){
        ajax_url='static/ajax/dashboard.html';
    }
    LoadAjaxContent(ajax_url);
    $('#main-menu').on('click','a',function(e){
        if($(this).hasClass('ajax-link')){//如果是一级菜单
            e.preventDefault();//取消默认点击的事件
            var url=$(this).attr('href');
            LoadAjaxContent(url);
        }
        else{
            return ;
        }
    });
});
/*-------------------------------------------
 Main scripts used by theme
 ---------------------------------------------*/
//
// Function for modal show
//
function OpenModal(modal){
    $(function() {
        $(modal).modal({
            keyboard: true
        })
    });
}
//
//  Function for load content from url and put in $('.ajax-content') block
//
function LoadAjaxContent(url){
    //$('.preloader').show();
    $.ajax({
        mimeType: 'text/html; charset=utf-8', // ! Need set mimeType only when run from local file
        url: url,
        type: 'GET',
        success: function(data) {
            $('#ajax-content').html(data);
     //       $('.preloader').hide();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert(errorThrown);
        },
        dataType: "html",
        async: false
    });
}




//模态框有两种模式
//一种是添加 一种是修改
//添加需要
function OpenGroupModal(modal,pagetype){
    //模态框开启
    if(pagetype='modify'){
        //DOM修改
        //$('')
    }
    $(function() {
        $(modal).modal({
            keyboard: true
        })
    });
}

//
//Search the group which is checked
//
function Group9SearchChecked(){
    var tbody=$('#ajax-data').childNodes()[0];
    alert(tbody.html);
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