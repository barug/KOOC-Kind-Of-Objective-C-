#!/usr/bin/env python3

from cnorm.parsing.declaration import Declaration
from koocTranslator import koocTranslator

parser = Declaration()

ast = parser.parse_file("decl.c")
print(ast.to_yml())
print(ast)
translator = koocTranslator()
translator.translateKoocAst(ast)

