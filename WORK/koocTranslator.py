#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
from pyrser.parsing.node import Node
from cnorm.parsing.declaration import Declaration
from cnorm.nodes import *
from koocClasses import *
from koocModuleTable import KoocModuleTable

class KoocTranslator:

    def __init__(self):
        self.moduleTable = KoocModuleTable()
        self.newRootBody = []
    def add_mangled_type(self, ctype, mangledName):
        mangledName += str(len(ctype._identifier)) + ctype._identifier
        decltype = ctype._decltype
        while decltype:
            mangledName += 'P'
            decltype = decltype._decltype
        return mangledName

    def mangle_symbol(self,
                      moduleName,
                      declarationNode):
        mangledName = "_K" + str(len(moduleName)) + moduleName \
        + str(len(declarationNode._name)) + declarationNode._name
        if (type(declarationNode._ctype) is PrimaryType):
            mangledName += "T"
            mangledName = self.add_mangled_type(declarationNode._ctype,
                                                mangledName)
        if (type(declarationNode._ctype) is FuncType):
            mangledName += "R"
            mangledName = self.add_mangled_type(declarationNode._ctype,
                                                mangledName)
            mangledName += "A" + str(len(declarationNode._ctype.params)) + "_"
            for param in declarationNode._ctype.params:
                mangledName = self.add_mangled_type(param._ctype,
                                                    mangledName)
        # print(mangledName)
        declarationNode._name = mangledName

    def translateModule(self, moduleNode):
        self.moduleTable.addModule(node._name)        
        for declaration in node.compoundDeclaration.body:
            unMangledName = declaration._name
            self.mangle_symbol(node._name,
                               declaration)
            self.moduleTable.addSymbol(node._name,
                                       unMangledName,
                                       declaration)
            self.newRootBody.append(declaration)
            
    def translateClass(self, classNode):
        self.moduleTable.addModule(classNode._name)
        structName = "_" + classNode._name + "_instance_struct_"
        instanceStructNode = nodes.Decl(structName)
        ctype = nodes.ComposedType(structName)
        instanceStructNode._ctype = ctype
        ctype._storage = Storages.TYPEDEF
        ctype._specifier = nodes.Specifiers.STRUCT
        ctype.fields = []
        parentName = classNode.parent_class
        selfNode = nodes.Decl('self', nodes.PrimaryType(structName))
        selfNode._ctype._decltype = nodes.PointerType()
        selfNode._ctype._storage = Storages.AUTO
        selfNode._ctype._specifier = Specifiers.AUTO
        
        if (parentName is not None
            and self.moduleTable.hasModule(parentName)):
            SymbolLists = self.moduleTable.getAllSymbolLists(parentName,
                                                             KoocModuleTable.MEMBER)
            for key, symbolList in SymbolLists.items():
                for symbol in symbolList:
                    ctype.fields.append(symbol)
        for declaration in classNode.compoundDeclaration.body:
            if isinstance(declaration, ClassMember):
                for member in declaration.compoundDeclaration.body:
                    unMangledName = member._name
                    self.mangle_symbol(classNode._name,
                                       member)
                    if isinstance(member._ctype, FuncType):
                        member._ctype.params.insert(0, selfNode)
                    self.moduleTable.addSymbol(classNode._name,
                                               unMangledName,
                                               member,
                                               KoocModuleTable.MEMBER)
                ctype.fields.append(member)
            else:
                unMangledName = declaration._name
                self.mangle_symbol(classNode._name,
                                   declaration)
                self.moduleTable.addSymbol(classNode._name,
                                           unMangledName,
                                           declaration,
                                           KoocModuleTable.NON_MEMBER)
                self.newRootBody.append(declaration)
        self.newRootBody.append(instanceStructNode)
        
        
        
    def translateKoocAst(self, rootNode):
        for node in rootNode.body:
            if isinstance(node, ModuleDeclaration):
                self.translateModule(node)
            elif isinstance(node, ClassDeclaration):
                self.translateClass(node)
            else:
                self.newRootBody.append(node)
        rootNode.body = self.newRootBody
        print(self.moduleTable)
