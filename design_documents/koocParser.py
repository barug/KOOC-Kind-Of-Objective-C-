#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-    

from pyrser.grammar import Grammar
from pyrser import meta
from pyrser.parsing.node import Node
from cnorm.parsing.declaration import Declaration
import koocClasses

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
               [ module_declaration
               | module_implementation ]:decl
               #end_decl(current_block, decl)
           ]

               module_declaration = 
               [
                   "@module " id:module_name Statement.compound_statement:st
                   #module_declaration(_, module_name, st)
               ]

               module_implementation = 
               [
                   "@implementation " id:module_name Statement.compound_statement:st
                   #module_implementation(_, module_name, st)
               ]
"""

@meta.hook(koocParser)
def module_declaration(self, decl, module_name, st):
    decl = koocClasses.moduleDeclaration(self.value(module_name), module_name)
    print(decl)
    return True

@meta.hook(koocParser)
def test(self, decl):
    print(decl)
    return True

@meta.hook(koocParser)
def module_implementation(self, decl, module_name, st):
    decl = koocClasses.moduleImplementation(self.value(module_name), module_name)
    return True
