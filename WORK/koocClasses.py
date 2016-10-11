from pyrser.parsing.node import Node
from cnorm import nodes

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
        
class moduleImplementation(KoocDeclaration):
    def __init__(self, moduleName, compoundDeclaration):
        self.moduleName = moduleName
        self.compoundDeclaration = compoundDeclaration

class moduleImport(KoocStatement):
    def __init__(self, moduleName):
        self.moduleName = moduleName

    def translate(self):
        decl = nodes.Raw
        decl.value = "#include \"" + self.moduleName + ".h\"\n"
        return (decl)
