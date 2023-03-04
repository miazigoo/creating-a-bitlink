import argparse
import os

import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def get_command_line_argument():
    """parse link arg"""
    parser = argparse.ArgumentParser(
        description="""Программа создает битлинк. Если это битлтнк - сколько кликов по ней было.""")
    parser.add_argument('link', nargs='?', help='Введите сылку: ')
    link = parser.parse_args().link

    return link


def split_url(user_input):
    """finding the link path"""
    parse = urlparse(user_input)
    split_link = f'{parse.netloc}{parse.path}'
    return split_link


def shorten_link(user_input, url, token):
    """creating a bitlink"""
    headers = {
        'Authorization': f'Bearer {token}',
    }
    long_link = {"long_url": user_input}
    response = requests.post(url, headers=headers, json=long_link)
    response.raise_for_status()
    bit_link = response.json()['link']
    return bit_link


def count_clicks(user_input, url, parsed, token):
    """get the number of clicks on the bitlink"""
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'{url}{parsed}/clicks/summary',
                                headers=headers)
    response.raise_for_status()

    clicks_count = response.json()["total_clicks"]
    return clicks_count


def is_bitlink(url, user_input, parsed, token):
    """Checking on bitlink"""
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'{url}{parsed}',
                                headers=headers)
    return response.ok


def main():
    load_dotenv()
    user_input = get_command_line_argument()
    bitlink_url = 'https://api-ssl.bitly.com/v4/bitlinks/'
    split_link = split_url(user_input)
    token = os.environ['BITLY_TOKEN']
    try:
        if is_bitlink(bitlink_url, user_input, split_link, token):
            clicks_count = count_clicks(user_input, bitlink_url, split_link, token)
            print('Колличество кликов по ссылке: ', clicks_count)
        else:
            bitlink = shorten_link(user_input, bitlink_url, token)
            print('Битлинк: ', bitlink)
    except requests.exceptions.HTTPError:
        print('Введена не корректная ссылка')


if __name__ == '__main__':
    main()
