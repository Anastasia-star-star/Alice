from flask import Flask, request
import logging
import json
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)

logging.basicConfig(level=logging.INFO)
sessionStorage = {}

list_of_films = ['аниме', 'биография', 'боевик', 'вестерн', 'военный',
                 'детектив', 'детский', 'документальный', 'драма',
                 'исторический', 'кинокомикс', 'комедия', 'концерт',
                 'криминал', 'мелодрама', 'мистика', 'мультфильм',
                 'мюзикл',
                 'научный', 'приключения', 'реалити - шоу', 'семейный',
                 'спорт', 'триллер', 'ужасы', 'фантастика',
                 'фильм - нуар', 'фэнтези']

list_of_all_company = ['один', 'одна', 'сам с собой', 'сама с собой', 'компанией', 'другом', 'друзьями', 'семьёй',
                       'родственниками', 'родителями', 'мамой',
                       'папой', 'тётей', 'второй половинкой', 'парнем', 'девушкой', 'сестрой', 'братом', 'сестрами',
                       'братьями']

list_of_alone = ['один', 'одна', 'сам с собой', 'сама с собой']
list_of_big_company = ['компанией', 'другом', 'друзьями', 'семьёй', 'родственниками', 'родителями', 'мамой',
                       'папой', 'тётей', 'второй половинкой', 'парнем', 'девушкой', 'сестрой', 'братом', 'сестрами',
                       'братьями']


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {'company': None,
                                   'actors': None,
                                   'genre': None,
                                   'country': None}
        # company = False
        res['response']['text'] = 'Привет! Это приложение называется кинолюбитель.' \
                                  ' Оно поможет тебе выбрать кино по вкусу'
        res['response']['buttons'] = [{'title': 'Помощь',
                                       'hide': True}]
        return

    # Блок определяющий компанию пользователя
    if sessionStorage[user_id]['company'] is None:
        res['response']['text'] = 'Скажите, пожалуйста, вы будете смотреть фильм один, c семьей или с компанией друзей'
        res['response']['buttons'] = [{'title': elem,
                                       'hide': True} for elem in ['С друзьями', 'Один', 'С семьёй', 'Помощь']]
        sessionStorage[user_id]['company'] = True
        return

    if req['request']['original_utterance'].lower() in 'с друзьями' and sessionStorage[user_id]['company']:
        sessionStorage[user_id]['company'] = 'с друзьями'
        res['response']['text'] = 'Это отлично! Буду подбирать кино для компании друзей'
        return

    if req['request']['original_utterance'].lower() == 'помощь':
        res['response']['text'] = 'Это приложение называется кинолюбитель.' \
                                  ' Оно поможет тебе выбрать кино по вкусу, анализируя Ваши ответы'
        return



    # Блок определяющий предпочтённый ЖАНР пользователя / пользователей
    if sessionStorage[user_id]['company'].lower() in list_of_all_company and sessionStorage[user_id]['genre'] is None:
        if sessionStorage[user_id]['company'].lower() in list_of_big_company:
            res['response']['text'] = 'Какой жанр наиболее предпочтённый в вашей компании?'
        if sessionStorage[user_id]['company'].lower() in list_of_big_company:
            res['response']['text'] = 'Какой жанр наиболее Вам предпочтённый?'
        res['response']['buttons'] = [{'title': elem,
                                       'hide': True} for elem in list_of_films]
        sessionStorage[user_id]['genre'] = True
        return
    if sessionStorage[user_id]['genre'] is True


if __name__ == '__main__':
    app.run()
