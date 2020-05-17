from flask import Flask, request
import logging
import json
from flask_ngrok import run_with_ngrok
from data import db_session
from data.films import Films
from data.genres import Genres
from main_file import main_main

from data.genre import Genre
from lst_of_all import list_of_all_age, list_of_genre, list_of_adult, list_of_child

app = Flask(__name__)
run_with_ngrok(app)

logging.basicConfig(level=logging.INFO)
sessionStorage = {}


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
    if (req['request']['original_utterance'].lower() == 'помощь' or 'как это работает' in req['request']
    ['original_utterance'].lower()) and sessionStorage[user_id]['genre'] is None:
        res['response']['text'] = 'Это приложение называется кинолюбитель.' \
                                  ' Оно поможет тебе выбрать кино по вкусу, анализируя Ваши ответы на мои вопросы'
        return

    if req['session']['new']:
        sessionStorage[user_id] = {'company': None,
                                   'genre': None,
                                   'country': None}

        res['response']['buttons'] = [{'title': 'Помощь',
                                       'hide': True}]
        res['response']['text'] = 'Привет! Это приложение называется кинолюбитель.' \
                                  ' Оно поможет тебе выбрать кино по вкусу. \n'

        if sessionStorage[user_id]['company'] is None:
            res['response']['text'] += 'Скажите, пожалуйста, среди зрителей есть дети?'
            res['response']['buttons'] = [{'title': elem,
                                           'hide': True} for elem in list_of_all_age]
            sessionStorage[user_id]['company'] = True
        return

    # Блок определяющий Компанию пользователя.
    if sessionStorage[user_id]['company'] is True:
        for company in list_of_adult:
            if company in req['request']['original_utterance']:
                sessionStorage[user_id]['company'] = 'adult'
                res['response']['text'] = 'Отлично! Буду подбирать Вам кино для хорошего просмотра) \n'
                break
        for company in list_of_child:
            if company in req['request']['original_utterance']:
                sessionStorage[user_id]['company'] = 'child'
                res['response']['text'] = 'Это отлично! Буду подбирать кино с учетом детей!\n'
                break
        if sessionStorage[user_id]['company'] is True:
            res['response']['buttons'] = [{'title': elem,
                                           'hide': True} for elem in list_of_all_age]
            res['response']['text'] = 'Извините, я не расслышала. Повторите, пожалуйста!'
            return

        # start genre
        if type(sessionStorage[user_id]['company']) is str:
            res['response']['text'] += 'Какой жанр наиболее предпочтённый Вам и, может, Вашей компании?'
            res['response']['buttons'] = [{'title': elem,
                                           'hide': True} for elem in list_of_genre]
            res['response']['buttons'].append({'title': 'Помощь',
                                               'hide': True},
                                              {'title': 'Как это работает?',
                                               'hide': True})
            sessionStorage[user_id]['genre'] = True
        # end

        if sessionStorage[user_id]['company'] is True:
            res['response']['text'] = 'Прошу прощения, но я не поняла, что вы сказали. Повторите ещё раз.'
            res['response']['buttons'] = [{'title': elem,
                                           'hide': True} for elem in list_of_genre]
            res['response']['buttons'].append({'title': 'Помощь',
                                               'hide': True})
            res['response']['buttons'].append({'title': 'Как это работает?',
                                               'hide': True})
        return

    # Блок определяющий предпочтённый ЖАНР пользователя / пользователей
    if sessionStorage[user_id]['genre'] is True:
        for el in ['какие бывают жанры', 'помощь']:
            if el in req['request']['original_utterance'].lower():
                res['response'][
                    'text'] = 'От вас требуется сказать или ввести жанр фильма, который вы бы хотели посмотреть.\n' \
                              'Типы жанров: '
                for el in list_of_genre:
                    res['response']['text'] += el + '\n'
                break
        return
    if sessionStorage[user_id]['genre'] is True:
        for genre in list_of_genre:
            if genre in req['request']['original_utterance'].lower():
                sessionStorage[user_id]['genre'] = genre
                res['response']['text'] = 'Едем дальше! Вы хотели бы посмотреть зарубежное или российское кино?'
                break
        if sessionStorage[user_id]['genre'] is True:
            res['response']['text'] = 'Я знаю довольно много жанров кино, но конкретно этот - нет. ' \
                                      'Предложите другой жанр.'
            res['response']['buttons'] = [{'title': elem,
                                           'hide': True} for elem in list_of_genre]
            res['response']['buttons'].append({'title': 'Помощь',
                                               'hide': True})
            res['response']['buttons'].append({'title': 'Как это работает?',
                                               'hide': True})
        return

    # start Блок отвечающий за страну, выпустившею фильм
    if type(sessionStorage[user_id]['genre']) is str:
        for country in ['российское', 'россия', 'отечественное', 'наше']:
            if country in req['request']['original_utterance'].lower():
                sessionStorage[user_id]['country'] = 'Russia'
                res['response']['text'] = 'Хороший выбор. Буду подбирать Вам российское кино) \n'
                break
            else:
                res['response']['text'] = 'Ну хорошо! Тогда будет зарубежное кино) \n'
                sessionStorage[user_id]['country'] = 'foreign'
    # end

    # start Блок, выполняющий взаимодействие с базой данных
    if type(sessionStorage[user_id]['country']) is str:
        need_genre = sessionStorage[user_id]['genre']
        need_company = sessionStorage[user_id]['company']
        need_country = sessionStorage[user_id]['country']

        db_session.global_init("db/list_of_films.sqlite")
        session = db_session.create_session()

        g = session.query(Genre.id).filter(Genre.title_g == need_genre).all()
        id_g = g[0][0]
        id_fs = session.query(Genres.id_film).filter(Genres.id_genre == id_g).all()
        data_id_film = []
        lst_films = []
        for el in id_fs:
            data_id_film.append(el[0])

        for idd in data_id_film:
            film = session.query(Films.name).filter(Films.id == idd, Films.company == need_company,
                                                    Films.country == need_country).all()
            if film == []:
                break
            lst_films.append(film)
        result_lst = [el[0] for el in lst_films]
        res['response']['text'] += ' Вот что я могу предложить по вашему запросу:'
        for el in result_lst:
            res['response']['text'] += f' {el[0]} \n'
        res['response']['text'] += 'Приятного просмотра!'
        return
    # end


if __name__ == '__main__':
    app.run()
