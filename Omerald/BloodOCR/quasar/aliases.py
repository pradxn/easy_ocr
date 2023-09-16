aliases = {
    'type-1': ['1', '2', '3'], 
    'type-2': ['a', 'b', 'c'],
    'type-3': ['A', 'B', 'C'],
    }
print('\n')
name = input('Enter an alias: ')
print('\n')
for key, value in aliases.items():
    if name == key:
        print('Given input is an alias of: ' + value)
        print('\n')
        break
    elif name in value:
        print('Given input is an alias of: ' + key)
        print('\n')
        break
else:
    print('Alias not found, add to the list?')
