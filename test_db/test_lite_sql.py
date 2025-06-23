from sqlite3 import connect


def get_connection():
    return connect('library.db')


def make_lib_table(cursor):
    cursor.execute('''Create table if not exists books(
    id integer primary key AUTOINCREMENT not null,
    title text not null,
    author text not null,
    year integer not null,
    UNIQUE (title, author, year));''')


def add_new_book(cursor, books):
    try:
        cursor.executemany('''Insert into books (title,author,year) values (?,?,?);''', books)
    except sqlite3.Error as e:
        print(e)
        return False
    else:
        return True


def show_all_books(cursor):
    return cursor.execute('''Select * from books''').fetchall()


def find_record_id(cursor, title, author, year):
    return cursor.execute('''select id from books where title = ? and author = ? and year = ?;''',
                          (title, author, year)).fetchone()[0]


def update_record(cursor, id, new_title, new_author, new_year):
    try:
        cursor.execute('''update books set title = ?, author = ?, year = ? where id = ?;''',
                       (new_title, new_author, new_year, id))
    except sqlite3.Error as e:
        print(e)


def delete_record(cursor, id):
    try:
        cursor.execute('''Delete from books where id = ?;''', (id,))
    except sqlite3.Error as e:
        print(e)


if __name__ == "__main__":
    conn = get_connection()
    cursor = conn.cursor()
    make_lib_table(cursor)
    books = [
        ("1984", "Джордж Оруэлл", 1949),
        ("Убить пересмешника", "Харпер Ли", 1960),
        ("Великий Гэтсби", "Фрэнсис Скотт Фицджеральд", 1925),
        ("Sherlock Holmes", "Conan Doyle", 2007)
    ]
    if add_new_book(cursor, books):
        conn.commit()
    print(show_all_books(cursor))
    record_id = find_record_id(cursor, 'Sherlock Holmes', 'Conan Doyle', 2007)
    update_record(cursor, record_id, 'Sherlock Holmes', 'Arthur Conan Doyle', 2009)
    print(show_all_books(cursor))
    delete_record(cursor, find_record_id(cursor,'Sherlock Holmes', 'Arthur Conan Doyle', 2009))
    print(show_all_books(cursor))