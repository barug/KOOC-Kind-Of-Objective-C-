
class KoocModuleTable:
    NON_MEMBER = 0
    MEMBER = 1
    VIRTUAL = 2
    
    def __init__(self):
        self.nonMemberTables = {}
        self.membersTables = {}
        self.virtualsTables = {}
        
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

    def getAllSymbolLists(self, moduleName, Stype):
        if Stype == KoocModuleTable.NON_MEMBER:
            return self.nonMemberTables[moduleName]
        if Stype == KoocModuleTable.MEMBER:
            return self.membersTables[moduleName]
        if Stype == KoocModuleTable.VIRTUAL:
            return self.virtualsTables[moduleName]
        
        
    def getSymbolList(self, moduleName, unMangledName, Stype):
        if Stype == KoocModuleTable.NON_MEMBER:
            return self.nonMemberTables[moduleName][unMangledName]
        if Stype == KoocModuleTable.MEMBER:
            return self.membersTables[moduleName][unMangledName]
        if Stype == KoocModuleTable.VIRTUAL:
            return self.virtualsTables[moduleName][unMangledName]

            
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
                
