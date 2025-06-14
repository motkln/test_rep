import telebot
from telebot import types
import os
import datetime
import json
from copy import deepcopy
bots_token = os.getenv('TOKENBOT')
bot = telebot.TeleBot(bots_token)


class Data_store:
    def __init__(self):
        self.data_base_records = []

    def get_list(self):
        return self.data_base_records

    def append(self, element):
        self.data_base_records.append(element)
        self.save_data()

    def save_data(self):
        # with open('data_base_users', 'w', encoding="utf-8") as f:
        #     json.dump(data_base_users, f, indent=4)
        with open(os.getcwd()+'\\telegram_bot\\data_base_records.json', 'w', encoding="utf-8") as f1:
            data = deepcopy(data_base_records.get_list())
            for each in data:
                each['start_sleep_time'] = each['start_sleep_time'].strftime('%d %B %Y, %H:%M:%S')
                each['wake_time'] = each['wake_time'].strftime('%d %B %Y, %H:%M:%S')
            json.dump(data, f1, indent=4)

    def load_data(self):
        if (os.path.exists(os.getcwd()+'\\telegram_bot\\data_base_records.json')
                and os.path.getsize(os.getcwd()+'\\telegram_bot\\data_base_records.json') > 0):
            with open(os.getcwd()+'\\telegram_bot\\data_base_records.json', 'r', encoding="utf-8") as f1:
                # self.data_base_records = json.load(f1)
                data = json.load(f1)
                for each in data:
                    each['start_sleep_time'] = datetime.datetime.strptime(each['start_sleep_time'], '%d %B %Y, %H:%M:%S')
                    each['wake_time'] = datetime.datetime.strptime(each['wake_time'], '%d %B %Y, %H:%M:%S')
                self.data_base_records = data

        else:
            print("Файл пуст или не существует.")
            self.data_base_records = []  # Или инициализируйте пустой список
        #
        # with open(os.getcwd()+'\\telegram_bot\\data_base_records.json', 'r', encoding="utf-8") as f1:
        #     self.data_base_records = json.load(f1)



data_base_users = {}

data_base_records = Data_store()


def check_forget(message, id):
    if data_base_users.get(id).get('start_sleep_time') - data_base_users.get(id).get('wake_time') > datetime.timedelta(
            hours=16):
        bot.send_message(message.chat.id,
                         "Похоже вы забыли записать ваш подъем в прошлый раз! Прошлый день не будет учитываться")
        return 0


def add_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_ans1 = types.KeyboardButton('/sleep')
    button_ans2 = types.KeyboardButton('/wake')
    button_ans3 = types.KeyboardButton('/quality')
    button_ans4 = types.KeyboardButton('/notes')
    button_ans5 = types.KeyboardButton('/edit_note')
    button_ans6 = types.KeyboardButton('/edit_quality')
    button_ans7 = types.KeyboardButton('/show')
    markup.add(button_ans1, button_ans2, button_ans3, button_ans4, button_ans5, button_ans6, button_ans7)
    return markup


def count_sleeping_time(id):
    sleeping_time = data_base_users.get(id).get('wake_time') - data_base_users.get(id).get('start_sleep_time')
    time_date = str(sleeping_time).split(':')
    output_string = time_date[0] + " часов " + time_date[1] + " минут " + time_date[2][:2] + " секунд "
    return output_string


def add_record_db(id, sleep_time=None, wake_time=None, quality_value=None, input_note=None):
    input_info = {'start_sleep_time': sleep_time, 'wake_time': wake_time, 'quality': quality_value,
                  'notes': input_note}
    data_base_users[id] = input_info


@bot.message_handler()
def give_answ(message):
    if message.text == "/start":
        bot.send_message(message.chat.id,
                         'Привет! Я умею отслеживать параметры твоего сна. \nМои команды:'
                         '\n/sleep -   Чтобы начать отслеживать сон'
                         '\n/wake -    Чтобы уведомить о подъеме'
                         '\n/quality - Для оценки качества сна'
                         '\n/notes -   Чтобы добавить заметку'
                         '\n/edit_note -   Чтобы редактировать заметку'
                         '\n/edit_quality -   Чтобы редактировать заметку'
                         '\n/show -   Чтобы показать заметки',
                         reply_markup=add_keyboard())
        add_record_db(message.from_user.id)
        data_base_records.load_data()
    try:
        if message.text == '/sleep':
            now = datetime.datetime.now()
            if (data_base_users.get(message.from_user.id)['start_sleep_time'] is None) or (
                    now - data_base_users.get(message.from_user.id)['start_sleep_time'] < datetime.timedelta(minutes=5)):
                data_base_users.get(message.from_user.id)['start_sleep_time'] = now
                data_base_users.get(message.from_user.id)['wake_time'] = None
                data_base_users.get(message.from_user.id)['notes'] = 'C ' + str(
                    datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                bot.send_message(message.chat.id,
                                 "Спокойной ночи!\n\nНе забудьте написать команду /wake, когда проснетесь.")
            elif (now - data_base_users.get(message.from_user.id)['start_sleep_time'] > datetime.timedelta(hours=12)):
                bot.send_message(message.chat.id,
                                 "Похоже вы забыли засчитать ваш подъем вчера!\nСпокойной ночи!\n\nНе забудьте написать команду /wake, когда проснетесь.")
                data_base_users.get(message.from_user.id)['start_sleep_time'] = now
                data_base_users.get(message.from_user.id)['wake_time'] = None
                data_base_users.get(message.from_user.id)['notes'] = 'C ' + str(
                    datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    except:
        bot.send_message(message.chat.id,"Необходимо перезапустить бота! Пожалуйста, введите команду /start...")

    if message.text == '/wake':
        now = datetime.datetime.now()
        if data_base_users.get(message.from_user.id)['wake_time'] == None:
            if data_base_users.get(message.from_user.id)['start_sleep_time'] != None:
                data_base_users.get(message.from_user.id)['wake_time'] = now
                data_base_users.get(message.from_user.id)['notes'] += ' По ' + str(
                    datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "\n")
                bot.send_message(message.chat.id,
                                 f'Доброе утро!\nВы спали: {count_sleeping_time(message.from_user.id)}')
                data_base_users.get(message.from_user.id)['quality'] = str('-')
                copy_data = data_base_users.get(message.chat.id).copy()
                copy_data['id'] = message.chat.id
                data_base_records.append(copy_data)
            else:
                bot.send_message(message.chat.id, 'Записей пока нет.')
        else:
            bot.send_message(message.chat.id, 'Похоже, что подъем уже был засчитан!')

    if message.text == '/notes':
        show_notes(message, 0)

    if message.text == '/edit_note':
        show_notes(message, 1)

    if message.text == '/show':
        show_all(message)

    if message.text == '/quality':
        show_notes(message, 2)

    if message.text == '/edit_quality':
        show_notes(message, 3)


def give_quality(message, number_of_note, founded_elements):
    try:
        quality = message.text
        check_qual = int(quality) + 1
        for record in data_base_records.get_list():
            if record == founded_elements[number_of_note]:
                record['quality'] = quality
                bot.send_message(message.chat.id, "Заметка добавлена!", reply_markup=add_keyboard())
        data_base_records.save_data()

    except ValueError:
        bot.send_message(message.chat.id,
                         "Похоже ты ввел число не в нужном формате\nВведи только номер заметки: 1, 2 и т.д.")
        bot.register_next_step_handler(message, give_quality, number_of_note)


def get_number_notes(message, mode, founded_element):
    try:
        number_of_note = int(message.text) - 1
        if mode == 0:
            bot.send_message(message.chat.id, "Теперь напиши заметку к этому периду сна...")
            bot.register_next_step_handler(message, add_note, number_of_note, founded_element)
        elif mode == 1:
            bot.send_message(message.chat.id, "Теперь напиши заметку к этому периду сна...")
            bot.register_next_step_handler(message, edit_note, number_of_note, founded_element)
        elif mode == 2:
            bot.send_message(message.chat.id, "Теперь поставь оценку к этому периду сна (0-10)")
            bot.register_next_step_handler(message, give_quality, number_of_note, founded_element)
        elif mode == 3:
            bot.send_message(message.chat.id, "Теперь поставь оценку к этому периду сна (0-10)")
            bot.register_next_step_handler(message, give_quality, number_of_note, founded_element)

    except ValueError:
        bot.send_message(message.chat.id,
                         "Похоже ты ввел число не в нужном формате\nВведи только номер заметки: 1, 2 и т.д.")
        bot.register_next_step_handler(message, get_number_notes, mode, founded_element)


def add_note(message, number_of_note, founded_elements):
    note = message.text
    add_str = 'Заметка: ' + note
    if number_of_note <= len(data_base_records.get_list()):
        for record in data_base_records.get_list():
            if record == founded_elements[number_of_note]:
                print(record)
                record['notes'] += add_str
                bot.send_message(message.chat.id, "Заметка успешно добавлена!", reply_markup=add_keyboard())
        data_base_records.save_data()
    else:
        bot.send_message(message.chat.id,"Похоже ты ввел не верный номер заметки, попробуй еще раз")

def edit_note(message, number_of_note, founded_elements):
    note = message.text
    if number_of_note <= len(data_base_records.get_list()):
        for record in data_base_records.get_list():
            if record == founded_elements[number_of_note]:
                selected_record = data_base_records.get_list()
                record['notes'] = selected_record[number_of_note]['notes'][
                                  :selected_record[number_of_note]['notes'].rfind(
                                      "Заметка:")] + "\nЗаметка: " + note

                bot.send_message(message.chat.id, "Заметка успешно изменена!", reply_markup=add_keyboard())
        data_base_records.save_data()
    else:
        bot.send_message(message.chat.id, "Похоже ты ввел не верный номер заметки, попробуй еще раз")

def show_all(message):
    count = 0
    for times in data_base_records.get_list():
        if message.chat.id == times.get('id'):
            bot.send_message(message.chat.id,
                             str(count + 1) + ') ' + times.get('notes') + '\nКачество сна: ' + times.get('quality'))
            count += 1
        else:
            continue
    if count == 0:
        bot.send_message(message.chat.id, 'Записей пока нет.')


def show_notes(message, mode):
    founded_elements = []
    count = 0
    if mode == 1:
        bot.send_message(message.chat.id,
                         "Поменяй заметку ко сну!\nВыбери к какой записи ты хочешь добавить заметку и введи ее номер:")
    elif mode == 0:
        bot.send_message(message.chat.id,
                         "Добавь заметку ко сну!\nВыбери к какой записи ты хочешь добавить заметку и введи ее номер:")
    elif mode == 2:
        bot.send_message(message.chat.id,
                         "Добавь оценку качества сна!\nВыбери к какой записи ты хочешь добавить заметку и введи ее номер:")
    elif mode == 3:
        bot.send_message(message.chat.id,
                         "Измени оценку качества сна\nВыбери к какой записи ты хочешь добавить заметку и введи ее номер:")

    for times in data_base_records.get_list():
        if message.chat.id == times.get('id'):
            bot.send_message(message.chat.id,
                             str(count + 1) + ') ' + times.get('notes') + '\nКачество сна: ' + times.get('quality'))
            count += 1
            founded_elements.append(times)
    bot.register_next_step_handler(message, get_number_notes, mode, founded_elements)

data_base_records.load_data()
bot.polling(none_stop=True, interval=0)
