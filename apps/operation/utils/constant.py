# -*- coding:utf-8 -*-
# Time 2017-8-11 16:42:41
# Author Yo
# 你说 看不到的脚本还用\t来维护可读性是不是脑子有问题
FUNCTION_ARGS='function Args(){\n' \
              '\t%s\n' \
              '\teval set -- "${ARGS}"\n' \
              '\twhile true\n' \
              '\t\tdo\n' \
              '\t\t\tcase "$1" in\n' \
              '%s\n' \
              '\t\t\tesac\n' \
              '\t\tdone\n' \
              '}\n'

SIMPLE_CASE_ITEM='\t\t\t\t--%s)\n' \
                 '\t\t\t\t%s=$1\n' \
                 '\t\t\t\tshift\n' \
                 '\t\t\t\t;;\n'

EXTEND_CASE_ITEM='\t\t\t\t--%s)\n' \
          '\t\t\t\t%s=$2\n' \
          '\t\t\t\tshift 2\n' \
          '\t\t\t\t;;\n'

CASE_END='\t\t\t\t--)\n' \
         '\t\t\t\tshift\n' \
         '\t\t\t\tbreak\n' \
         '\t\t\t\t;;\n' \
         '\t\t\t\t*)\n' \
         '\t\t\t\texit 2\n' \
         '\t\t\t\t;;\n'


PATTERN_BR = r'\<br\>'
PATTERN_P = r'\<p\>'
PATTERN_F_P = r'\<\/p\>'