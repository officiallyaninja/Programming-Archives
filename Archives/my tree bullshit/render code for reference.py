class Node():
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.type = 'NODE'


class Branch(Node):
    def __init__(self, name):
        super().__init__(name)
        self.children = {}
        self.type = 'BRANCH'

    def create_branch(self, branch_name):
        new_branch = Branch(branch_name)
        new_branch.parent = self
        self.children[new_branch.name] = new_branch

    def create_leaf(self, leaf_name, link):
        new_leaf = Leaf(leaf_name, link)
        new_leaf.parent = self
        self.children[new_leaf.name] = new_leaf

    def render(self, depth=0):
        if self.parent is None:
            print(' '*3*depth + '---' + f'{self.name}')
        else:
            print(('   |')*depth + '---' + f'{self.name}')
        print('   |'*(depth+1))

        for node in self.children.values():
            if node.type == "LEAF":
                print('   |'*(depth+1) + '---' + f'{node.name}: {node.link}')

        for node in self.children.values():
            if node.type == 'BRANCH':
                node.render(depth+1)


class Leaf(Node):
    def __init__(self, name, link):
        super().__init__(name)
        self.link = link
        self.type = 'LEAF'


# ROOT should be the only branch created explicitly like this
# all others should be created through method calls
root = Branch('root')

root.create_branch('govind')

root.children['govind'].create_branch('alias')
root.children['govind'].children['alias'].create_leaf('name1', 'link1')

root.children['govind'].create_leaf('name2', 'link2')
root.children['govind'].create_leaf('name3', 'link3')

root.create_branch('legend')
root.children['legend'].create_leaf('name4', 'link4')
root.render()
