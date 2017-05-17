/**
 * @Time: 2017-5-17
 * @Author: Yo
 * @Email: YoLoveLIfe@outlook.com
 * */

/**
 * @Type: Object
 * @Desc: $.loginValidate .login js
 * */
$.loginValidate={};

/**
* @Type: Object
* @Desc: all options in this project.
* */
$.loginValidate.options={
}

/**
 * @Type: Function
 * @Return Ajax recv Data
 * @Usage: $.loginValidate.ajaxBkDataAsync(url,async,type)
 * @Argv: url - the ajax url;type - 'GET/POST';async - 'true/false';postdata - exchange data
 * */
$.loginValidate.ajaxBkDataAsync=function(url,async,type,postdata){
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
 * @Return: Login
 * @Usage: $.loginValidate.loginPermit()
 * */
$.loginValidate.loginPermit=function(){
    var username=document.getElementById('loginemail').value;
    var passwd=document.getElementById('loginpasswd').value;
    var postdata={'username':username,'passwd':passwd};
    var result=$.loginValidate.ajaxBkDataAsync('loginpermit/',false,'GET',postdata);
    if(result['status']==1){
        var newurl=window.location.protocol+'//'+window.location.host+'/anweb/';
        window.location.href=newurl;
        return false;
    }else if(result['status']==0){
        alter('登录密码错误');
        console.log('登录密码错误');
    }else{
        alter('未知错误');
        console.log('未知错误');
    }
}
