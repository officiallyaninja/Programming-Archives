storage = {'root': {'govind': {'_file_': [('img.txt', 'assdsadsad')], 'alias': {'_file_': [('none.txt', 'assdsadsad'), ('water.png', 'assdsadsad')], 'something': {
    '_file_': [('boobie_pics', 'urmum.txt')]}}}, 'legend': {'_file_': [('pswrd.txt', '192.111.232')]}}}

while True:
    userinput = input(">add ")
    listlist = userinput.split()
    pathinput = listlist[0]
    link = listlist[1]
    name = listlist[2]

    pathlist = pathinput.split("/")

    # add operation

    pointer = storage

    for path in pathlist:
        if path in pointer.keys():
            tempvar = pointer
            del pointer
            pointer = tempvar[path]
        else:
            pointer[path] = {}
            tempvar = pointer
            del pointer
            pointer = tempvar[path]

    if "_file_" in pointer.keys():
        pointer["_file_"].append((name, link))
    else:
        pointer["_file_"] = []
        pointer["_file_"].append((name, link))

    print(storage)

# render operation
