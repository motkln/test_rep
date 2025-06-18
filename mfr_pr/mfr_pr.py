from functools import reduce


def cube(element):
    return element ** 3


def multiple_five(element):
    return element % 5 == 0


def is_odd(element):
    return element % 2 == 1


def multiply(a, b):
    return a * b


input_list = [1, 2, 3, 4, 5]
sq_list = list(map(cube, input_list))
print(sq_list)

print(list(filter(multiple_five, sq_list)))

odd_multiply = reduce(multiply, list(filter(is_odd, sq_list)))
print(odd_multiply)
