import requests
import collections


def get_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        res = response.json()
        return res
    else:
        raise Exception(f'Код ошибки: {response.status_code}')


def analyze_repos(repos):
    repositories = len([x['name'] for x in repos])
    total_stars = sum([x['stargazers_count'] for x in repos])
    most_famous_rep = sorted([(x['name'], x['stargazers_count']) for x in repos], key=lambda x: x[1], reverse=True)
    language_list = collections.Counter(x['language'] for x in repos)

    return f"""Аналитика профиля GitHub: {repos[0]['owner']['login']}
---------------------------------------------------
- Количество публичных репозиториев: {repositories}
- Общее количество звёзд: {total_stars}
- Самый популярный репозиторий: {most_famous_rep[0]}
- Топ языков программирования:{str(language_list)[str(language_list).rfind('{'):-1]}
---------------------------------------------------"""


def main():
    while True:
        username = input('Введите имя пользователя на GitHub:\n')
        try:
            repositories = get_repos(username)
        except Exception as e:
            print(e)
        else:
            print(analyze_repos(repositories))
            # задание 2
            result = autobahn_api()
            print(analyz_autobahn_api(result))




def autobahn_api():
    url = 'https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Ошибка {response.status_code}')


def analyz_autobahn_api(response):
    result = response['electric_charging_station']
    quantity = len(result)
    coordinates = [(x['title'], x['coordinate']) for x in result]
    return f"""Информация о зарядных станциях на автобанах Германии дороги A1
------------------------------------------------------------
Количество зарядных станций на дороге - {quantity}
Название зарядной станции, ее координаты  - {coordinates}"""

if __name__ == '__main__':
    main()
