#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-    

from pyrser.grammar import Grammar
from pyrser import meta
from pyrser.parsing.node import Node
from cnorm.parsing.declaration import Declaration


class koocParser(Grammar, Declaration):
    entry = "translation_unit"
    grammar = """
       declaration =
       [
           Declaration.declaration
           | kooc_declaration
       ]

       kooc_declaration = 
       [
           import_declaration
           | module_declaration
           | module_implementation
       ]

       import_declaration = 
       [
           '@import \"' id:file_to_import '\"' 
           #add_import(_, file_to_import)
       ]

       module_declaration = 
       [
           '@module ' id:module_name Statement.compound_statement:st
           #add_module_declaration(_, module_name, st)
       ]

       module_implementation = 
       [
           '@implementation ' id:module_name 
           [
               declaration    
           ]
           #add_module_implementation(_, module_name)
       ]

"""

@meta.hook(koocParser)
def add_import(self, ast, file_to_import):
    pass
    return True

@meta.hook(koocParser)
def add_module_declaration(self, ast, module_name):
    print("ok")
    return True

@meta.hook(koocParser)
def add_module_implementation(self, ast, module_name):
    pass
    return True
