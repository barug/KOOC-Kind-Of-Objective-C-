#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
from pyrser.parsing.node import Node
from cnorm.parsing.declaration import Declaration
from cnorm.nodes import *
from koocClasses import *
from koocModuleTable import KoocModuleTable
from collections import ChainMap

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
        declarationNode._name = mangledName

    def translateModule(self, moduleNode):
        self.moduleTable.addModule(moduleNode._name)        
        for declaration in moduleNode.compoundDeclaration.body:
            unMangledName = declaration._name
            self.mangle_symbol(moduleNode._name,
                               declaration)
            if (type(declaration._ctype) is PrimaryType):
                declaration._ctype._storage = Storages.EXTERN
                if (hasattr(declaration, "_assign_expr")):
                    declaration._koocVarVal = declaration._assign_expr
                    delattr(declaration, "_assign_expr")
            self.moduleTable.addSymbol(moduleNode._name,
                                       unMangledName,
                                       declaration,
                                       KoocModuleTable.NON_MEMBER)
            self.newRootBody.append(declaration)

    def translateImplementation(self, implementationNode):
        nonMembers = self.moduleTable.getAllSymbolLists(implementationNode._name,
                                                        KoocModuleTable.NON_MEMBER)
        structName = self.moduleTable.getInstanceStruct(implementationNode._name)
        if (structName is not None):
            selfNode = nodes.Decl('self', nodes.PrimaryType(structName))
            selfNode._ctype._decltype = nodes.PointerType()
            selfNode._ctype._storage = Storages.AUTO
            selfNode._ctype._specifier = Specifiers.AUTO
        for nonMemberName, symbolList in nonMembers.items():
            for symbol in symbolList:
                if (type(symbol._ctype) is PrimaryType):
                    variableImpl = copy.deepcopy(symbol)
                    variableImpl._assign_expr = variableImpl._koocVarVal
                    variableImpl._ctype._storage = Storages.AUTO
                    self.newRootBody.append(variableImpl)
        for implementation in implementationNode.compoundDeclaration.body:
            if type(implementation) is ClassMember:
                for member in implementation.compoundDeclaration.body:
                    if isinstance(member._ctype, FuncType):
                        self.mangle_symbol(implementationNode._name,
                                           member)
                        member._ctype.params.insert(0, selfNode)
                        member._className = implementationNode._name
                        self.searchKoocExpression(member, ChainMap())
                        self.newRootBody.append(member)
            else:
                self.mangle_symbol(implementationNode._name,
                                   implementation)
                self.newRootBody.append(implementation)
            
    def translateClass(self, classNode):
        self.moduleTable.addModule(classNode._name)
        structName = "_" + classNode._name + "_instance_struct_"
        self.moduleTable.addInstanceStruct(classNode._name, structName)
        instanceStructNode = nodes.Decl(structName)
        self.newRootBody.append(instanceStructNode)
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
                    if not isinstance(symbol._ctype, nodes.FuncType):
                        ctype.fields.append(symbol)
        for declaration in classNode.compoundDeclaration.body:
            if isinstance(declaration, ClassMember):
                for member in declaration.compoundDeclaration.body:
                    unMangledName = member._name
                    self.mangle_symbol(classNode._name,
                                       member)
                    self.moduleTable.addSymbol(classNode._name,
                                               unMangledName,
                                               member,
                                               KoocModuleTable.MEMBER)
                    if isinstance(member._ctype, FuncType):
                        bodyNode = copy.deepcopy(member)
                        bodyNode._ctype.params.insert(0, selfNode)
                        self.newRootBody.append(bodyNode)
                    else:
                        ctype.fields.append(member)
            else:
                unMangledName = declaration._name
                self.mangle_symbol(classNode._name,
                                   declaration)
                if (type(declaration._ctype) is PrimaryType):
                    declaration._storage = Storages.EXTERN
                    if (hasattr(declaration, "_assign_expr")):
                        declaration._koocVarVal = declaration._assign_expr
                        delattr(declaration, "_assign_expr")
                self.moduleTable.addSymbol(classNode._name,
                                           unMangledName,
                                           declaration,
                                           KoocModuleTable.NON_MEMBER)
                self.newRootBody.append(declaration)

        allocName = "_" + classNode._name + "_alloc_";
        allocNode = nodes.Decl(allocName, nodes.FuncType(structName))
        allocNode._ctype._decltype = nodes.PointerType()
        allocBody = []
        instanceDeclNode = nodes.Decl("newInstance", nodes.PrimaryType(structName))
        instanceDeclNode._ctype._decltype = PointerType()
        mallocNode = nodes.Func(nodes.Id("malloc"),
                                [nodes.Sizeof(nodes.Id("sizeof"),
                                              [nodes.PrimaryType(structName)])])
        instanceDeclNode._assign_expr = mallocNode
        allocBody.append(instanceDeclNode)
        allocBody.append(nodes.Return(nodes.Id("newInstance")))
        allocNode.body = nodes.BlockStmt(allocBody)
        self.moduleTable.addSymbol(classNode._name,
                                   "alloc",
                                   allocNode,
                                   KoocModuleTable.NON_MEMBER)
        self.newRootBody.append(allocNode)

    def getFunctionSymbol(self, exprNode, symbol):
        params = []
        if ((type(symbol._ctype) is FuncType)
            and (len(exprNode.params) == len(symbol._ctype._params))):
            print ("found function: " + str(symbol))
            for i in range(0, len(exprNode.params)):
                if (type(exprNode.params[i]) is Cast):
                    print(str(exprNode.params[i]))
                    print(str(symbol._ctype._params[0]))
                    if (exprNode.params[i].params[0]._identifier
                    != symbol._ctype._params[i]._ctype._identifier):
                        return None
                    else:
                        params.append(exprNode.params[i].params[1])
        else:
            return None
        funcNode = nodes.Func(nodes.Id(symbol._name), params)
        print("found right function")
        return funcNode

    def translateSelfExpression(self, exprNode):
        print ("enter self expression: " + str(exprNode))
        if (isinstance(exprNode, VariableCall)):
            return nodes.Arrow(nodes.Id("self"), [nodes.Id(exprNode.name)])
        return None

    def translateMemberCall(self, exprNode, className):
        print("entering member call")
        print(className)
        print(exprNode.Kclass)
        symbolList = self.moduleTable.getSymbolList(className,
                                                    exprNode.name,
                                                    KoocModuleTable.MEMBER)
        print(str(exprNode))
        if symbolList is not None:
            print ("found symbol")
            for symbol in symbolList:
                print (str(symbol))
                funcNode = self.getFunctionSymbol(exprNode, symbol)
                if funcNode is not None:
                    funcNode.params.insert(0, nodes.Id(exprNode.Kclass))
                    exprNode = funcNode
                    return exprNode
        return None
                    
                
        
    
    def translateKoocExpression(self, exprNode, scopeMaps):
        print ("entering translate:")
        if (exprNode.Kclass == "self"):
            return self.translateSelfExpression(exprNode)
        if ((not self.moduleTable.hasModule(exprNode.Kclass))
        and (exprNode.Kclass in scopeMaps)):
            return self.translateMemberCall(exprNode,
                                            scopeMaps[exprNode.Kclass])
        symbolList = self.moduleTable.getSymbolList(exprNode.Kclass,
                                                    exprNode.name,
                                                    KoocModuleTable.NON_MEMBER)
        if symbolList is not None:
            if (isinstance(exprNode, VariableCall)):
                print("symbolList: " + str(symbolList))
                for symbol in symbolList:
                    if (symbol._ctype._identifier == exprNode.type):
                        print("symbol :" + str(symbol))
                        exprNode = nodes.Id(symbol._name)
            if (isinstance(exprNode, FunctionCall)):
                for symbol in symbolList:
                    funcNode = self.getFunctionSymbol(exprNode, symbol)
                    if funcNode is not None:
                        print("found corresponding function")
                        exprNode = funcNode 
                        
        print (str(exprNode))
        return exprNode

    def searchKoocExpression(self, node, scopeMaps):
        # print(str(node))
        if (type(node) is BlockStmt):
            scopeMaps = scopeMaps.new_child()
        if ((type(node) is Decl)
        and(type(node._ctype) is PrimaryType)):
            if self.moduleTable.hasModule(node._ctype._identifier):
                scopeMaps[node._name] = node._ctype._identifier
                print(str(scopeMaps))
                node._ctype._identifier = self.moduleTable.getInstanceStruct(node._ctype._identifier)
        if (hasattr(node, "__dict__")):
            for attrName, attrValue in node.__dict__.items():
                # print(str(attrValue))
                setattr(node, attrName, self.searchKoocExpression(attrValue, scopeMaps))
        if (type(node) == list):
            for i in range(0, len(node)):
                node[i] = self.searchKoocExpression(node[i], scopeMaps)
        if isinstance(node, KoocStatement):
            node = self.translateKoocExpression(node, scopeMaps)
        return node

    def translateImport(self, importNode):
        newRootSave = self.newRootBody
        self.newRootBody = []
        self.translateKoocAst(importNode.ast)
        self.newRootBody = newRootSave
        self.newRootBody.append(nodes.Raw('#include "' + importNode.moduleName + '.h"\n'))
    
    def translateKoocAst(self, rootNode):
        for node in rootNode.body:
            if isinstance(node, ModuleDeclaration):
                self.translateModule(node)
            elif isinstance(node, ClassDeclaration):
                self.translateClass(node)
            elif isinstance(node, ModuleImplementation):
                self.translateImplementation(node)
            elif isinstance(node, ModuleImport):
                self.translateImport(node)
            else:
                node = self.searchKoocExpression(node, ChainMap())
                self.newRootBody.append(node)
        rootNode.body = self.newRootBody
        print(self.moduleTable)
