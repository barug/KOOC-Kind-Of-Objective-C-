from pyrser.parsing.node import Node
from cnorm import nodes

class KoocNode(Node):
    def translate(self):
        pass
    pass

class KoocDeclaration(KoocNode):
    def translate(self):
        pass
    pass

class KoocStatement(KoocNode):
    def translate(self):
        pass
    pass

class moduleDeclaration(KoocDeclaration):
    def __init__(self, moduleName, compoundDeclaration):
        self.moduleName = moduleName
        self.compoundDeclaration = compoundDeclaration

    def translate(self):
        pass                    # code goes here

class moduleImplementation(KoocDeclaration):
    def __init__(self, moduleName, compoundDeclaration):
        self.moduleName = moduleName
        self.compoundDeclaration = compoundDeclaration

    def translate(self):
        pass                    # code goes here

class moduleImport(KoocStatement):
    def __init__(self, moduleName):
        self.moduleName = moduleName

    def translate(self):
        decl = nodes.Raw
        decl.value = "#include \"" + self.moduleName + ".h\"\n"
        return (decl)

class classDeclaration(KoocDeclaration):
    def __init__(self, className, compoundDeclaration):
        self.className = className
        self.compoundDeclaration = compoundDeclaration

    def translate(self):
        pass

class classMember(KoocDeclaration):
    def __init__(self, className, compoundDeclaration):
        self.className = className
        self.compoundDeclaration = compoundDeclaration

    def translate(self):
        pass
