import string


def count_uniq_words(file):
    words_dict = {}
    words_list = []
    with open(file, 'r') as data:
        for row in data:
            words_list.extend([x.strip(string.punctuation).lower() for x in row.split()])
    for i in words_list:
        words_dict[i] = words_dict.get(i, 0) + 1
    return words_dict


if __name__ == "__main__":
    file_name = 'input_text.txt'
    with open(file_name, 'w', encoding='windows-1251') as f:
        f.write("""Здравствуйте, уважаемый руководитель. Меня зовут Фамилия Имя.
Я хотел бы подать заявление на вакансию начальника отдела продаж в
вашей компании. Я являюсь опытным профессионалом в области продаж и коммерческой деятельности с десятилетним опытом работы в различных отраслях. С уважением, Фамилия Имя.""")
print(count_uniq_words(file_name))
