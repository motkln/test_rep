# 1
input_list = ["apple", "kiwi", "banana", "fig"]
modify_list = list(filter(lambda x: len(x) > 4, input_list))
print(modify_list)
# 2
dict_list = [{"name": "John", "grade": 90}, {"name": "Jane", "grade": 85}, {"name": "Dave", "grade": 92}]
best_student = max(dict_list, key=lambda x: x['grade'])
print(best_student)
# 3
tuple_list = [(1, 5), (3, 2), (2, 8), (4, 3)]
sorted_list = sorted(tuple_list, key=lambda x: x[0] + x[1])
print(sorted_list)
# 4
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)


# 5
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person(name='{self.name}', grade={self.age})"

person1 = Person('Andrew', 20)
person2 = Person('Tom', 45)
person3 = Person('Kate', 12)
person4 = Person('Vernon', 22)
person5 = Person('Ustin', 29)
person_list = [person1, person2, person3, person4, person5]
sorted_person_list = sorted(person_list, key=lambda x: x.age)
print(sorted_person_list)

