import json
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from datetime import datetime

from config import TOKEN, CLUB_ID

def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, CLUB_ID)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            text = event.obj.message['text']
            if any([1 for w in ['время', 'число', 'дата', 'день'] if w in text.lower()]):
                vk = vk_session.get_api()
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=datetime.now().strftime('%A %d.%m.%Y %H:%M:%S'),
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
