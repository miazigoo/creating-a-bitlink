import argparse
import os

import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def returns_the_received_link():
    """parse link arg"""
    parser = argparse.ArgumentParser(
        description="""Программа создает битлинк. Если это битлтнк - сколько кликов по ней было.""")
    parser.add_argument('link', nargs='?', help='Введите сылку: ')
    link = parser.parse_args().link

    return link


def split_parse_url(user_input):
    """finding the link path"""
    split_url = urlparse(user_input)
    split_link = f'{split_url.netloc}{split_url.path}'
    return split_link


def shorten_link(user_input, url, token):
    """creating a bitlink"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    long_link = {"long_url": user_input}
    post_response = requests.post(url, headers=headers, json=long_link)
    post_response.raise_for_status()
    bit_link = post_response.json()['link']
    return bit_link


def count_clicks(user_input, url, parsed, token):
    """get the number of clicks on the bitlink"""
    headers = {
        'Authorization': f'Bearer {token}'
    }
    get_response = requests.get(f'{url}{parsed}/clicks/summary',
                                headers=headers)
    get_response.raise_for_status()

    clicks_count = get_response.json()["total_clicks"]
    return clicks_count


def is_bitlink(url, user_input, parsed, token):
    """Checking on bitlink"""
    headers = {
        'Authorization': f'Bearer {token}'
    }
    get_response = requests.get(f'{url}{parsed}',
                                headers=headers)
    return get_response.ok


def main():
    load_dotenv()
    user_input = returns_the_received_link()
    bitlink_url = 'https://api-ssl.bitly.com/v4/bitlinks/'
    split_link = split_parse_url(user_input)
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
