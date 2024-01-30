import requests
import sys

__doc__ = """
Viết 1 script để liệt kê tất cả các GitHub repository của 1 user:
Ví dụ với user pymivn, sử dụng dữ liệu ở JSON format tại
https://api.github.com/users/pymivn/repos
"""


def githubrepos(name):
    result = []
    link = 'https://api.github.com/users/{}/repos'.format(name)
    json_data = requests.get(link).json()
    for i in json_data:
        result.append(i["name"])
    return result


def solve(input_data):
    return githubrepos(input_data)


def main():
    input_data = sys.argv[1]
    print(solve(input_data))


if __name__ == '__main__':
    main()
