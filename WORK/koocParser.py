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
                   __scope__: decl
                   "@module " id:module_name Statement.compound_statement:st
                   #module_declaration(decl, module_name, st, current_block)

               ]

               module_implementation = 
               [
                   __scope__: decl
                   "@implementation " id:module_name Statement.compound_statement:st
                   #module_implementation(decl, module_name, st, current_block)
               ]

               module_import = 
               [
                   __scope__: decl
                   "@import " id:module_name".kh"
                   #module_import(decl, module_name, current_block)
               ]
"""

@meta.hook(koocParser)
def module_declaration(self, decl, module_name, st, ast):
    decl = koocClasses.moduleDeclaration(self.value(module_name), st)
    ast.ref.body.append(decl)
    return True

@meta.hook(koocParser)
def module_implementation(self, decl, module_name, st, ast):
    decl = koocClasses.moduleImplementation(self.value(module_name), st)
    ast.ref.body.append(decl)
    return True

@meta.hook(koocParser)
def module_import(self, decl, module_name, ast):
    decl = koocClasses.moduleImport(self.value(module_name))
    ast.ref.body.append(decl)
    return True
