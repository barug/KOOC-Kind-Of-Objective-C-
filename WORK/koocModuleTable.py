
class KoocModuleTable:
    NON_MEMBER = 0
    MEMBER = 1
    VIRTUAL = 2
    
    def __init__(self):
        self.nonMemberTables = {}
        self.membersTables = {}
        self.virtualsTables = {}
        self.instancesStructs = {}
        self.parentClasses = {}
        
    def addModule(self, moduleName):
        self.nonMemberTables[moduleName] = {}
        self.membersTables[moduleName] = {}
        self.virtualsTables[moduleName] = {}

    def hasModule(self, moduleName):
        return moduleName in self.nonMemberTables
        
    def addSymbol(self, moduleName, unMangledName, mangledSymbolNode, Stype):
        if Stype == KoocModuleTable.NON_MEMBER:
            table = self.nonMemberTables[moduleName]
        elif Stype == KoocModuleTable.MEMBER:
            table = self.membersTables[moduleName]
        elif Stype == KoocModuleTable.VIRTUAL:
            table = self.virtualsTables[moduleName]
        if unMangledName not in table:
            table[unMangledName] = []
        table[unMangledName].append(mangledSymbolNode)

    def addParentClass(self, className, parentName):
        self.parentClasses[className] = parentName

    def getParentClass(self, className):
        return self.parentClasses[className]

    def getParentStruct(self, className):
        return self.instancesStructs[self.parentClasses[className]]
    
    def getParentClassSymbols(self, className, unMangledName, Stype):
        if Stype == KoocModuleTable.NON_MEMBER:
            return self.nonMembersTable[self.parentClasses[className]][unMangledName]
        elif Stype == KoocModuleTable.MEMBER:
            return self.membersTables[self.parentClasses[className]][unMangledName]
        elif Stype == KoocModuleTable.VIRTUAL:
            return self.virtualsTables[self.parentClasses[className]][unMangledName]
        
    def addInstanceStruct(self, className, structName):
        self.instancesStructs[className] = structName

    def getInstanceStruct(self, className):
        if className in self.instancesStructs:
            return self.instancesStructs[className]
        else:
            return None
    
    def getAllSymbolLists(self, moduleName, Stype):
        if Stype == KoocModuleTable.NON_MEMBER:
            table = self.nonMemberTables
        elif Stype == KoocModuleTable.MEMBER:
            table = self.membersTables
        elif Stype == KoocModuleTable.VIRTUAL:
            table = self.virtualsTables
        if moduleName in table:
            return table[moduleName]
        else:
            return None
        
        
    def getSymbolList(self, moduleName, unMangledName, Stype):
        if Stype == KoocModuleTable.NON_MEMBER:
            table = self.nonMemberTables
        elif Stype == KoocModuleTable.MEMBER:
            table = self.membersTables
        elif Stype == KoocModuleTable.VIRTUAL:
            table = self.virtualsTables
        if moduleName in table:
            if unMangledName in table[moduleName]:
                return table[moduleName][unMangledName]
            else:
                return None
        else:
            return None

    def setSymbolList(self, moduleName, symbolList, Stype):
        if Stype == KoocModuleTable.NON_MEMBER:
            self.nonMemberTables[moduleName] = symbolList
        elif Stype == KoocModuleTable.MEMBER:
            self.membersTables[moduleName] = symbolList
        elif Stype == KoocModuleTable.VIRTUAL:
            self.virtualsTables[moduleName] = symbolList
        
        
    # def __str__(self):
    #     stringRep = ""
    #     for moduleName, symbolDict in self.nonMembersTable.items():
    #         stringRep += "module " + moduleName +":\n"
    #         for unMangledName, symbolList in symbolDict.items():
    #             stringRep += "\t" + unMangledName + ":\n"
    #             for symbolNode in symbolList:
    #                 stringRep += "\t\t" + symbolNode._name + "\n"
    #         for unMangledName, memberList in self.membersTables[moduleName].items():
                
    #     return stringRep
                
