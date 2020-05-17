from flask import Flask
from data import db_session
from data.films import Films
from data.genre import Genre
from lst_of_all import list_of_genre

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

child_adventures_f = ['Дорога домой: Невероятное путешествие', 'Один дома', 'Один дома 2: Затерянный в Нью-Йорке',
                      'Бесконечная история', 'Короткое замыкание', ' Бэйб: Четвероногий малыш', ' Инопланетянин',
                      'Короткое замыкание 2', 'Кристофер Робин', 'Питер Пэн', 'Бэйб: Поросенок в городе', 'Бетховен 2',
                      'Покемон. Детектив Пикачу', ' Мэри Поппинс возвращается', 'Алиса в Зазеркалье',
                      'Пэн: Путешествие в Нетландию', 'Один дома 3', 'Король лев', 'Монстр-траки', 'Бетховен 3',
                      'Бесконечная история 2: Новая глава', 'Один дома 4', 'Один дома 5: Праздничное ограбление',
                      'Мама', 'Зверополис', 'Моана', 'в поисках Немо', 'Мадагаскар', 'Ледниковый период 2: '
                                                                                     'Глобальное потепление',
                      'В поисках дори', 'Тайная жизнь домашних животных']

child_adventures_R = ['Золушка', 'Кащей Бессмертный', 'Про Красную Шапочку', 'Морозко', 'Остров сокровищ',
                      'Приключения Тома Сойера и Гекльберри Финна', 'Приключение Электроника', 'Мэри Поппинс, до'
                                                                                               'свидания',
                      'Три толстяка', 'Старик Хоттабыч', 'Мама', ' Королевство кривых зеркал', 'Илья Муромец'
                                                                                               ' и Соловей-Разбойник',
                      'Частное пионерское', 'Частное пионерское. Ура, каникулы!!!',
                      'Страна хороших деточек', 'Осторожно, каникулы', 'Приключения в изумрудном городе: Серебряные '
                                                                       'туфельки', 'Маленький принц', 'Дюймовочка',
                      'Бегство рогатых викингов', 'Дар',
                      'Слоненок-турист', 'Вещий сон', 'И я там был', 'Маленькая принцесса', 'Чебурашка',
                      'Князь Владимир', 'Добрыня Никитич и Змей Горыныч']

anime = ['Ходячий замок', 'Унесённые призраками', 'Ариэтти из страны лилипутов', 'Корабль-призрак', 'Дитя погоды ',
         'Волчьи дети Амэ и Юки', 'Ловцы забытых голосов', 'Патэма наоборот', 'Мой сосед Тоторо', 'Ветер крепчает',
         'Твое имя', 'Врата Штейна: Дежа вю']

comedy_R = ['Кухня в Париже', 'Держи удар, детка!', 'О чём говорят мужчины', 'Я худею', 'Холоп', 'Каникулы строгого'
                                                                                                 ' режима',
            'Последний богатырь', 'Призрак', 'Янка + Янко', 'Служебный роман', 'Служебный роман. Наше время',
            'Горько2', 'Взломать блогеров', 'Кавказская пленница',
            '8 первых свиданий', '30 свиданий', 'Домашний арест', 'Каникулы президента', 'Бабушка легкого поведения',
            'Бабушка лёгкого поведения 2. Престарелые мстители', 'Дублёр', 'Самый лучший день', 'Друзья друзей',
            'Всё и сразу', 'Хороший мальчик', 'Кухня. Последняя битва', '8 лучших свиданий', 'Бармен', 'Без границ',
            'Пять невест', 'Лёгок на помине', 'Мылодрама', 'Zолушка', 'Одной левой', 'Завтрак у папы',
            'Как я стал русским', 'Свадьба по обмену', 'Помню - не помню!', 'Срочно выйду замуж']
comedy_f = ['1 + 1', 'Криминальное чтиво', 'В джазе только девушки', 'Укрощение строптивого', 'Брюс Всемогущий',
            'Мистер и миссис Смит', 'Такси', 'Стажёр', 'Джуманджи', 'Предложение', 'Лжец лжец']
comedy_child = ['Каникулы маленького Николя', 'Чарли и шоколадная фабрика', 'Новые приключения Аладдина',
                'где это виданно, где это слыханно', 'Лавка чудес', 'Матильда', 'Король воздуха', 'Чудо на 34 улице',
                '4:0 в пользу Танечки', 'План игры', 'Дети шпионов', '']

dramma_f = ['За закатом рассвет', 'Побег из Шоушенка', 'Настоящая любовь', 'Список Шиндлера', 'Титаник', 'Зеленая миля',
            'Дюна', 'Зеленая книга']
drama_R = ['Война и мир', 'Белый Бим Черное ухо', 'Движение вверх', 'Сёстры', 'Лёд', 'Лёд2', 'Родина',
           'Временные трудности']
sport_f = ['Мой пес Скип', 'Касаясь пустоты', 'Гол!', 'Бешенный бык', 'Рокки', 'Малышка на миллион',
           'Легенда Багера Ванса']

musikl = ['Король лев', 'Богемская рапсодия', 'Анастасия', 'Красавица и чудовище', 'Паваротти', 'Звезда родилась',
          'Величайший шоумен', 'Бурлекс', 'Шаг вперёд', 'Зверопой', 'Стиляги', 'Рок на века', '', '']

historical = ['А зори здесь тихие', 'Калашников', 'Список Шиндлера', 'Социальная сеть', 'Чтец', 'Королева',
              'Тарас Бульба', 'Королевский роман', 'Александр Невский', 'Герцогиня', 'Броненосец «Потемкин»',
              'Орда', 'Голод', '', ]
biography = ['Легенда 17', 'Убеждение', 'Морис Ришар', 'Лев Яшин. Вратарь моей мечты', 'Высоцкий. Спасибо, что живой',
             'Матильда', 'Соль земли', 'Джейн Остин', 'Пианист', 'Мария - королева Шотландии', 'Колетт',
             'Жена смотрителя зоопарка', 'Варавва', 'Леди']


def main_main():
    for el in child_adventures_f:
        db_session.global_init("db/list_of_films.sqlite")
        f = Films()
        session = db_session.create_session()
        f.name = el
        f.country = 'foreign'
        f.company = 'child'
        session.add(f)
        # session.commit()
    for el in child_adventures_R:
        db_session.global_init("db/list_of_films.sqlite")
        f = Films()
        session = db_session.create_session()
        f.name = el
        f.country = 'Russia'
        f.company = 'child'
        session.add(f)
        # session.commit()
    for el in anime:
        db_session.global_init("db/list_of_films.sqlite")
        f = Films()
        session = db_session.create_session()
        f.name = el
        f.country = 'foreign'
        f.company = 'child'
        session.add(f)
        # session.commit()
    for el in comedy_R:
        db_session.global_init("db/list_of_films.sqlite")
        f = Films()
        session = db_session.create_session()
        f.name = el
        f.country = 'Russia'
        f.company = 'adult'
        session.add(f)
        # session.commit()
    for el in comedy_f:
        db_session.global_init("db/list_of_films.sqlite")
        f = Films()
        session = db_session.create_session()
        f.name = el
        f.country = 'foreign'
        f.company = 'adult'
        session.add(f)
        # session.commit()
    for el in comedy_child:
        db_session.global_init("db/list_of_films.sqlite")
        f = Films()
        session = db_session.create_session()
        f.name = el
        f.country = 'Russia'
        f.company = 'child'
        session.add(f)
        # session.commit()
    for el in dramma_f:
        db_session.global_init("db/list_of_films.sqlite")
        f = Films()
        session = db_session.create_session()
        f.name = el
        f.country = 'foreign'
        f.company = 'adult'
        session.add(f)
        # session.commit()
    for el in drama_R:
        db_session.global_init("db/list_of_films.sqlite")
        f = Films()
        session = db_session.create_session()
        f.name = el
        f.country = 'Russia'
        f.company = 'adult'
        session.add(f)
        # session.commit()
    for el in sport_f:
        db_session.global_init("db/list_of_films.sqlite")
        f = Films()
        session = db_session.create_session()
        f.name = el
        f.country = 'foreign'
        f.company = 'adult'
        session.add(f)
        # session.commit()
    for el in musikl:
        db_session.global_init("db/list_of_films.sqlite")
        f = Films()
        session = db_session.create_session()
        f.name = el
        f.country = 'Russia'
        f.company = 'adult'
        session.add(f)
        # session.commit()
    for el in historical:
        db_session.global_init("db/list_of_films.sqlite")
        f = Films()
        session = db_session.create_session()
        f.name = el
        f.country = 'Russia'
        f.company = 'adult'
        session.add(f)
        # session.commit()
    for el in biography:
        db_session.global_init("db/list_of_films.sqlite")
        f = Films()
        session = db_session.create_session()
        f.name = el
        f.country = 'foreign'
        f.company = 'child'
        session.add(f)
        # session.commit()
    for el in list_of_genre:
        db_session.global_init("db/list_of_films.sqlite")
        g = Genre()
        session = db_session.create_session()
        g.title_g = el
        session.add(g)
    # session.commit()

    app.run()


if __name__ == '__main__':
    main_main()
