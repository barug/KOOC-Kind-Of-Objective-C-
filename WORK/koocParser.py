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
               module_declaration
               | module_implementation
               | module_import
           ]

               module_declaration = 
               [
                   "@module " id:module_name Statement.compound_statement:st
                   #add_module_declaration(module_name, st, current_block)

               ]

               module_implementation = 
               [
                   "@implementation " id:module_name Statement.compound_statement:st
                   #add_module_implementation(module_name, st, current_block)
               ]

               module_import = 
               [
                   "@import " id:module_name".kh"
                   #add_module_import(module_name, current_block)
               ]

"""

@meta.hook(koocParser)
def add_module_declaration(self, module_name, st, current_block):
    decl = koocClasses.moduleDeclaration(self.value(module_name), st)
    current_block.ref.body.append(decl)
    return True

@meta.hook(koocParser)
def add_module_implementation(self, module_name, st, current_block):
    decl = koocClasses.moduleImplementation(self.value(module_name), st)
    current_block.ref.body.append(decl)
    return True

@meta.hook(koocParser)
def add_module_import(self, module_name, current_block):
    decl = koocClasses.moduleImport(self.value(module_name))
    current_block.ref.body.append(decl)
    decl.translate()
    return True
