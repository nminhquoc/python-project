__doc__ = """
Viết một script kiểm tra xem các số argument đầu vào có trúng lô không
(2 số cuối trùng với một giải nào đó). Nếu không có argument nào thì print
ra tất cả các giải từ đặc biệt -> giải 7.
Lấy kết quả từ ketqua1.net.
"""

import requests
from bs4 import BeautifulSoup
import sys


def find_lottery():
    lottery = []
    ses = requests.Session()
    r = ses.get("http://ketqua1.net", timeout=5)
    tree = BeautifulSoup(markup=r.text, features='html.parser')
    for number in tree.find_all('div', attrs={"data-sofar": True}):
        lottery.append(number.text)
    return lottery


def display_lottery(lottery):
    view = '''
    Giải đặc biệt:              {}
    Giải nhất:                  {}
    Giải nhì:           {}              {}
    Giải ba:        {}          {}          {}
                    {}          {}          {}
    Giải tư:    {}        {}          {}        {}
    Giải năm:       {}          {}          {}
                    {}          {}          {}
    Giải sáu:       {}           {}           {}
    Giải bảy:    {}          {}            {}          {}
    '''
    result = view.format(*lottery[1:])
    return result


def check_lottery(number, winner_number):
    for i in winner_number[1:]:
        if i[-2:] == number[-2:]:
            result = True
            break
        else:
            result = False
    if result == True:
        print("Bạn đã trúng giải")
    else:
        print("Chúc bạn may mắn lần sau")
    return result


def solve(input_number):
    if check_lottery(input_number, find_lottery()) == False:
        print(display_lottery(find_lottery()))


def main():
    input_data = sys.argv[1]
    solve(input_data)


if __name__ == '__main__':
    main()
