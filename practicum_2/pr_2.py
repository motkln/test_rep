import random
from collections import Counter
from collections import namedtuple
from collections import defaultdict
from collections import deque


def get_random_list(lenght):
    random_list = [random.randint(1, 10) for x in range(lenght + 1)]
    return random_list


if __name__ == "__main__":
    # 1
    r_list = get_random_list(10)
    counter = Counter(r_list)
    print(f"Количество уникальных элементов: {len(counter)}")
    most_common = counter.most_common(3)
    for each in most_common:
        print(f"Число {each[0]} встретилось {each[1]} раз(а)")
    # 2
    Book = namedtuple("Book", ["title", "author", "genre"])
    Book1 = Book("Sherlock Holmes", "Conan Doyle", "detective")
    Book2 = Book("Harry Potter", "Dj.K. Rowling", "fantasy")
    books = [Book1, Book2]
    for each in books:
        print(f'Название: {each.title}, автор: {each.author}, жанр: {each.genre}')
    # 3
    my_dict = defaultdict(list)
    my_dict['games'].append("cs2")
    my_dict['games'].append("Dota 2")
    my_dict['games'].append("Stalker 2")
    my_dict['games'].append("Half life 2")
    my_dict['names'].append("Dima")
    my_dict['names'].append("Nastya")
    my_dict['names'].append("Polly")
    my_dict['names'].append("James")
    print(my_dict)
    # 4
    my_deq = deque()
    for _ in range(10):
        my_deq.append(random.randint(1,100))
    print(my_deq)
    my_deq.pop()
    print(my_deq)
    my_deq.popleft()
    print(my_deq)
    my_deq.appendleft(0)
    print(my_deq)
    my_deq.append(100)
    print(my_deq)
    # 5
    queue = deque()
    def is_empty():
        return len(queue) == 0

    def append_new(element):
        queue.append(element)

    def pop_el():
        if not is_empty():
            return queue.pop()
        else:
            print('Очередь уже пуста')

    append_new(1)
    append_new(2)
    append_new(3)
    print(queue)
    pop_el()
    print(queue)
    pop_el()