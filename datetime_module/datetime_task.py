import datetime
from re import split

weekday_dir = {
    0: 'Понедельник',
    1: 'Вторник',
    2: 'Среда',
    3: 'Четверг',
    4: 'Пятница',
    5: 'Суббота',
    6: 'Воскресенье'
}


def check_year(year):
    if year % 4 == 0:
        return "Год является високосным"
    else:
        return "Год не является високосным"


def count_diff():
    input_str = input("Для расчета разницы в датах введите дату в  формете yyyy-mm-dd\n").split('-')
    arr_data = [int(x) for x in input_str]
    date = datetime.datetime(*arr_data)
    difference = date - datetime.datetime.now()
    days = difference.days
    hours, ost_sec = divmod(difference.seconds, 3600)
    minutes, seconds = divmod(ost_sec, 60)
    return f"Разница в датах: {days} дней {hours} минут {minutes} секунд"


if __name__ == "__main__":
    current_date = datetime.datetime.now()
    print(weekday_dir.get(datetime.datetime.weekday(current_date)))
    check_year(current_date.year)
    print(count_diff())