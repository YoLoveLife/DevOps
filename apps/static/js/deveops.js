/**
 * @Time: 2017-4-11
 * @Author: Yo
 * @Email: YoLoveLIfe@outlook.com
 * */

/**
 * @Desc: Make sure jQuery has been loaded before deveops.js
 * */
if (typeof jQuery==="undefined"){
    throw new Error("devEops requires jQuery");
}

/**
 * @Type: Object
 * @Desc: $.devEops is the main object for the app.
 * */
$.devEops={};

/**
* @Type: Object
* @Desc: all options in this project.
* */
$.devEops.options={
    animationSpeed:500,
    mainPage:'static/pages/dashboard.html'
}

/**
 * @Type: Function
 * @Return: Null
 * @Desc: Some init for this object
 * */
$(function(){
    if (typeof devEopsOptions !=="undefined"){
        $.extend(true,
            $.devEops.options,
            devEopsOptions
        );
    }
    var o=$.devEops.options;
    //_init();
    //$.devEops.pushMenu.activate("[data-toggle='offcanvas']");
    $.devEops.treeMenu('.sidebar');
    // var ajax_url=location.hash.replace(/^#/, '');
    // if(ajax_url.length<1){
    //     ajax_url=o.mainPage;
    // }
    //$.devEops.loadAjaxContent('static/pages/dashboard.html');

    //$.devEops.ajaxContentClickModify('.sidebar');
    //$.devEops.ajaxContentClickModify('.app-bell');
})

/**
 * @Type: Function
 * @Return: Null
 * @Usage: $.devEops.ajaxContentClickModify('.sidebar')
 * @Desc: element class sidebar will check the ajax-link tab.And element will show the page by ajax.
 * */
$.devEops.ajaxContentClickModify=function(element){
    $(element).on('click','a',function(e){
        if($(this).hasClass('ajax-link')){
            e.preventDefault();
            var url=$(this).attr('href');
            $.devEops.loadAjaxContent(url);
        }
        else{
            return ;
        }
    });
}

/**
 * @Type: Function
 * @Return: Null
 * @Usage: $.devEops.pushMenu.activate("[data-toggle='offcanvas']")
 * @Desc: Null
 * */
$.devEops.pushMenu={
    activate:function(toggleBtn){
        $(document).on('click',toggleBtn,function(e){
            e.preventDefault();//取消事件默认操作
            console.log("Hello push Menu");
        })
    }
}

/**
 * @Type: Function
 * @Return: Null
 * @Usage: $.devEops.treeMenu('.sidebar')
 * @Desc: Modify the click function abount the tree-menu.
 * */
$.devEops.treeMenu=function(menu){
    var _this=this;
    var animationSpeed=$.devEops.options.animationSpeed;
    $(document).off('click',menu+' li a')
        .on('click',menu+' li a',function(e){
            var $this=$(this);
            var checkElement=$this.next();

            if((checkElement.is('.treeview-menu'))&&(checkElement.is(':visible'))){//如果点击的是有子菜单的 并且已展开的
                checkElement.slideUp(animationSpeed,function(){//以animationSpeed来去除menu-open class
                    checkElement.removeClass('menu-open');
                });
                checkElement.parent('li').removeClass('active');//去除class中的active
            }
            else if((checkElement.is('.treeview-menu'))&&(!checkElement.is(':visible'))){//如果点击的是有子菜单 并且未展开
                var parent=$this.parents('ul').first();//获取父的第一个ul元素
                var ul=parent.find('ul:visible').slideUp(animationSpeed);//搜索列表中已经开启的母菜单并且将其关闭
                ul.removeClass('menu-open');
                var parent_li=$this.parent("li");
                checkElement.slideDown(animationSpeed,function(){
                   checkElement.addClass('menu-open');
                   parent.find('li.active').removeClass('active');
                   parent_li.addClass('active');
                });
            }
            if(checkElement.is('.treeview-menu')){
                e.preventDefault();
            }
        })
}

/**
 * @Type: Function
 * @Return: Null
 * @Usage: $.devEops.loadAjaxContent('pages/dashboard.html')
 * @Desc: Load the page in the index.html's tab id #ajax-content
 * */
$.devEops.loadAjaxContent=function (url) {
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

/**
 * @Type: Function
 * @Return: Null
 * @Usage: $.devEops.openModal(modal)
 * @Desc: Open the Modal
 * */
$.devEops.openModal=function(modal){
    $(function() {
        $(modal).modal({
            keyboard: true
        })
    });
}

/**
 * @Type: Function
 * @Return the value of pick up list
 * @Usage: $.devEops.listPickUp(listname)
 * @Argv: Listname - the id of tab.
 * @Desc: Get the select Tab value and return.
 * */
$.devEops.SelectPickUp=function(listname){
    var objSelect = document.getElementById(listname);
    var objvalue = objSelect.options[objSelect.selectedIndex].value;
    var objlabel = objSelect.options[objSelect.selectedIndex].label;
    return [objvalue,objlabel];
}

/**
 * @Type: Function
 * @Return: Element of checked.
 * @Usage: $.devEops.searchChecked(listelement)
 * @Desc: Through getElementsByClassName get the nodelist of tab-class and find which is checked
 * @Notice: 如果有可能通过在点击的时候也增添class 使用hasClass来做 循环的方式不合理
 * */
$.devEops.searchChecked=function(listelement){
    var nodeList=document.getElementsByClassName(listelement);
    for (var i = 0; i < nodeList.length; i++) {//遍历NodeLists中的所有元素 每一次就是一行
        if(nodeList[i].firstElementChild.firstElementChild.checked){
            //nodeList[i]就是每一行 每一行的第一个元素firstElementChild就是所谓的checkbox 但是这里的checkbox由两部分组成<label><input></label>我们所需要的是input中的属性
            //如果被选中的话
            return nodeList[i]
        }
    }
    return null;
}


/**
 * @Type: Function
 * @Return Ajax recv Data
 * @Usage: $.devEops.ajaxBkDataAsync(url,async,type)
 * @Argv: url - the ajax url;type - 'GET/POST';async - 'true/false';postdata - exchange data
 * */
$.devEops.ajaxBkDataAsync=function(url,async,type,postdata){
    var list;
    $.ajax({
        async:async,
        url:url,
        type:type,
        data:postdata,
        dataType:"json",
        success:function(qlist){
            list=qlist;
        },
        error:function(){
            console.log("Ajax Fail");
        }
    });
    return list;
}

/**
 * @Type: Function
 * @Arvg: String of search info
 * @Return:
 * @Usage: $.devEops.analyzeSearchItem(String)
 * @Desc: analyze the Search Info and return a list type of info.
 * */
$.devEops.analyzeSearchItem=function(string){
    var Item=new Array();
    var Dist={};
    Items=string.split(';');
    for(var i=0;i<Items.length;i++){
        var Item=new Array();
        Item=Items[i].split('=');
        Dist[Item[0]]=Item[1];
    }
    console.log(Dist);
    return Dist;
}

/**
 * @Type: Function
 * @Argv: object
 * @Return: list
 * @Usage: $.devEops.object2List()
 * @Desc: 将object字典的值部分转换为list
 * */
$.devEops.object2List=function(object) {
    var list=[];
    for(var i in object){
        list.push(object[i]);
    }
    return list;
}
