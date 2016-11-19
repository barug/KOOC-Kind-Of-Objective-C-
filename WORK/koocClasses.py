#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

from pyrser.parsing.node import Node
from cnorm import nodes

class KoocNode(Node):
    pass

class KoocDeclaration(KoocNode):
    pass

class KoocStatement(KoocNode):
    pass

class ModuleDeclaration(KoocDeclaration):
    def __init__(self, moduleName, compoundDeclaration):
        self._name = moduleName
        self.compoundDeclaration = compoundDeclaration

class ModuleImplementation(KoocDeclaration):
    def __init__(self, moduleName, compoundDeclaration):
        self._name = moduleName
        self.compoundDeclaration = compoundDeclaration

class ModuleImport(KoocStatement):
    def __init__(self, moduleName, ast):
        self.moduleName = "@import \"" + moduleName + ".kh\"\n"
        self.ast = ast

class ClassDeclaration(KoocDeclaration):
    def __init__(self, className, compoundDeclaration, parent_class = None):
        self._name = className
        self.compoundDeclaration = compoundDeclaration
        self.parent_class = parent_class

class ClassMember(KoocDeclaration):
    def __init__(self, className, compoundDeclaration):
        self.className = className
        self.compoundDeclaration = compoundDeclaration

class ClassVirtual(KoocDeclaration):
    def __init__(self, className, compoundDeclaration):
        self.className = className
        self.compoundDeclaration = compoundDeclaration

class VariableCall(KoocStatement) :
    def __init__(self, type, Kclass, attr):
        self.type = type
        self.Kclass = Kclass
        self.attr = attr

class FunctionCall(KoocStatement) :
    def __init__(self, type, Kclass, func, var):
        self.type = type
        self.Kclass = Kclass
        self.func = func
        self.params = []
        print (var)
        var = var.split(':')
        for arg in var :
            if (arg != '') :
                print ('[' + arg + ']')
            # pars = arg.split(')')
            # pars[0] = pars[0][1:]
                self.params.append(arg)
