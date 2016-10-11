from pyrser.parsing.node import Node

class KoocNode(Node):
    pass

class KoocDeclaration(KoocNode):
    pass

class KoocStatement(KoocNode):
    pass

class moduleDeclaration(KoocDeclaration):
    def __init__(self, moduleName, compoundDeclaration):
        self.moduleName = moduleName
        self.compoundDeclaration = compoundDeclaration
        
class moduleImplementation(KoocStatement):
    def __init__(self, moduleName, compoundDeclaration):
        self.moduleName = moduleName
        self.compoundDeclaration = compoundDeclaration

class moduleImport(KoocDeclaration):
    def __init__(self, moduleName):
        self.moduleName = moduleName
