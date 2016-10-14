#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyrser.parsing.node import Node
from cnorm.parsing.declaration import Declaration
from cnorm.nodes import *
from koocClasses import *

class KoocTranslator:

    def __init__(self):
        self.symbolTable = {}

    def mangle_symbol(self, moduleName, declarationNode):
        print("enter mangle")
        # mangledName = "_K" + str(len(moduleName)) + moduleName \
        # + str(len(declarationNode._name)) + declarationNode._name
        # if (isinstance(declarationNode._ctype, PrimaryType)):
        #     print("primary")
        # if (isinstance(declarationNode._ctype, FuncType)):
        #     print("func")

    def translateKoocAst(self, node):
        pass
        # if (isinstance(node, KoocDeclaration)):
        #     print("isInstance")
        #     print(node)
        #     for declaration in node.compoundDeclaration.body:
        #         self.mangle_symbol(node.moduleName, declaration)
        # elif (hasattr(node, "body")):
        #     for childNode in node.body:
        #         self.translateKoocAst(childNode)

    def mangling(self,koocModule):
        symbols = []
