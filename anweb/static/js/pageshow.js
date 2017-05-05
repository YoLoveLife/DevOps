/**
 * @Time: 2017-4-19
 * @Author: Yo
 * @Email: YoLoveLIfe@outlook.com
 * @Desc: Function for DOM
 * */

/**
 * @Type: Object
 * @Desc: $.pageShow is the page-show for the app.
 * */
$.pageShow={};

/*-----------Group Page Data JS-----------*/
/**
 * @Type: Function
 * @Argv: modal - id name of modal tab
 * @Return: Null
 * @Usage: $.pageShow.openGroupModal4Modify('modalmysql')
 * */
$.pageShow.openGroupModal4Modify=function(modal){
    var Element=$.devEops.searchChecked('group-table');
    var list=[Element.childNodes[1].innerHTML,Element.childNodes[2].innerHTML,Element.childNodes[3].innerHTML];
    /***More***/
}
/*-----------Search Page Data JS-----------*/
/**
 * @Type: Function
 * @Argv:
 * @Return: Null
 * @Usage: $.pageShow.SearchInfoResult()
 * */
$.pageShow.SearchInfoResult=function() {
    var NodeList=document.getElementsByClassName('manager-search-input');
    var Element=NodeList[NodeList.length-1];
    var string=Element.value;
    $.devEops.analyzeSearchItem(string);
}


/*-----------Batch Page Data JS-----------*/
$.pageShow.AnsibleIPList=[];

/**
 * @Type: Function
 * @Argv: inputclass - name of input tab's class
 * @Return: Null
 * @Usage: $.pageShow.clearBatchInputBox('mysqlinput')
 * @Desc: Clear the page input box.
 * */
$.pageShow.clearBatchInputBox=function(inputclass){
    var NodeList=document.getElementsByClassName(inputclass);
    if(NodeList.length==0){
        return;
    }else{
        for(var i=0;i<NodeList.length;i++){
            NodeList[i].value="";
        }
    }
}

