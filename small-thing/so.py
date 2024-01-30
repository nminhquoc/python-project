__doc__ = """
Viết script lấy top **N** câu hỏi được vote cao nhất của tag
**LABEL** trên stackoverflow.com.
In ra màn hình: Title câu hỏi, link đến câu trả lời được vote cao nhất

Link API: https://api.stackexchange.com/docs

Dạng của câu lệnh:

  python3 so.py N LABEL
"""

import sys

import requests


def get_question(N, LABEL):
    result = []
    question_url = ('https://api.stackexchange.com/2.3/questions?pagesize={}'
                    '&order=desc&sort=votes&tagged={}'
                    '&site=stackoverflow').format(N, LABEL)
    answer_url = ('https://api.stackexchange.com/2.3/questions/{}'
                  '/answers?pagesize=1&order=desc'
                  '&sort=votes&site=stackoverflow')

    ses_question = requests.Session()
    ses_answer = requests.Session()

    r_question = ses_question.get(question_url, timeout=15)
    question_data = r_question.json()
    for question in question_data['items']:
        r_answer = ses_answer.get(answer_url.format(
            question['question_id']), timeout=15)
        answer_data = r_answer.json()
        for answer in answer_data['items']:
            answer_link = question['link'] + '/' + '{0}#{0}'.format(
                answer['answer_id'])
            result.append((question['title'], answer_link))
    return result


def solve(input_data):
    N = input_data[0]
    LABEL = input_data[1]
    result = get_question(N, LABEL)
    for question, link_answer in result:
        print('Question title: {}\nAnswer link: {}'.format(
            question, link_answer))


def main():
    input_data = sys.argv[1:]
    solve(input_data)


if __name__ == '__main__':
    main()
