#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

from pyrser.grammar import Grammar
from pyrser import meta
from pyrser.parsing.node import Node
from cnorm.parsing.declaration import Declaration
from cnorm.parsing.expression import Expression
import koocClasses

class koocParser(Grammar, Declaration):

    entry = "translation_unit"
    grammar = """
       declaration =
       [
           Declaration.declaration
           | kooc_declaration
       ]

       primary_expression =
       [
           Expression.primary_expression:>_
           | kooc_expression:>_
       ]

           kooc_expression =
           [
              ["@!("Base.id:KoocType')'] [
                                         '[' id:Kclass'.'id:attribut ']' #kooc_var(_, KoocType, Kclass, attribut)
                                         | '[' id:Kclass id:func [ ':'expression ]*:var  ']' #kooc_func(_, KoocType, Kclass, func, var)
                                         ]
           ]

           kooc_declaration =
           [
               module_declaration
               | module_implementation
               | module_import
               | class_declaration
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
                   "@import " id:module_name ".kh"
                   #add_module_import(module_name, current_block)
               ]

               class_declaration =
               [
                   "@class " id:class_name class_statement:st
                   #add_class_declaration(class_name, st, current_block)
               ]

                  class_statement =
                  [
                       '{'
                       __scope__:current_block
                       #new_blockstmt(_, current_block)
                       [
                            line_of_code
                            | class_member
                       ]*
                       '}'
                  ]

                      class_member =
                      [
                           "@member" class_member_statement:st
                           #add_member_declaration(class_name, st, current_block)
                      ]

                          class_member_statement =
                          [
                               Statement.compound_statement:>_
                               | [
                                   __scope__:current_block
                                   #new_blockstmt(_, current_block) line_of_code
                                 ]
                          ]

"""

@meta.hook(koocParser)
def add_module_declaration(self, module_name, st, current_block):
    decl = koocClasses.ModuleDeclaration(self.value(module_name), st)
    current_block.ref.body.append(decl)
    return True

@meta.hook(koocParser)
def add_module_implementation(self, module_name, st, current_block):
    decl = koocClasses.ModuleImplementation(self.value(module_name), st)
    current_block.ref.body.append(decl)
    return True

@meta.hook(koocParser)
def add_module_import(self, module_name, current_block):
    decl = koocClasses.ModuleImport(self.value(module_name))
    current_block.ref.body.append(decl)
    decl.translate()
    return True

@meta.hook(koocParser)
def add_class_declaration(self, class_name, st, current_block):
    decl = koocClasses.ClassDeclaration(self.value(class_name), st)
    current_block.ref.body.append(decl)
    return True

@meta.hook(koocParser)
def add_member_declaration(self, class_name, st, current_block):
    decl = koocClasses.ClassMember(self.value(class_name), st)
    current_block.ref.body.append(decl)
    return True

@meta.hook(koocParser)
def kooc_var(self, current_block, type, Kclass, attr):
    decl = koocClasses.VariableCall(self.value(type), self.value(Kclass), self.value(attr))
    current_block.set(decl)
    # current_block.ref.body.append(decl)
    return True

@meta.hook(koocParser)
def kooc_func(self, current_block, type, Kclass, func, var):
    decl = koocClasses.FunctionCall(self.value(type), self.value(Kclass), self.value(func), self.value(var))
    current_block.set(decl)
    # current_block.ref.body.append(decl)
    return True
