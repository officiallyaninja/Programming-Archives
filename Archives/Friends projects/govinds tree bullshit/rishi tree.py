class Node():
    def __init__(self, name):
        self.name = name
        self.content = []
        self.parent = None
        self.type = None


class Folder(Node):
    def __init__(self, name):
        super().__init__(name)
        self.type = "BRANCH"
        self.sub = None

    def create_branch(self):
        self.sub = (0, self.name)
        self.content.append(self.sub)


f1 = Folder('Govind')
f1.create_branch()
print(f1.content)
