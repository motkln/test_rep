import itertools

if __name__ == "__main__":
    input_list = [1, 2, 3, 4]
    # 1
    for i in itertools.combinations(input_list, 2):
        print(i)
    # 2
    input_word = 'Python'

    for i in itertools.permutations(input_word):
        print(i)
    # 3
    count = 0
    input_list1 = ['a', 'b']
    input_list2 = [1, 2, 3]
    input_list3 = ['x', 'y']
    for i in itertools.cycle(itertools.chain(input_list1, input_list2, input_list3)):
        if count > (len(input_list1) + len(input_list2) + len(input_list3)) * 6 - 1:
            break
        count += 1
        print(i)
    # 4
    fib_num = [0, 1]
    for i in itertools.count(fib_num[-2], fib_num[-1]):
        if len(fib_num) == 10:
            break
        fib_num.append(fib_num[-1] + fib_num[-2])
        print(fib_num)
    # 5
    colors = ['red','blue']
    cloths = ['shirt','shoes']
    for i in itertools.combinations(itertools.chain(colors,cloths),2):
        if (i[0] in colors and i[1] not in colors) or (i[0] in cloths and i[1] not in cloths):
            print(i)
