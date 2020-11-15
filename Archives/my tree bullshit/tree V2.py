from copy import deepcopy


class Node():

    def __init__(self, name: str):
        self.name = name
        self.children = {}  # in the format {child_name : child}
        self.files = []  # each file should be a tuple in the form (<name>,<link>)
        self.parent = None

    def create_child(self, name):
        child = Node(name)
        child.parent = self
        self.children[child.name] = child

    def append(self, tree):
        tree.parent = self
        self.children[tree.name] = tree

    def delete(self):
        parent = self.parent
        parent.children.pop(self.name)
        del self

    def pop(self, child_name):
        return self.children.pop('child_name')

    def add_file(self, name, link):
        self.files.append((name, link))

    def render(self, depth=0):
        print(' '*3*depth + '--- ' + f'{self.name}')
        print(' '*3*(depth+1) + '|')

        for file in self.files:
            # file[0] is the name and file [1] is the link
            print(' '*3*(depth+1) + '--- ' + f'{file[0]}: {file[1]}')

        for node in self.children.values():
            node.render(depth+1)

    def copy(self):
        return deepcopy(self)

    def dict(self):
        dict = {}
        dict['_files_'] = self.files
        for child in self.children.values():
            dict[child.name] = child.dict()

        return dict

# ------------------------------------------------------------------------------


def tree(dict, root_name):
    root = Node(root_name)
    root.files = dict.pop('_files_')
    for child_name in dict:
        child = tree(dict[child_name], child_name)
        root.append(child)
    return root


root = Node('Root')

root.create_child('govind')

root.children['govind'].create_child('alias')
root.children['govind'].children['alias'].add_file('name1', 'link1')

root.children['govind'].add_file('name2', 'link2')
root.children['govind'].add_file('name3', 'link3')

root.create_child('legend')
root.children['legend'].add_file('name4', 'link4')

D = root.dict()
rt = tree(D, 'rt')
root.children['legend'].append(rt)
root.render()
