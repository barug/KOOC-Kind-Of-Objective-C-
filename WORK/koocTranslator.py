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
        # print(mangledName)
        declarationNode._name = mangledName
            
    def translateKoocAst(self, rootNode):
        rootBodyCopy = rootNode.body[:]
        for node in rootBodyCopy:
            if (isinstance(node, KoocDeclaration)):
                for declaration in node.compoundDeclaration.body:
                    self.mangle_symbol(node.moduleName, declaration)
                nodeIndex = rootNode.body.index(node)
                rootNode.body[nodeIndex:nodeIndex] = node.compoundDeclaration.body
                rootNode.body.remove(node)
