import ast
import sys

a = input()

arr = a.split(' ')

if len(arr) != 5:
    sys.exit('Некорректное выражение')

with open(r'index.json', 'r',
          encoding='utf-8') as file:
    index = ast.literal_eval(file.read())

all_values = set(range(1, 101))
all_values = set([str(i) for i in all_values])

new_arr = []

for i in range(len(arr)):
    if i % 2 == 0:
        if arr[i].startswith('!'):
            if index.get(arr[i][1:]) == None:
                sys.exit('Нет слов')

            new_arr.append(all_values - set(index.get(arr[i][1:])))
            arr[i] = arr[i][1:]
        else:
            if index.get(arr[i]) == None:
                sys.exit('Нет слов')
            new_arr.append(index.get(arr[i]))

if arr[1] == '|' or arr[1] == 'ИЛИ':
    if arr[3] == '|' or arr[3] == 'ИЛИ':
        result = set(new_arr[0]) | set(new_arr[1]) | set(new_arr[2])
    elif arr[3] == '&' or arr[3] == 'И':
        result = set(new_arr[0]) | set(new_arr[1]) & set(new_arr[2])
elif arr[1] == '&' or arr[1] == 'И':
    if arr[3] == '|' or arr[3] == 'ИЛИ':
        result = set(new_arr[0]) & set(new_arr[1]) | set(new_arr[2])
    elif arr[3] == '&' or arr[3] == 'И':
        result = set(new_arr[0]) & set(new_arr[1]) & set(new_arr[2])

if len(result) == 0:
    print("Не найдено")
else:
    with open(r'3rd_Task/result.txt', 'a',
        encoding='utf-8') as file:
        file.write(a + '\n')
        result = set([int(i) for i in result])
        sortedResult = sorted(result)
        for i, el in enumerate(sortedResult):
            if i == 0:
                file.write('[')
            if i == len(sortedResult) - 1:
                file.write(str(el) + ']' + '\n')
                continue
            file.write(str(el) + ', ')
        print(sortedResult)

# телефон & фонарь | звезда
# телефон | фонарь | звезда
# телефон & !фонарь | !звезда
# телефон | !фонарь | !звезда
# телефон И фонарь ИЛИ звезда
# телефон ИЛИ фонарь ИЛИ звезда
# телефон И !фонарь ИЛИ !звезда
# телефон ИЛИ !фонарь ИЛИ !звезда