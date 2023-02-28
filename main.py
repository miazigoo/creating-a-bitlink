import argparse
import os


import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()


def createParser():
    """parse link arg"""
    parser = argparse.ArgumentParser(
        description="""Программа создает битлинк. Если это битлтнк - сколько кликов по ней было.""")
    parser.add_argument('link', nargs='?', help='Введите сылку: ')
    link = parser.parse_args().link

    return link


def split_parse_url(user_input):
    """finding the link path"""
    url_split = urlparse(user_input)
    parsed = f'{url_split.netloc}{url_split.path}'
    return parsed


def shorten_link(user_input, url, token):
    """creating a bitlink"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    data = {"long_url": user_input}
    response_post = requests.post(url, headers=headers, json=data)
    response_post.raise_for_status()
    bit_link = response_post.json()['link']
    return bit_link


def count_clicks(user_input, url, parsed, token):
    """get the number of clicks on the bitlink"""
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response_get = requests.get(f'{url}{parsed}/clicks/summary',
                                headers=headers)
    response_get.raise_for_status()

    clicks_count = response_get.json()["total_clicks"]
    return clicks_count


def is_bitlink(url, user_input, parsed, token):
    """Checking on bitlink"""
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response_get = requests.get(f'{url}{parsed}',
                                headers=headers)
    return response_get.ok


def main():
    user_input = createParser()
    bitlink_url = 'https://api-ssl.bitly.com/v4/bitlinks/'
    parsed = split_parse_url(user_input)
    token = os.environ['BITLINK_TOKEN']
    try:
        if is_bitlink(bitlink_url, user_input, parsed, token):
            clicks_count = count_clicks(user_input, bitlink_url, parsed, token)
            print('Колличество кликов по ссылке: ', clicks_count)
        else:
            bitlink = shorten_link(user_input, bitlink_url, token)
            print('Битлинк: ', bitlink)
    except:
        print('Введена не корректная ссылка')


if __name__ == '__main__':
    main()
