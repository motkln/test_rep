import json
import csv


def json_to_dict(file):
    with open(file, 'r', encoding="utf-8") as f:
        res_dict = json.load(f)
    return res_dict


def get_average_score(input_list):
    grade_sum = 0
    for each in input_list['grades'].items():
        grade_sum += each[1]
    return grade_sum / len(input_list['grades'])


def get_best_student(input_list):
    return max(input_list.items(), key=lambda x: x[1]['average_score'])


def get_worst_student(input_list):
    return min(input_list.items(), key=lambda x: x[1]['average_score'])


def descript_find(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result:
            result = result[0]
            print(
                f'Имя: {result[0]}\nВозраст: {result[1]["age"]}\nПредметы: {result[1]["subjects"]}\nОценки: {result[1]["grades"]}')
        else:
            print('Студент с таким именем не найден')
        return result

    return wrapper


@descript_find
def find_student(name, inp_dict):
    finded_student = list(filter(lambda x: x[0] == name, inp_dict.items()))
    if find_student:
        return finded_student
    else:
        return False


def make_new_list(dict):
    new_students = []
    for each in dict.items():
        each[1]['name'] = each[0]
        each[1].pop('average_score')
        new_students.append(each[1])
    return new_students


def make_csv_file(data):
    with open("students.csv", "w", encoding="utf-8",newline='') as csv_file:
        fields_names = ['name','age','subjects','grades']
        writer = csv.DictWriter(csv_file,fieldnames=fields_names)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    # 1
    students: dict = json_to_dict("student_list.json")
    for each in students.items():
        print(f'Средний балл для студента {each[0]}: {get_average_score(each[1])}')
        each[1]['average_score'] = get_average_score(each[1])
    # 2
    best_student = get_best_student(students)
    print(f'Наилучший студент: {best_student[0]} (Средний балл: {best_student[1]["average_score"]})')

    worst_student = get_worst_student(students)
    print(f'Худший студент: {worst_student[0]} (Средний балл: {worst_student[1]["average_score"]})')
    # 3
    find_student('Saha', students)
    find_student('John', students)
    # 4
    sorted_list = sorted(students.items(), key=lambda x: x[1]["average_score"], reverse=True)
    for each in sorted_list:
        print(f'{each[0]}: {each[1]["average_score"]}')
    # 5
    new_list = make_new_list(students)
    print(new_list)
    # 6
    make_csv_file(new_list)