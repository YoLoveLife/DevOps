/**
 * Created by yo on 17-8-14.
 */
Args=['function','case','esac','while','for']
Script={
    'CASE':
        'case "${变量}" in\n' +
        '\t${模式})\n' +
        '\t${语句}\n' +
        '\t;;\n' +
        '\t*)\n' +
        '\t${语句}\n' +
        '\t;;\n' +
        'esac\n',
    'FOR':
        'for "${条件}"\n' +
        'do\n' +
        '\t${语句}\n' +
        'done\n',
    'WHILE':
        'while "${条件}"\n' +
        'do\n' +
        '\t${语句}\n' +
        'done\n',
    'FUNCTION':
        'function ${方法名}()\n' +
        '{\n' +
        '\t${方法内容}\n' +
        '}\n'
}

function insertAtTextArea(Element,value){
    Element.summernote('editor.insertText',value);
}