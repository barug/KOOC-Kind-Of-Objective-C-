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
               module_declaration
               | module_implementation
           ]

               module_declaration = 
               [
                   "@module " id:module_name Statement.compound_statement:st
                   #module_declaration(current_block, module_name, st)
                   #end_decl(current_block, decl
               ]

               module_implementation = 
               [
                   "@implementation " id:module_name Statement.compound_statement:st
                   #add_module_implementation(current_block, module_name, st)
               ]

"""

@meta.hook(koocParser)
def add_import(self, ast, file_to_import):
    return True

@meta.hook(koocParser)
def add_module_declaration(self, ast, module_name, st):
    print("ok")
    print(st)
    return True

@meta.hook(koocParser)
def add_module_implementation(self, ast, module_name, st):
    return True
