def gen():
    print('poo')
    yield 'first'
    print('hello world')
    yield 'second'


test = gen()
count = 0
for i in test:
    input()
    print(count)
    print(i)
    count+= 1