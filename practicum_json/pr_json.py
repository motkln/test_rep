import json
import csv


def read_json(file):
    with open(file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def create_discription(data: list, subj: str):
    senior_student = None
    python_student = 0
    for each in data:
        if subj in each['предметы']:
            python_student += 1
        if senior_student is None or each['возраст'] > senior_student['возраст']:
            senior_student = each
    return f'Количество студентов в файле: {len(data)}\nСтарший студент: {senior_student}\nИзучающих {subj}: {python_student}'


def read_csv(file):
    with open(file, 'r', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',', lineterminator='\n')
        data = [x for x in reader]
        return data


def sales_period(data):
    periods = {}
    for i in range(len(data)):
        # Создается словарь: ключ - цифра месяца, значение - сумма
        periods[data[i]['Дата'].split('-')[1]] = periods.get(data[i]['Дата'].split('-')[1], 0) + int(
            data[i]['Сумма'])
    print(periods)
    sum_all_period = 0
    count_product = {}
    for each in data:
        sum_all_period += int(each['Сумма'])
        count_product[each['Продукт']] = count_product.get(each['Продукт'], 0) + 1
    max_product = max(count_product, key=lambda x: x[1])
    return sum_all_period, max_product, periods


def print_res_csv_data(*args):
    total_summary, best_product, month_summary = args
    print(
        f'Общая сумма продаж: {total_summary}\n'
        f'Продукт месяца: {best_product}\n'
        f'Количество проданных продуков по месяцам: {month_summary}')


def merge_json_csv_analys(json_data, csv_data):
    for i in json_data:
        for j in csv_data:
            if i['id'] == int(j['employee_id']):
                i['продуктивность'] = int(j['performance'])
    performances = [x['продуктивность'] for x in json_data]
    avg_performance = sum(performances) / len(performances)
    max_emp = json_data[performances.index(max(performances))]
    return (f"Средняя производительность всех сотрудников: {avg_performance}\n"
            f"Самый продуктивный работник:{max_emp['имя'],max_emp['продуктивность']}")


if __name__ == '__main__':
    # 1
    subject_search = 'Python'
    students_list = read_json('students.json')
    print(create_discription(students_list, subject_search))
    print('---')
    # 2
    data = read_csv('sales.csv')
    res_data = sales_period(data)
    print_res_csv_data(*res_data)
    print('---')
    # 3
    emp_data = read_json('employees.json')
    perf_data = read_csv('performance.csv')
    print(merge_json_csv_analys(emp_data, perf_data))
