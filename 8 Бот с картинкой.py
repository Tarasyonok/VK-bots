import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

from config import LOGIN, PASSWORD, CLUB_ID, MAIN_ALBUM_ID, TOKEN


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main():
    login, password = LOGIN, PASSWORD
    user_vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler,
        app_id=6287487
    )

    try:
        user_vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    user_vk = user_vk_session.get_api()
    try:
        response = user_vk.photos.get(album_id=MAIN_ALBUM_ID, group_id=CLUB_ID)
        print(response)

        images = response['items']
        id_list = []
        for img in images:

            id_list.append(f'photo{img["owner_id"]}_{img["id"]}')
    except:
        print('Что то пошло не так')
        return


    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, CLUB_ID)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.obj.message['from_id']
            response = user_vk.users.get(user_id=user_id)
            info = response[0]

            vk = vk_session.get_api()
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=f'Привет, {info["first_name"]}',
                             attachment=random.choice(id_list),
                             random_id=random.randint(0, 2 ** 64))



if __name__ == '__main__':
    main()
