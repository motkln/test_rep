import json
import csv

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


def add_to_json_str(add_data):
    json_str = json.dumps(add_data, ensure_ascii=False, indent=4)
    return json_str


if __name__ == '__main__':
    data_list = read_csv('data.csv')
    print(add_to_json_str(data_list))
