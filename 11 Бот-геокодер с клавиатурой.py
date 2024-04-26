import json
from io import BytesIO

import requests
import vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from datetime import datetime

from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from config import TOKEN, CLUB_ID

user_ans = {}


def upload_photo(upload, url):
    img = requests.get(url).content
    f = BytesIO(img)

    response = upload.photo_messages(f)[0]

    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']

    return owner_id, photo_id, access_key


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    settings = dict(one_time=True, inline=False)
    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label='Карта', color=VkKeyboardColor.POSITIVE,
                                 payload={"type": "map"})
    keyboard.add_line()
    keyboard.add_callback_button(label='Спутниковый снимок', color=VkKeyboardColor.PRIMARY,
                                 payload={"type": "sat"})
    keyboard.add_line()
    keyboard.add_callback_button(label='Гибрид', color=VkKeyboardColor.SECONDARY,
                                 payload={"type": "skl"})

    longpoll = VkBotLongPoll(vk_session, CLUB_ID)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.obj.message['from_id']
            vk = vk_session.get_api()

            if user_id not in user_ans:
                user_ans[user_id] = '1'
                vk.messages.send(user_id=user_id,
                                 message='Привет, какое место ты хочешь увидеть?',
                                 random_id=random.randint(0, 2 ** 64))
            elif user_ans[user_id] == '1':
                try:
                    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
                    response = requests.get(geocoder_uri, params={
                        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                        "format": "json",
                        "geocode": event.obj.message['text']
                    })

                    data = response.json()

                    print(data)
                    toponym = data["response"]["GeoObjectCollection"][
                        "featureMember"][0]["GeoObject"]

                    lower_c = toponym["boundedBy"]["Envelope"]["lowerCorner"].replace(' ', ',')
                    upper_c = toponym["boundedBy"]["Envelope"]["upperCorner"].replace(' ', ',')

                    bbox = f"{lower_c}~{upper_c}"

                    # Можно воспользоваться готовой функцией,
                    # которую предлагалось сделать на уроках, посвящённых HTTP-геокодеру.

                    place_name = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"]
                    static_api_request = f"http://static-maps.yandex.ru/1.x/?bbox={bbox}"
                    print(static_api_request)

                    user_ans[user_id] = '2'
                    vk.messages.send(user_id=user_id,
                                     message='Выберете тип карты',
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=keyboard.get_keyboard())
                except:
                    vk.messages.send(user_id=user_id,
                                     message='Нечего не найдено, назовите другое место',
                                     random_id=random.randint(0, 2 ** 64))

            elif user_ans[user_id] == '2':
                vk.messages.send(user_id=user_id,
                                 message='Выберете тип карты на клавиатуре',
                                 random_id=random.randint(0, 2 ** 64),
                                 keyboard=keyboard.get_keyboard())

        elif event.type == VkBotEventType.MESSAGE_EVENT:
            # if event.object.payload.get('type') == 'map':
            #     vk.messages.send(user_id=user_id,
            #                      message='Ура',
            #                      conversation_message_id=event.obj.conversation_message_id,
            #                      random_id=random.randint(0, 2 ** 64),
            #                      keyboard=[])
            if event.object.payload.get('type') == 'map':
                l = 'map'

            if event.object.payload.get('type') == 'sat':
                l = 'sat'

            if event.object.payload.get('type') == 'skl':
                l = 'skl'

            upload = VkUpload(vk)
            static_api_request += f'&l={l}'
            print(static_api_request)

            owner_id, photo_id, access_key = upload_photo(upload, static_api_request)

            attachment = f'photo{owner_id}_{photo_id}_{access_key}'
            user_ans[user_id] = '1'
            vk.messages.send(
                user_id=user_id,
                message=f'Это {place_name}. Что вы еще хотите увидеть?',
                random_id=random.randint(0, 2 ** 64),
                attachment=attachment,
                keyboard=keyboard.get_empty_keyboard())




if __name__ == '__main__':
    main()
