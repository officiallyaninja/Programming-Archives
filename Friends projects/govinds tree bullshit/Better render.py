storage = {'root': {'govind': {'_file_': [('img.txt', 'assdsadsad')], 'alias': {'_file_': [('none.txt', 'assdsadsad'), ('water.png', 'assdsadsad')], 'something': {'_file_': [('boobie_pics', 'urmum.txt')]}}, 'new_folder': {
    '_file_': [('wheee', 'whoo')]}}, 'legend': {'_file_': [('pswrd.txt', '192.111.232')], 'arjun': {'_file_': [('file1', 'name1')], 'deeeeeper': {'doopie': {'_file_': [('file2', 'name2')]}}}}}}


showpath = input(">show ")


def nodenav(nodepath):
    pointer = storage
    node_list = nodepath.split("/")
    currdir = list(node_list)

    for node in node_list:
        tempvar = pointer[node]
        del pointer
        pointer = tempvar

    def render(pointer):
        key_list = list(pointer.keys())

        if "_file_" in key_list:
            for z in pointer["_file_"]:
                print(("-"*3*len(currdir)) + f"{z}")
            print()
            key_list.remove("_file_")
        # print(currdir, ':', l)
        i = 0
        while i < len(key_list):
            k = key_list[i]
            try:
                tempvar = pointer[k]
                print(("---"*len(currdir))+f"{k}")
                print(((" "*3) * len(currdir)) + "|")
                del pointer
                pointer = tempvar
                currdir.append(k)
                render(pointer)
                i += 1
            except KeyError:
                currdir.pop()
                pointer = storage
                for x in currdir:
                    tempvar = pointer[x]
                    del pointer
                    pointer = tempvar

    render(pointer)


nodenav(showpath)
