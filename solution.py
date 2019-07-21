# Interactive python client for fizzbot

import json
import urllib.request
import urllib.error

domain = 'https://api.noopschallenge.com'

def print_sep(): print('----------------------------------------------------------------------')

# print server response
def print_response(dict):
    print(dict)
    print('')
    print('message:')
    print(dict.get('message'))
    print('')
    for key in dict:
        if key != 'message':
            print('%s: %s' % (key, json.dumps(dict.get(key))))
    print('')

# try an answer and see what fizzbot thinks of it
def try_answer(question_url, answer):
    print_sep()
    body = json.dumps({ 'answer': answer })
    print('*** POST %s %s' % (question_url, body))
    try:
        req = urllib.request.Request(domain + question_url, data=body.encode('utf8'), headers={'Content-Type': 'application/json'})
        res = urllib.request.urlopen(req)
        response = json.load(res)
        print_response(response)
        print_sep()
        return response

    except urllib.error.HTTPError as e:
        response = json.load(e)
        print_response(response)
        return response

# keep trying answers until a correct one is given
def get_correct_answer(question_url, question_data, old_rules):
    while True:
        if 'exampleResponse' in question_data and question_data['exampleResponse']['answer'] == 'COBOL': answer = 'COBOL'
        else:
            answer = doFizzBuzz(question_data['numbers'], question_data["rules"] if "rules" in question_data else old_rules)

        response = try_answer(question_url, answer)

        if (response.get('result') == 'interview complete'):
            print('congratulations!')
            exit()

        if (response.get('result') == 'correct'):
            return response.get('nextQuestion')

# do the next question
def do_question(domain, question_url, old_rules):
    print_sep()
    print('*** GET %s' % question_url)

    request = urllib.request.urlopen( ('%s%s' % (domain, question_url)) )
    question_data = json.load(request)
    print_response(question_data)
    print_sep()

    next_question = question_data.get('nextQuestion')

    rules = question_data["rules"] if "rules" in question_data else old_rules

    if next_question: return next_question, rules
    return get_correct_answer(question_url, question_data, old_rules), old_rules


def doFizzBuzz(numbers, rules):
    answer = ""
    for num in numbers:
        appended = False
        for rule in rules:
            if num % rule["number"] == 0:
                answer += rule['response']
                appended = True
        if not appended:
            answer += str(num)
        answer += " "
    return answer.strip()

def main():
    question_url = '/fizzbot'
    old_rules = []
    while question_url:
        question_url, old_rules = do_question(domain, question_url, old_rules)

if __name__ == '__main__': main()
