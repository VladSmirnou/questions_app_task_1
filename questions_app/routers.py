import requests

from flask import request, Blueprint

from .extentions import db
from .models import Question


main = Blueprint('main', __name__)

@main.route('/', methods=['POST'])
def main_view():
    try:
        if not isinstance(number:= request.get_json().get('questions_num'), int):
            if number is None:
                return make_err('Invalid key or value is null', 400)
            return make_err('Invalid value data type. Must be [ int ]', 400)
    except:
        return make_err('Invalid MIME type. Must be [ application/json ]', 415)
    
    if not 0 < number <= 100:
        return make_err('Invalid number. Must be 0 < [ number ] <= 100', 400)
    
    if data:= api_call(number):
        return write_db(data, number)
    return make_err('Service is not available', 503)


def write_db(data, number, iterations_count=1, last_saved_question=None):
    for dct in data:
        if not Question.query.get(dct['id']):
            if number:
                number -= 1
                last_saved_question = Question(
                    id=dct['id'],
                    question=dct['question'],
                    answer=dct['answer'],
                    date_created=dct['created_at'],
                )
                db.session.add(last_saved_question)
                db.session.commit()
            else:
                break
    if number:
        if iterations_count > 50:  # число 50 просто случайный порог, можно увеличить или уменьшить
            if last_saved_question:
                return make_response(last_saved_question)
            return {}, 200
        
        if data:= api_call():
            return write_db(data, number, iterations_count + 1, last_saved_question)
        
        if last_saved_question:
            return {
                'status': 'error',
                'message': ('An internal error has occurred while processing '
                            'the request. Service has stopped responding'),
                'last saved question': make_response(last_saved_question)[0],
            }, 201
        return make_err('Service is not available', 503)
    
    return make_response(last_saved_question)
    

def api_call(number=None):
    URL = f'https://jservice.io/api/random?count={number or 25}'  # чем больше пул, тем меньше реквестов к API
    resp = requests.get(URL)
    if resp.status_code == 200:
        return resp.json()


def make_response(last_saved_question):
    return {
    'id': last_saved_question.id,
    'question': last_saved_question.question,
    'answer': last_saved_question.answer,
    'date_created': last_saved_question.date_created,
    }, 201


def make_err(err_message, code):
    return {
        'status': 'error',
        'message': err_message,
    }, code
