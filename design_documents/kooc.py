#!/usr/bin/env python3
# -*- coding: utf-8 -*-    

from cnorm.passes import to_c
from cnorm.parsing.declaration import Declaration
from sys import exit, argv as av
from koocParser import *

def     main():
    if (len(av) != 2):
        exit(0)
    parser = koocParser()
    ast = parser.parse_file(av[1])
    # parser.inject_begin(ast)
    c_file = (av[1][:-2] + 'c')
    c_file = open(c_file, 'w')
    c_file.write(str(ast.to_c()))
    c_file.close()
    print("OK")
    # print(str(ast.to_c()))

if __name__ == '__main__':
    exit(main())
