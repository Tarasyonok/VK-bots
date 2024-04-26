import json
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from datetime import datetime

from config import TOKEN, CLUB_ID

user_ans = set()

def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, CLUB_ID)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.obj.message['from_id']
            vk = vk_session.get_api()
            if user_id not in user_ans:
                user_ans.add(user_id)
                vk.messages.send(user_id=user_id,
                                 message='Привет, я могу сказать, в какой день недели была какая-нибудь дата и введи дату в формате YYYY-MM-DD',
                                 random_id=random.randint(0, 2 ** 64))
            else:
                try:
                    y, m, d = map(int, event.obj.message['text'].split('.'))
                    vk = vk_session.get_api()
                    vk.messages.send(user_id=user_id,
                                     message=datetime(year=y, month=m, day=d).strftime('%A'),
                                     random_id=random.randint(0, 2 ** 64))
                except:
                    vk.messages.send(user_id=user_id,
                                     message='Что то пошло не так',
                                     random_id=random.randint(0, 2 ** 64),)


if __name__ == '__main__':
    main()
