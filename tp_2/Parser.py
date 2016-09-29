#!/usr/bin/env python3
# -*- coding: utf-8 -*-    


##
##   BEGIN AND END PARSER FOR PISCINE J05
##



from pyrser import grammar, meta
from pyrser.grammar import Grammar
from cnorm.parsing.declaration import Declaration
from cnorm.passes import to_c
from sys import argv as av

class Parser(Grammar, Declaration):
    entry = 'init'
    grammar = """
    init = [#init_storage [Declaration.translation_unit:>_]]
    
    c_decl = [begin_decl | end_decl | Declaration.c_decl]

    begin_decl = [["@begin("id:name')' #init_begin(_, name)]
    '{' [[line_of_code:>_]:new_line #set_begin_line(_, name, new_line)]* '}' #push_begin(_, name)]
 
    end_decl = [["@end("id:name')' #init_end(_, name)]
    '{' [[Declaration.line_of_code:>_]:new_line #set_end_line(_, name, new_line)]* '}' #push_end(_, name)]
    """
    
    def inject_begin(self, ast):
        for name, line in self.begin_dict.items():
            func = ast.func(name)
            func.body.body.insert(0, self.parse(line))
            return (True)

    def inject_end(self):
        pass

@meta.hook(AspectC)
def init_storage(self):
    self.begin_dict = {}
    self.end_dict = {}
    return True

@meta.hook(AspectC)
def init_begin(self, ast, name):
    if (not str(self.value(name)) in self.begin_dict):
        self.begin_dict[str(self.value(name))] = ""
    self.begin_line = ""
    return True

@meta.hook(AspectC)
def init_end(self, ast, name):
    if (not str(self.value(name)) in self.end_dict):
        self.end_dict[str(self.value(name))] = ""
    self.end_line = ""
    return True 

@meta.hook(AspectC)
def set_begin_line(self, ast, name, decl):
    self.begin_line += str(self.value(decl))
    return True

@meta.hook(AspectC)
def set_end_line(self, ast, name, decl):
    self.end_line += str(self.value(decl))
    return True

@meta.hook(AspectC)
def push_begin(self, ast, name):
    self.begin_dict[str(self.value(name))] = self.begin_line + self.begin_dict[str(self.value(name))]
    return (True)

@meta.hook(AspectC)
def push_end(self, ast, name):
    self.end_dict[str(self.value(name))] = self.end_line + self.begin_dict[str(self.value(name))]
    return (True)
