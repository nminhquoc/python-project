__doc__ = '''Viết script dùng API tạo 1 Trello board với 2 list "Thứ 3", "Thứ 5",
và tạo 12 card ứng với 12 buổi học của lớp, có set due date ứng với các ngày
học.'''

import datetime
import os

import requests

file_path = os.path.dirname(__file__)

with open(os.path.join(file_path, 'trello_api.txt'), 'rt') as f:
    api_key = f.read()

with open(os.path.join(file_path, 'trello_token.txt'), 'rt') as f:
    token_key = f.read()


def create_board(key, token, name, color):
    url = 'https://api.trello.com/1/boards'
    obj = {'key': key, 'token': token, 'name': name, 'prefs_background': color}
    url_ses = requests.Session()
    url_res = url_ses.post(url, params=obj, timeout=3)
    url_data = url_res.json()
    if url_res.status_code != 200:
        return None
    return url_data


def create_list(id_board, key, token, name):
    url = "https://api.trello.com/1/boards/{}/lists".format(id_board)
    obj = {'key': key, 'token': token, 'name': name}
    url_ses = requests.Session()
    url_res = url_ses.post(url, params=obj, timeout=3)
    url_data = url_res.json()
    if url_res.status_code != 200:
        return None
    return url_data


def create_card(id_list, key, token, name, duedate):
    url = "https://api.trello.com/1/cards"
    obj = {'key': key, 'token': token, 'name': name, 'due': duedate, 'idList': id_list}
    url_ses = requests.Session()
    url_res = url_ses.post(url, params=obj, timeout=3)
    url_data = url_res.json()
    if url_res.status_code != 200:
        return None
    return url_data


def main():
    list_day = list(range(7))
    board = create_board(api_key, token_key, 'Python course', 'sky')
    week = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
    for i in range(7):
        list_day[i] = create_list(board['id'], api_key, token_key, week[i])

    learning_date_tue = datetime.datetime(year=2022, month=3, day=22)
    learning_date_thu = datetime.datetime(year=2022, month=3, day=24)

    for i in range(1, 13):
        if i % 2 == 0:
            create_card(list_day[2]['id'], api_key, token_key,
                        'Lesson' + str(i), learning_date_tue)
            learning_date_tue += datetime.timedelta(days=7)
        else:
            create_card(list_day[4]['id'], api_key, token_key,
                        'Lesson' + str(i), learning_date_thu)
            learning_date_thu += datetime.timedelta(days=7)


if __name__ == '__main__':
    main()
