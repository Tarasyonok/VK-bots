# вставить свои данные в package.json
import json
import requests
import os

from config import ACCESS_TOKEN, MAIN_ALBUM_ID, CLUB_ID

def get_upload_server():
    params_vk = {
        'access_token': ACCESS_TOKEN,
        'album_id': MAIN_ALBUM_ID,
        'group_id': CLUB_ID,
        'v': 5.199
    }
    print(params_vk)
    result = requests.get('https://api.vk.com/method/photos.getUploadServer', params=params_vk).json()
    print(result)
    return result['response']['upload_url']


def get_result(req):
    params_vk = {
        'access_token': ACCESS_TOKEN,
        'album_id': req['aid'],
        'group_id': req['gid'],
        'server': req['server'],
        'photos_list': req['photos_list'],
        'hash': req['hash'],
        'v': 5.199
    }
    result = requests.get('https://api.vk.com/method/photos.save', params=params_vk).json()
    return result


def main():
    files = {
        'file1': open(os.path.join('static', 'img', 'img1.png'), mode='rb'),
        'file2': open(os.path.join('static', 'img', 'img2.jpg'), mode='rb'),
        'file3': open(os.path.join('static', 'img', 'img3.jpg'), mode='rb'),
    }

    url = get_upload_server()
    req = requests.post(url, files=files).json()
    get_result(req)


if __name__ == '__main__':
    main()
