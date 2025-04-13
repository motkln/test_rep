import csv


def read_file(file):
    with open(file, encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        print(list(reader))


def add_to_file():
    data = [
        ['Имя', 'Возраст', 'Город'], ['Анна', '25', 'Москва'], ['Петр', '30', 'Десногорск'],
        ['Мария', '28', 'Барнаул']]
    with open('data.csv', 'a', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


def csv_dict(data):
    with open('data.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
        fieldnames = ['Имя', 'Возраст', 'Город']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return


def csv_read():
    with open('data.csv', 'r', encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['Имя'], row['Возраст'], row['Город'])
        print('Прочитано строк: ', reader.line_num)


def txt_to_csv(file, headers):
    data_list = []
    with open(file, 'r', encoding='utf-8') as data:
        for row in data:
            data_list.append(row.split())

    with open(f'{file[:-4]}.csv', 'w', encoding='utf-8', newline='') as data_csv:
        writer = csv.writer(data_csv)
        writer.writerow(headers)
        writer.writerows(data_list)


def total_cost(file) -> str:
    with open(file, 'r', encoding='utf-8', newline='') as data_csv:
        reader = csv.DictReader(data_csv)
        total_sum = 0
        for row in reader:
            total_sum += int(row['Цена за штуку'])
    return f'Итоговая стоимость заказа: {total_sum}'


if __name__ == '__main__':
    # data = [
    #     {'Имя': 'Анна', 'Возраст': '25', 'Город': 'Москва'},
    #     {'Имя': 'Петр', 'Возраст': '30', 'Город': 'Санкт-Петербург'},
    #     {'Имя': 'Мария', 'Возраст': '28', 'Город': 'Киев'}]
    # read_file('data.csv')
    # add_to_file()
    # read_file('data.csv')
    # csv_dict(data)
    # csv_read()

    data_headeres = ['Наименование товара', 'Количество товара', 'Цена за штуку']
    txt_to_csv('prices.txt', data_headeres)
    read_file('prices.csv')
    print(total_cost('prices.csv'))
