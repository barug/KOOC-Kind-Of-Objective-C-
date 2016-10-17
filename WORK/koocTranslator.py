#!/usr/bin/env python3
# -*- coding: utf-8 -*-   

from pyrser.parsing.node import Node
from cnorm.parsing.declaration import Declaration
from cnorm.nodes import *
from koocClasses import *

class KoocTranslator:
    
    def __init__(self):
        self.symbolTable = {}

    def add_mangled_type(self, ctype, mangledName):
        mangledName += str(len(ctype._identifier)) + ctype._identifier
        decltype = ctype._decltype
        while decltype:
            mangledName += 'P'
            decltype = decltype._decltype
        return mangledName

    def mangle_symbol(self, moduleName, declarationNode):
        mangledName = "_K" + str(len(moduleName)) + moduleName \
        + str(len(declarationNode._name)) + declarationNode._name
        if (type(declarationNode._ctype) is PrimaryType):
            mangledName += "T"
            mangledName = self.add_mangled_type(declarationNode._ctype, mangledName)
        if (type(declarationNode._ctype) is FuncType):
            mangledName += "R"
            mangledName = self.add_mangled_type(declarationNode._ctype, mangledName)
            mangledName += "A" + str(len(declarationNode._ctype.params)) + "_"
            for param in declarationNode._ctype.params:
                mangledName = self.add_mangled_type(param._ctype, mangledName)
        print(mangledName)
        declarationNode._name = mangledName

    def translate_declaration(self, declarationNode):
        for declaration in declarationNode.compoundDeclaration.body:
            self.mangle_symbol(declarationNode.moduleName, declaration)
        return declarationNode.compoundDeclaration.body
            
    def translateKoocAst(self, node):
        if (isinstance(node, KoocDeclaration)):
            self.translate_declaration(node)
        elif (hasattr(node, "body")):
            for childNode in node.body:
                self.translateKoocAst(childNode)
        
    def mangling(self,koocModule):
        symbols = []
        
