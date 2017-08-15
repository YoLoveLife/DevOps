/**
 * Created by yo on 17-8-14.
 */
Normal_Args=['/etc/hosts','/etc/systemctl/iptables','/etc/my.cnf','/usr/local','prefix'
    ,'tar -xvzf','tar -cvzf','service']
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