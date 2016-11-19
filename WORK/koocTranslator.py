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
        for memberName, symbolList in nonMembers.items():
            for symbol in symbolList:
                if (type(symbol._ctype) is PrimaryType):
                    variableImpl = copy.deepcopy(symbol)
                    variableImpl._assign_expr = variableImpl._koocVarVal
                    variableImpl._ctype._storage = Storages.AUTO
                    self.newRootBody.append(variableImpl)
        for implementation in implementationNode.compoundDeclaration.body:
            self.mangle_symbol(implementationNode._name,
                               implementation)
            self.newRootBody.append(implementation)
            
            

    # def translateImplementation(self, implementationModule):
    #     self.moduleTable.addModule(moduleNode._name)        
    #     for declaration in moduleNode.compoundDeclaration.body:
    #         unMangledName = declaration._name
    #         self.mangle_symbol(moduleNode._name,
    #                            declaration)
    #         if (isinstance(declaration._ctype, PrimaryType)):
    #             declaration._ctype._storage = Storages.EXTERN
    #         self.moduleTable.addSymbol(moduleNode._name,
    #                                    unMangledName,
    #                                    declaration,
    #                                    KoocModuleTable.MEMBER)
    #         self.newRootBody.append(declaration)
            
    def translateClass(self, classNode):
        self.moduleTable.addModule(classNode._name)
        structName = "_" + classNode._name + "_instance_struct_"
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
                        member._ctype.params.insert(0, selfNode)
                        self.newRootBody.append(member)
                    else:
                        ctype.fields.append(member)
            else:
                unMangledName = declaration._name
                self.mangle_symbol(classNode._name,
                                   declaration)
                if (isinstance(declaration, nodes.PrimaryType)):
                    declaration._storage = Storages.EXTERN
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
        print(instanceDeclNode.to_yml())
        print(allocNode.to_yml())
        self.moduleTable.addSymbol(classNode._name,
                                   "alloc",
                                   allocName,
                                   KoocModuleTable.NON_MEMBER)
        self.newRootBody.append(allocNode)
        
    def translateKoocExpression(self, expressionNode):
        pass

    def searchKoocExpression(self, scope):
        pass

    def translateKoocAst(self, rootNode):
        for node in rootNode.body:
            if isinstance(node, ModuleDeclaration):
                self.translateModule(node)
            elif isinstance(node, ClassDeclaration):
                self.translateClass(node)
            elif isinstance(node, ModuleImplementation):
                self.translateImplementation(node)
            else:
                self.newRootBody.append(node)
        rootNode.body = self.newRootBody
        print(self.moduleTable)
