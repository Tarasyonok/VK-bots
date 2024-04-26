import flask

app = flask.Flask(__name__)


import vk_api
from vk_api.vk_api import VkApiMethod

from config import LOGIN, PASSWORD, CLUB_ID, MAIN_ALBUM_ID


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def get_stats(group_id):
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler,
        app_id=6287487
    )

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    # try:
    vk = vk_session.get_api()

    response = vk.stats.get(group_id=group_id, intervals_count=10, stats_groups='reach')

    return response
    # except:
    #     print('Что то пошло не так')


# 148928912
@app.route("/vk_stat/<int:group_id>/")
def vk_stat(group_id):
    data = get_stats(group_id)
    print(data)

    activities = {}
    # activities['likes'] = data['activity']['likes']
    # activities['comments'] = data['activity']['comments']
    # activities['subscribed'] = data['activity']['subscribed']

    activities['likes'] = 0
    activities['comments'] = 0
    activities['subscribed'] = 0
    ages = {'12-18': 0, '18-21': 0, '21-24': 0, '24-27': 0, '27-30': 0, '30-35': 0, '35-45': 0, '45-100': 0}
    cities = set()
    for info in data:
        if 'activity' in info:
            activities['likes'] += info['activity']['likes']
            activities['comments'] += info['activity']['comments']
            activities['subscribed'] += info['activity']['subscribed']
            # print(info['activity'])
            for age in info['reach']['age']:
                ages[age['value']] += age['count']

            for city in info['reach']['cities']:
                cities.add(city['name'])

    print(activities)
    print(ages)
    print(cities)

    return flask.render_template('index.html', activities=activities, ages=ages, cities=cities)

[
    {'activity':
         {'comments': 10, 'copies': 4, 'likes': 632, 'subscribed': 2, 'unsubscribed': 4},
     'period_from': 1713783510,
     'period_to': 1713869909,
     'reach': {'age': [
         {'value': '12-18', 'count': 439},
         {'value': '18-21', 'count': 2177},
         {'value': '21-24', 'count': 2882},
         {'value': '24-27', 'count': 2112},
         {'value': '27-30', 'count': 867},
         {'value': '30-35', 'count': 611},
         {'value': '35-45', 'count': 257},
         {'value': '45-100', 'count': 121}
     ],
         'cities': [
             {'count': 553, 'name': 'Москва', 'value': 1},
             {'count': 363, 'name': 'Санкт-Петербург', 'value': 2},
             {'count': 134, 'name': 'Новосибирск', 'value': 99},
             {'count': 102, 'name': 'Екатеринбург', 'value': 49},
             {'count': 92, 'name': 'Красноярск', 'value': 73},
             {'count': 89, 'name': 'Челябинск', 'value': 158},
             {'count': 80, 'name': 'Краснодар', 'value': 72},
             {'count': 80, 'name': 'Ростов-на-Дону', 'value': 119},
             {'count': 76, 'name': 'Пермь', 'value': 110},
             {'count': 69, 'name': 'Самара', 'value': 123},
             {'count': 68, 'name': 'Tokyo', 'value': 1914764},
             {'count': 61, 'name': 'Омск', 'value': 104},
             {'count': 61, 'name': 'Воронеж', 'value': 42},
             {'count': 57, 'name': 'Уфа', 'value': 151},
             {'count': 55, 'name': 'Нижний Новгород', 'value': 95},
             {'count': 51, 'name': 'Томск', 'value': 144},
             {'count': 50, 'name': 'Тюмень', 'value': 147},
             {'count': 47, 'name': 'Хабаровск', 'value': 153},
             {'count': 45, 'name': 'Казань', 'value': 60},
             {'count': 45, 'name': 'Саратов', 'value': 125},
             {'count': 45, 'name': 'Иркутск', 'value': 57},
             {'count': 43, 'name': 'Волгоград', 'value': 10},
             {'count': 42, 'name': 'Барнаул', 'value': 25},
             {'count': 38, 'name': 'Ижевск', 'value': 56},
             {'count': 37, 'name': 'Владивосток', 'value': 37}
         ], 'countries': [
             {'code': 'RU', 'count': 9143, 'name': 'Россия', 'value': 1},
             {'code': 'KZ', 'count': 228, 'name': 'Казахстан', 'value': 4},
             {'code': 'BY', 'count': 129, 'name': 'Беларусь', 'value': 3},
             {'code': 'DE', 'count': 36, 'name': 'Германия', 'value': 65},
             {'code': 'FR', 'count': 21, 'name': 'Франция', 'value': 209},
             {'code': 'PL', 'count': 18, 'name': 'Польша', 'value': 160},
             {'code': 'UA', 'count': 17, 'name': 'Украина', 'value': 2},
             {'code': 'MD', 'count': 16, 'name': 'Молдова', 'value': 15},
             {'code': 'KG', 'count': 14, 'name': 'Кыргызстан', 'value': 11},
             {'code': 'JP', 'count': 11, 'name': 'Япония', 'value': 229},
             {'code': 'UZ', 'count': 10, 'name': 'Узбекистан', 'value': 18},
             {'code': 'EE', 'count': 10, 'name': 'Эстония', 'value': 14},
             {'code': 'NL', 'count': 9, 'name': 'Нидерланды', 'value': 139},
             {'code': 'GB', 'count': 9, 'name': 'Великобритания', 'value': 49},
             {'code': 'US', 'count': 8, 'name': 'США', 'value': 9},
             {'code': 'CN', 'count': 7, 'name': 'Китай', 'value': 97},
             {'code': 'KR', 'count': 6, 'name': 'Южная Корея', 'value': 226},
             {'code': 'LV', 'count': 6, 'name': 'Латвия', 'value': 12},
             {'code': 'AM', 'count': 6, 'name': 'Армения', 'value': 6},
             {'code': 'IL', 'count': 5, 'name': 'Израиль', 'value': 8},
             {'code': 'AZ', 'count': 5, 'name': 'Азербайджан', 'value': 5},
             {'code': 'CZ', 'count': 5, 'name': 'Чехия', 'value': 215},
             {'code': 'TH', 'count': 5, 'name': 'Таиланд', 'value': 191},
             {'code': 'TJ', 'count': 4, 'name': 'Таджикистан', 'value': 16},
             {'code': 'FI', 'count': 3, 'name': 'Финляндия', 'value': 207}
         ],
         'mobile_reach': 9464,
         'reach': 9778,
         'reach_subscribers': 3299,
         'sex': [
             {'value': 'f', 'count': 2688},
             {'value': 'm', 'count': 7090}
         ],
         'sex_age': [
             {'value': 'f;12-18', 'count': 179},
             {'value': 'f;18-21', 'count': 693},
             {'value': 'f;21-24', 'count': 900},
             {'value': 'f;24-27', 'count': 485},
             {'value': 'f;27-30', 'count': 164},
             {'value': 'f;30-35', 'count': 106},
             {'value': 'f;35-45', 'count': 50},
             {'value': 'f;45-100', 'count': 21},
             {'value': 'm;12-18', 'count': 260},
             {'value': 'm;18-21', 'count': 1484},
             {'value': 'm;21-24', 'count': 1982},
             {'value': 'm;24-27', 'count': 1627},
             {'value': 'm;27-30', 'count': 703},
             {'value': 'm;30-35', 'count': 505},
             {'value': 'm;35-45', 'count': 207},
             {'value': 'm;45-100', 'count': 100}]
     },
     'visitors': {'age': [
         {'value': '12-18', 'count': 7},
         {'value': '18-21', 'count': 16},
         {'value': '21-24', 'count': 12},
         {'value': '24-27', 'count': 6},
         {'value': '27-30', 'count': 3},
         {'value': '30-35', 'count': 4},
         {'value': '35-45', 'count': 1},
         {'value': '45-100', 'count': 1}
     ], 'cities': [{'count': 4, 'name': 'Новосибирск', 'value': 99}, {'count': 2, 'name': 'Tokyo', 'value': 1914764}, {'count': 2, 'name': 'Тюмень', 'value': 147}, {'count': 2, 'name': 'Хабаровск', 'value': 153}, {'count': 2, 'name': 'Москва', 'value': 1}, {'count': 2, 'name': 'Санкт-Петербург', 'value': 2}, {'count': 1, 'name': 'Washington, D.C.', 'value': 1661}, {'count': 1, 'name': 'Уссурийск', 'value': 150}, {'count': 1, 'name': 'Сыктывкар', 'value': 138}, {'count': 1, 'name': 'Челябинск', 'value': 158}, {'count': 1, 'name': 'Нижний Новгород', 'value': 95}, {'count': 1, 'name': 'Warszawa', 'value': 1922897}, {'count': 1, 'name': 'Кишинев', 'value': 1710959}, {'count': 1, 'name': 'Тула', 'value': 146}, {'count': 1, 'name': 'Рязань', 'value': 122}, {'count': 1, 'name': 'Екатеринбург', 'value': 49}, {'count': 1, 'name': 'Брянск', 'value': 33}, {'count': 1, 'name': 'Рубцовск', 'value': 424}, {'count': 1, 'name': 'Ростов-на-Дону', 'value': 119}, {'count': 1, 'name': 'Самара', 'value': 123}], 'countries': [{'code': 'RU', 'count': 50, 'name': 'Россия', 'value': 1}, {'code': 'IN', 'count': 1, 'name': 'Индия', 'value': 80}, {'code': 'MD', 'count': 1, 'name': 'Молдова', 'value': 15}, {'code': 'IL', 'count': 1, 'name': 'Израиль', 'value': 8}, {'code': 'EE', 'count': 1, 'name': 'Эстония', 'value': 14}], 'mobile_views': 56, 'sex': [{'value': 'f', 'count': 26}, {'value': 'm', 'count': 27}], 'sex_age': [{'value': 'f;12-18', 'count': 3}, {'value': 'f;18-21', 'count': 12}, {'value': 'f;21-24', 'count': 6}, {'value': 'f;24-27', 'count': 1}, {'value': 'f;27-30', 'count': 2}, {'value': 'f;30-35', 'count': 1}, {'value': 'f;35-45', 'count': 0}, {'value': 'f;45-100', 'count': 0}, {'value': 'm;12-18', 'count': 4}, {'value': 'm;18-21', 'count': 4}, {'value': 'm;21-24', 'count': 6}, {'value': 'm;24-27', 'count': 5}, {'value': 'm;27-30', 'count': 1}, {'value': 'm;30-35', 'count': 3}, {'value': 'm;35-45', 'count': 1}, {'value': 'm;45-100', 'count': 1}], 'views': 65, 'visitors': 54}}]

app.run()