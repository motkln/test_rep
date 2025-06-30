import telebot
from telebot import types
import os
import datetime
import json
from copy import deepcopy
import sqlite3
from sqlite3 import connect

bots_token = os.getenv('TOKENBOT')
bot = telebot.TeleBot(bots_token)


class Data_Access_Object:
    def __init__(self):
        self.conn = self.get_connection()
        if self.conn:
            self.cursor = self.conn.cursor()
            self.make_bot_db()

    def get_connection(self):
        try:
            return connect(os.getcwd() + '\\telegram_bot\\tg_bot_database.db', check_same_thread=False)
        except Exception as e:
            print(e)
            return 0

    def show_all(self, user_id):
        res = self.cursor.execute('''select user_id,start_sleep_time,wake_time,quality,notes 
                                    from bot_db where user_id = ?''', (user_id,)).fetchall()
        return res

    def make_bot_db(self):
        return self.cursor.execute('''Create table if not exists bot_db(
        id integer primary key AUTOINCREMENT not null,
        user_id integer not null,
        start_sleep_time DATA,
        wake_time DATA,
        quality Integer,
        notes TEXT)''')

    # def update_record(self, user_id=None, start_sleep=None, wake_time=None, quality=None, notes=None):
    #     if user_id is not None:
    #         self.cursor.execute('''Update bot_db set user_id = ?;''', (user_id,))
    #     if start_sleep is not None:
    #         self.cursor.execute('''Update bot_db set start_sleep_time = ? where user_id = ?;''', (start_sleep, user_id))
    #     if wake_time is not None:
    #         self.cursor.execute('''Update bot_db set wake_time = ? where user_id = ?;''', (wake_time, user_id))
    #     if quality is not None:
    #         self.cursor.execute('''Update bot_db set quality = ? where user_id = ?;''', (quality, user_id))
    #     if notes is not None:
    #         self.cursor.execute('''Update bot_db set notes = ? where user_id = ?;''', (notes, user_id))

    # self.conn.commit()

    def edit_note(self, notes=None, id=None, mode=None):
        if mode == 0:
            self.cursor.execute('''Update bot_db set notes = notes || ? where id = ?;''', (notes, id))
        elif mode == 1:
            self.cursor.execute('''Update bot_db set notes = ? where id = ?;''', (notes, id))
        self.conn.commit()

    def add_record(self, user_id=None, start_sleep=None, wake_time=None, quality=None, notes=None):
        self.cursor.execute(
            '''insert into bot_db (user_id,start_sleep_time,wake_time,quality,notes) values (?,?,?,?,?)''',
            (user_id, start_sleep, wake_time, quality, notes))
        self.conn.commit()
        return 0

    def find_record(self, user_id=None, start_sleep=None, wake_time=None, quality=None, notes=None):
        return self.cursor.execute(
            '''select id from bot_db where user_id = ? 
                                            and start_sleep_time = ? 
                                            and wake_time = ? 
                                            and quality = ? 
                                            and notes = ?;''',
            (user_id, start_sleep, wake_time, quality, notes)).fetchone()[0]

    def find_note(self, id=None):
        return self.cursor.execute('''select notes from bot_db where id = ?;''', (id,)).fetchone()[0]

    def edit_quality(self, quality=None, id=None):
        self.cursor.execute('''Update bot_db set quality = ? where id = ?;''', (quality, id))
        self.conn.commit()


data_base_users = {}

data_base_records = Data_Access_Object()


# def check_forget(message, id):
#     if data_base_users.get(id).get('start_sleep_time') - data_base_users.get(id).get('wake_time') > datetime.timedelta(
#             hours=16):
#         bot.send_message(message.chat.id,
#                          "Похоже вы забыли записать ваш подъем в прошлый раз! Прошлый день не будет учитываться")
#         return 0


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
    # data_base_records.add_record(id, sleep_time, wake_time, quality_value, input_note)


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

    try:
        if message.text == '/sleep':

            now = datetime.datetime.now()
            if (data_base_users.get(message.from_user.id)['start_sleep_time'] is None) or (
                    now - data_base_users.get(message.from_user.id)['start_sleep_time'] < datetime.timedelta(
                minutes=5)):
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
        bot.send_message(message.chat.id, "Необходимо перезапустить бота! Пожалуйста, введите команду /start...")

    if message.text == '/wake':
        now = datetime.datetime.now()
        if data_base_users.get(message.from_user.id)['wake_time'] == None:
            if data_base_users.get(message.from_user.id)['start_sleep_time'] != None:
                data_base_users.get(message.from_user.id)['wake_time'] = now

                # data_base_records.update_record(message.from_user.id,
                #                                 wake_time=data_base_users.get(message.from_user.id)['wake_time'])
                data_base_users.get(message.from_user.id)['notes'] += ' По ' + str(
                    datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "\n")
                # data_base_records.update_record(message.from_user.id,
                #                                 notes=data_base_users.get(message.from_user.id)['notes'])
                bot.send_message(message.chat.id,
                                 f'Доброе утро!\nВы спали: {count_sleeping_time(message.from_user.id)}')
                data_base_users.get(message.from_user.id)['quality'] = str('-')
                # data_base_records.update_record(message.from_user.id,
                #                                 quality=data_base_users.get(message.from_user.id)['quality'])
                copy_data = data_base_users.get(message.chat.id).copy()
                copy_data['id'] = message.chat.id
                data_base_records.add_record(message.from_user.id,
                                             start_sleep=data_base_users.get(message.from_user.id)['start_sleep_time'],
                                             wake_time=data_base_users.get(message.from_user.id)['wake_time'],
                                             notes=data_base_users.get(message.from_user.id)['notes'],
                                             quality=data_base_users.get(message.from_user.id)['quality'])
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
        for record in data_base_records.show_all(message.chat.id):
            if record == founded_elements[number_of_note]:
                id = data_base_records.find_record(*record)
                data_base_records.edit_quality(quality=quality, id=id)
                bot.send_message(message.chat.id, "Качество сна добавлено!", reply_markup=add_keyboard())
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
    if number_of_note <= len(data_base_records.show_all(message.chat.id)):
        for record in data_base_records.show_all(message.chat.id):
            if record == founded_elements[number_of_note]:
                print(record)
                id_record = data_base_records.find_record(*record)
                data_base_records.edit_note(id=id_record, notes=add_str, mode=0)
                bot.send_message(message.chat.id, "Заметка успешно добавлена!", reply_markup=add_keyboard())
    else:
        bot.send_message(message.chat.id, "Похоже ты ввел не верный номер заметки, попробуй еще раз")


def edit_note(message, number_of_note, founded_elements):
    note = message.text
    if number_of_note <= len(data_base_records.show_all(message.chat.id)):
        for record in data_base_records.show_all(message.chat.id):
            if record == founded_elements[number_of_note]:
                id_record = data_base_records.find_record(*record)
                exist_note = data_base_records.find_note(id_record)
                new_note = exist_note[:exist_note.rfind("Заметка:")] + "Заметка: " + note
                data_base_records.edit_note(notes=new_note, id=id_record, mode=1)
                bot.send_message(message.chat.id, "Заметка успешно изменена!", reply_markup=add_keyboard())
    else:
        bot.send_message(message.chat.id, "Похоже ты ввел не верный номер заметки, попробуй еще раз")


def show_all(message):
    count = 0
    for times in data_base_records.show_all(message.chat.id):
        user_id, sleep_time, wake_time, quality, notes = times
        bot.send_message(message.chat.id,
                         str(count + 1) + ') ' + notes + '\nКачество сна: ' + str(quality))
        count += 1
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

    for times in data_base_records.show_all(message.chat.id):
        user_id, sleep_time, wake_time, quality, notes = times
        bot.send_message(message.chat.id,
                         str(count + 1) + ') ' + notes + '\nКачество сна: ' + str(quality))
        count += 1
        founded_elements.append(times)
    bot.register_next_step_handler(message, get_number_notes, mode, founded_elements)


# data_base_records.load_data()
bot.polling(none_stop=True, interval=0)
