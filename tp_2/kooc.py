#!/usr/bin/env python3
# -*- coding: utf-8 -*-    

from cnorm.passes import to_c
from cnorm.parsing.declaration import Declaration
from sys import exit, argv as av

def     main():
    if (len(av) != 2):
        exit(0)
    parser = Declaration()

    if (av[1].endswith(".kc")):
        #modif grammar
        ast = parser.parse_file(av[1])
        # modif ast
        c_file = (av[1][:-2] + 'c')
        with open(c_file, 'w') as c_file:
            c_file.write(str(ast.to_c()))
            c_file.close()

if __name__ == '__main__':
    exit(main())
