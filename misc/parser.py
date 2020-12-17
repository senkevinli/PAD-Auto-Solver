from os.path import abspath
filename = abspath('./misc/dump.txt')
with open(filename) as file:
    line = file.readline()
    
    parsed = ''
    while line:
        idx = line.find(':')
        number_str = line[idx + 2:]
        a, b, c = number_str.split(' ')
        params = f'{int(a, 16)} {int(b, 16)} {int(c, 16)}'
        parsed += 'sendevent /dev/input/event5 ' + params + ";"
        line = file.readline()
    print(parsed)

