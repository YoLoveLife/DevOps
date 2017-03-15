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

