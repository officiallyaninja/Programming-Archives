storage = {'root': {'govind': {'_file_': [('img.txt', 'assdsadsad')], 'alias': {'_file_': [('none.txt', 'assdsadsad'), ('water.png', 'assdsadsad')], 'something': {
    '_file_': [('boobie_pics', 'urmum.txt')]}}}, 'legend': {'_file_': [('pswrd.txt', '192.111.232')]}}}


showpath = input(">show ")


def nodenav(nodepath):
    pointer = storage
    path_split = nodepath.split("/")
    currdir = list(path_split)

    for x in path_split:
        tempvar = pointer[x]
        del pointer
        pointer = tempvar

    def render(pointer):
        listkey = list(pointer.keys())

        if "_file_" in listkey:
            for z in pointer["_file_"]:
                print((" "*3*(len(currdir)-1) + '---') + f"{z}")
            print()
            listkey.remove("_file_")

        l = len(listkey)
        # print(currdir, ':', l)
        i = 0
        while i < l:
            k = listkey[i]
            try:

                tempvar = pointer[k]
                print(("   "*(len(currdir)-1) + '---')+f"{k}")
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
