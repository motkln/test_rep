# 1
students_dict = {
    'Саша': 27,
    'Кирилл': 52,
    'Маша': 14,
    'Петя': 36,
    'Оля': 43,
}

sorted_students = sorted(students_dict.items(), key=lambda x: x[1])
print(sorted_students)
# 2
data = [
    (82, 191),
    (68, 174),
    (90, 189),
    (73, 179),
    (76, 184)
]

sorted_data = sorted(data, key=lambda x: x[0] / (x[1] * x[1] / 10000))
print(sorted_data)
# 3
students_list = [
    {
        "name": "Саша",
        "age": 27,
    },
    {
        "name": "Кирилл",
        "age": 52,
    },
    {
        "name": "Маша",
        "age": 14,
    },
    {
        "name": "Петя",
        "age": 36,
    },
    {
        "name": "Оля",
        "age": 43,
    },
]
sorted_students = sorted(students_list, key=lambda x: x['age'])
print(sorted_students)
