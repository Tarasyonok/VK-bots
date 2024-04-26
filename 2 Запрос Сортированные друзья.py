from config import LOGIN, PASSWORD

import vk_api
from datetime import datetime


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
    vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    response = vk.friends.get(fields='bdate, city')
    if response['items']:
        for item in sorted(response['items'], key=lambda x: x['last_name']):
            try:
                print(item['last_name'], item['first_name'], item['bdate'])
            except:
                print(f"С другом id={item['id']} что-то не так 0_0")


if __name__ == '__main__':
    main()
