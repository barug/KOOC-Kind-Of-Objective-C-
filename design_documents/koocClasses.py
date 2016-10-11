from pyrser.parsing.node import Node

class KoocNode(Node):
    pass

class KoocDeclaration(KoocNode):
    pass

class moduleDeclaration(KoocDeclaration):
    def __init__(self, compoundDeclaration, moduleName):
        self.moduleName = moduleName
        self.compoundDeclaration = compoundDeclaration
        
class moduleImplementation(KoocDeclaration):
    def __init__(self, compoundDeclaration, moduleName):
        self.moduleName = moduleName
        self.compoundDeclaration = compoundDeclaration