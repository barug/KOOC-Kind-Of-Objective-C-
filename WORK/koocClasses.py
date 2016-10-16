#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

from pyrser.parsing.node import Node
from cnorm import nodes

class KoocNode(Node):
    def translate(self):
        pass
    pass

class KoocDeclaration(KoocNode):
    def translate(self):
        pass
    pass

class KoocStatement(KoocNode):
    def translate(self):
        pass
    pass

class ModuleDeclaration(KoocDeclaration):
    def __init__(self, moduleName, compoundDeclaration):
        self.moduleName = moduleName
        self.compoundDeclaration = compoundDeclaration

    def translate(self):
        pass                    # code goes here

class ModuleImplementation(KoocDeclaration):
    def __init__(self, moduleName, compoundDeclaration):
        self.moduleName = moduleName
        self.compoundDeclaration = compoundDeclaration

    def translate(self):
        pass                    # code goes here

class ModuleImport(KoocStatement):
    def __init__(self, moduleName):
        self.moduleName = moduleName

    def translate(self):
        decl = nodes.Raw
        decl.value = "#include \"" + self.moduleName + ".h\"\n"
        return (decl)

class ClassDeclaration(KoocDeclaration):
    def __init__(self, className, compoundDeclaration):
        self.className = className
        self.compoundDeclaration = compoundDeclaration

    def translate(self):
        pass

class ClassMember(KoocDeclaration):
    def __init__(self, className, compoundDeclaration):
        self.className = className
        self.compoundDeclaration = compoundDeclaration

    def translate(self):
        pass

class KoocExpression(KoocStatement):
    def __init__(self, statement):
        self.statement = statement
    
    def translate(self):
        pass
