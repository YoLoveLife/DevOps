/**
 * Created by yo on 17-8-14.
 */
Search_Args=['']
Normal_Args=['/etc/hosts','/etc/systemctl/iptables','/etc/my.cnf','/usr/local','/etc/init.d',
    'tar -xvzf','tar -cvzf','service']
Script={
    'CASE':['case "${变量}" in','${模式})','${语句}',';;','*)','${语句}',';;','esac'],
    'FOR':['for "${条件}"','do','${语句}','done'],
    'WHILE':['while "${条件}"','do','${语句}','done'],
    'FUNCTION':['function ${方法名}()','{','${方法内容}','}']
}

function insertAtTextArea(Element,value){
    Element.summernote('insertParagraph',value);
    Element.summernote('indent');
    Element.summernote('insertText',value);
}

function insertAtTextAreaCaseCode(Element){
    for(var i =0;i<Script['CASE'].length;i++){
        if(i==0){
            Element.summernote('insertParagraph');
            Element.summernote('insertText',Script['CASE'][i]);
            Element.summernote('insertParagraph');
            Element.summernote('indent');
        }
        else if(i!=Script['CASE'].length-1){
            Element.summernote('insertText',Script['CASE'][i]);
            Element.summernote('insertParagraph');
        }else{
            Element.summernote('outdent');
            Element.summernote('insertText',Script['CASE'][i]);
        }
    }
}

function insertAtTextAreaForWhileFunctionCode(Element,ITEM){
    for(var i=0;i<Script[ITEM].length;i++){
        if(i==0||i==1){
            Element.summernote('insertParagraph');
            Element.summernote('insertText',Script[ITEM][i]);
            if(i==1){
                Element.summernote('insertParagraph');
                Element.summernote('indent');
            }
        }else if(i!=Script['FOR'].length-1){
            Element.summernote('insertText',Script[ITEM][i]);
            Element.summernote('insertParagraph');
        }else{
            Element.summernote('outdent');
            Element.summernote('insertText',Script[ITEM][i]);
        }
    }
}


/*adhoc commit function*/
MODULE_LIST={
    '0':'none',
    '1': 'shell',
    '2': 'copy',
    '3': 'file',
    '4': 'yum',
    '5': 'service',
    '6': 'script',
    '7': 'get_url'
}
function commitAgrsSelect(){
    var obj=$('#select_module')[0];
    var id=obj.options[obj.selectedIndex].id;
    switch(MODULE_LIST[id]){
        case 'shell':
            return commitArgsForModuleShell();break;
        case 'copy':
            return commitArgsForModuleCopy();break;
        case 'file':
            return commitArgsForModuleFile();break;
        case 'yum':
            return commitArgsForModuleYum();break;
        case 'service':
            return commitArgsForModuleService();break;
        case 'script':
            return commitArgsForModuleScript();break;
        case 'get_url':
            return commitArgsForModuleGeturl();break;
        default:
            return "";
    }
}


function commitArgsForModuleShell(){
    var args="";
    args = args + $('#id_args')[0].value + " ";
    if($('#id_chdir')[0].value!=''){
        args = args + 'chdir=' + $('#id_chdir')[0].value + " ";
    }
    if($('#id_creates')[0].value !=''){
        args = args + 'creates=' + $('#id_creates')[0].value + " ";
    }
    if($('#id_removes')[0].value !=''){
        args = args + 'removes=' + $('#id_removes')[0].value + " ";
    }
    var module = $('#id_module')[0].value;

    var data={'module':module,'args':args};
    return data;
}

function commitArgsForModuleCopy(){
    var args="";

    if($('#id_src')[0].value !=''){
        args = args + 'src=' + $('#id_src')[0].value + " ";
    }else{
        alert('源文件未填写');
        return {};
    }

    if($('#id_dest')[0].value !=''){
        args = args + 'dest=' + $('#id_dest')[0].value + " ";
    }else{
        alert('目标文件未填写');
        return {};
    }

    var backupObj=$('#id_backup')[0];
    if(backupObj.options[backupObj.selectedIndex].id==0){
        args +="backup=no ";
    }else{
        args +="backup=yes ";
    }

    var remote_srcObj=$('#id_remote_src')[0];
    if(remote_srcObj.options[remote_srcObj.selectedIndex].id==0){
        args +="remote_src=False ";
    }else{
        args +="remote_src=True ";
    }


    var module = $('#id_module')[0].value;
    var data={'module':module,'args':args};
    return data;
}

function commitArgsForModuleFile(){
    var args="";
    if($('#id_path')[0].value !=''){
        args = args + 'path=' + $('#id_path')[0].value + " ";
    }else{
        alert('路径未填写');
        return {};
    }

    var stateObj=$('#id_state')[0];
    args +="state=" +stateObj.options[stateObj.selectedIndex].id+" ";

    if($('#id_mode')[0].value !=''){
        args = args + 'mode=' + $('#id_mode')[0].value + " ";
    }


    if($('#id_group')[0].value !=''){
        args = args + 'group=' + $('#id_group')[0].value + " ";
    }

    var module = $('#id_module')[0].value;
    var data={'module':module,'args':args};
    return data;
}

function commitArgsForModuleYum(){
    var args="";

    if($('#id_yumname')[0].value !=''){
        args = args + 'name=' + $('#id_yumname')[0].value + " ";
    }else{
        alert('处理包名称未填写');
        return {};
    }

    var stateObj=$('#id_state')[0];
    args +="state=" +stateObj.options[stateObj.selectedIndex].id+" ";


    var module = $('#id_module')[0].value;
    var data={'module':module,'args':args};
    return data;
}

function commitArgsForModuleService(){
    var args="";

    var servicenameObj=$('#id_servicename')[0];
    args +="name=" +servicenameObj.options[servicenameObj.selectedIndex].id+" ";

    var stateObj=$('#id_state')[0];
    args +="state=" +stateObj.options[stateObj.selectedIndex].id+" ";

    var module = $('#id_module')[0].value;
    var data={'module':module,'args':args};
    return data;
}

function commitArgsForModuleScript() {
   var args="";

    var backupObj=$('#id_script_id')[0];

    args = args+backupObj.options[backupObj.selectedIndex].id;

    if($('#id_creates')[0].value !=''){
        args = args + 'creates=' + $('#id_creates')[0].value + " ";
    }
    if($('#id_removes')[0].value !=''){
        args = args + 'removes=' + $('#id_removes')[0].value + " ";
    }

    var module = $('#id_module')[0].value;

    var data={'module':module,'args':args};
    return data;

}