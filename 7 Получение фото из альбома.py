import vk_api
from config import LOGIN, PASSWORD, CLUB_ID, MAIN_ALBUM_ID


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

    try:
        vk = vk_session.get_api()
        response = vk.photos.get(album_id=MAIN_ALBUM_ID, group_id=CLUB_ID)
        print(response)

        images = response['items']
        for img in images:
            max_quality = [0, 0]
            url = ''
            for size in img['sizes']:
                if size['width'] > max_quality[0]:
                    max_quality = [size['width'], size['height']]
                    url = size['url']

            print(f'{max_quality[0]}X{max_quality[1]}\t\t{url}')
    except:
        print('Что то пошло не так')

if __name__ == '__main__':
    main()
