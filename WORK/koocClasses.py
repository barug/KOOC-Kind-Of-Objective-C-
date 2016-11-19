#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

from pyrser.parsing.node import Node
from cnorm import nodes

class KoocNode(Node):
    def translate(self):
        pass

class KoocDeclaration(KoocNode):
    def translate(self):
        pass

class KoocStatement(KoocNode):
    def translate(self):
        pass

class ModuleDeclaration(KoocDeclaration):
    def __init__(self, moduleName, compoundDeclaration):
        self._name = moduleName
        self.compoundDeclaration = compoundDeclaration

    def translate(self):
        pass                    # code goes here

class ModuleImplementation(KoocDeclaration):
    def __init__(self, moduleName, compoundDeclaration):
        self._name = moduleName
        self.compoundDeclaration = compoundDeclaration

    def translate(self):
        pass                    # code goes here

class ModuleImport(KoocStatement):
    def __init__(self, moduleName, ast):
        self.moduleName = "@import \"" + moduleName + ".kh\"\n"
        self.ast = ast

    def translate(self):
        pass

class ClassDeclaration(KoocDeclaration):
    def __init__(self, className, compoundDeclaration, parent_class = None):
        self._name = className
        self.compoundDeclaration = compoundDeclaration
        self.parent_class = parent_class

    def translate(self):
        pass

class ClassMember(KoocDeclaration):
    def __init__(self, className, compoundDeclaration):
        self.className = className
        self.compoundDeclaration = compoundDeclaration

    def translate(self):
        pass

class ClassVirtual(KoocDeclaration):
    def __init__(self, className, compoundDeclaration):
        self.className = className
        self.compoundDeclaration = compoundDeclaration

    def translate(self):
        pass

class VariableCall(KoocStatement) :
    def __init__(self, type, Kclass, attr):
        self.type = type
        self.Kclass = Kclass
        self.attr = attr

    def translate(self):
        pass

class FunctionCall(KoocStatement) :
    def __init__(self, type, Kclass, func, var):
        self.type = type
        self.Kclass = Kclass
        self.func = func
        self.argv = []
        var = var.split()
        for arg in var :
            pars = arg.split(')')
            pars[0] = pars[0][2:]
            self.argv.append(pars)

    def translate(self):
        pass
