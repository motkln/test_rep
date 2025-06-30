import telebot
from telebot import types
import os
import datetime
import sqlite3
from sqlite3 import connect

bots_token = os.getenv('TOKENBOT')
bot = telebot.TeleBot(bots_token)


class Data_Access_Object:
    def __init__(self):
        self.conn = self.get_connection()
        if self.conn:
            self.cursor = self.conn.cursor()
            self.make_users_db()
            self.make_data_db()
            self.make_notes_db()

    def get_connection(self):
        try:
            return connect(os.getcwd() + '\\telegram_bot\\tg_bot_database.db', check_same_thread=False)
        except Exception as e:
            print(e)
            return 0

    def show_all(self, user_id):
        res = self.cursor.execute('''select sr.user_id,sr.start_sleep_time,sr.wake_time,sr.quality,n.note 
                                    from sleep_records sr 
                                    join users u on u.id = sr.user_id
                                    join notes n on n.sleep_record_id = sr.id   
                                    where sr.user_id = ?''', (user_id,)).fetchall()
        return res

    def make_data_db(self):
        try:
            self.cursor.execute('''Create table if not exists sleep_records(
        id integer primary key AUTOINCREMENT not null,
        user_id integer not null,
        start_sleep_time DATA,
        wake_time DATA,
        quality Integer,
        foreign key (user_id) references users (id));''')
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            return 0

    def make_users_db(self):
        try:
            self.cursor.execute('''Create table if not exists users(
        id integer primary key not null,
        name TEXT not null)''')
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            return 0

    def make_notes_db(self):
        try:
            self.cursor.execute('''Create table if not exists notes(
        id integer primary key AUTOINCREMENT not null,
        note Text,
        sleep_record_id integer not null,
        foreign key (sleep_record_id) references sleep_records (id));''')
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            return 0

    def add_note(self, id=None, notes=None):
        self.cursor.execute('''insert into notes (sleep_record_id,note);''', (id, notes))
        self.conn.commit()

    def edit_note(self, notes=None, id=None, start_sleep=None, mode=None):
        if mode == 0:
            self.cursor.execute('''Update notes set note = note || ? where sleep_record_id = ?;''', (notes, id))
        elif mode == 1:
            self.cursor.execute('''Update notes set note = ? where sleep_record_id = ?;''', (notes, id))
        self.conn.commit()

    def add_record_user(self, id, name):
        try:
            self.cursor.execute(
                '''insert into users (id,name) values (?,?)''',
                (id, name))
            self.conn.commit()
        except Exception as e:
            print(e)
        return 0

    def add_record_data(self, user_id=None, start_sleep=None, wake_time=None, quality=None, notes=None):
        self.cursor.execute(
            '''insert into sleep_records (user_id,start_sleep_time,wake_time,quality) values (?,?,?,?)''',
            (user_id, start_sleep, wake_time, quality))
        sleep_record_id = self.find_record(user_id=user_id, start_sleep=start_sleep, wake_time=wake_time,
                                           quality=quality)
        self.cursor.execute(
            '''insert into notes (note,sleep_record_id) values (?,?)''', (notes, sleep_record_id))
        self.conn.commit()
        return 0

    def find_record(self, user_id=None, start_sleep=None, wake_time=None, quality=None):
        return self.cursor.execute(
            '''select id from sleep_records where user_id = ? and start_sleep_time = ?;''',
            (user_id, start_sleep)).fetchone()[0]

    def find_note(self, id=None):
        return self.cursor.execute('''select note from notes where sleep_record_id = ?;''', (id,)).fetchone()[0]

    def edit_quality(self, quality=None, id=None):
        self.cursor.execute('''Update sleep_records set quality = ? where id = ?;''', (quality, id))
        self.conn.commit()


data_base_users = {}

data_base_records = Data_Access_Object()


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
        data_base_records.add_record_user(message.chat.id, message.from_user.first_name)
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
                data_base_users.get(message.from_user.id)['notes'] += ' По ' + str(
                    datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "\n")

                bot.send_message(message.chat.id,
                                 f'Доброе утро!\nВы спали: {count_sleeping_time(message.from_user.id)}')
                data_base_users.get(message.from_user.id)['quality'] = str('-')

                copy_data = data_base_users.get(message.chat.id).copy()
                copy_data['id'] = message.chat.id
                data_base_records.add_record_data(message.from_user.id,
                                                  start_sleep=data_base_users.get(message.from_user.id)[
                                                      'start_sleep_time'],
                                                  wake_time=data_base_users.get(message.from_user.id)['wake_time'],
                                                  quality=data_base_users.get(message.from_user.id)['quality'],
                                                  notes=data_base_users.get(message.from_user.id)['notes'])
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
                id = data_base_records.find_record(record[0], record[1])
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
                id_record = data_base_records.find_record(record[0], record[1])
                data_base_records.edit_note(id=id_record, notes=add_str,start_sleep=record[1], mode=0)
                bot.send_message(message.chat.id, "Заметка успешно добавлена!", reply_markup=add_keyboard())
    else:
        bot.send_message(message.chat.id, "Похоже ты ввел не верный номер заметки, попробуй еще раз")


def edit_note(message, number_of_note, founded_elements):
    note = message.text
    if number_of_note <= len(data_base_records.show_all(message.chat.id)):
        for record in data_base_records.show_all(message.chat.id):
            if record == founded_elements[number_of_note]:
                id_record = data_base_records.find_record(record[0],record[1])
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


bot.polling(none_stop=True, interval=0)
