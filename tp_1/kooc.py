#!/usr/bin/env python3
# -*- coding: utf-8 -*-    

from cnorm.passes import to_c
from cnorm.parsing.declaration import Declaration
from sys import argv as av

if __name__ == '__main__':
    parser = Declaration()
    ast = parser.parse_file(av[1])
    # parser.inject_begin(ast)
    c_file = (av[1][:-2] + 'c')
    c_file = open(c_file, 'w')
    c_file.write(str(ast.to_c()))
    c_file.close()
    # print(str(ast.to_c()))
