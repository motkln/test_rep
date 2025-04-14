import json
import csv
from textwrap import indent

person = {
    "Имя": "Матвей",
    "Возраст": "25",
    "Город": "Москва",
    "Знания": ["Python", "SQL", "Django"]
}


def read_csv(file, delimiter=',', lineterminator='\n'):
    with open(file, 'r', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=delimiter, lineterminator=lineterminator)
        data = list(reader)
    return data


def add_to_json(file, add_data):
    print(add_data)
    with open(file, 'w', encoding='utf-8') as json_file:
        json.dump(add_data, json_file, ensure_ascii=False, indent=4)
    return


if __name__ == '__main__':
    data_list = read_csv('data.csv')
    add_to_json('data.json', data_list)
