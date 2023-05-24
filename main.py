import os
import argparse
from urllib.parse import urlparse
import requests
from dotenv import load_dotenv
load_dotenv()


def is_bitlink(url, token):
    headers = {
        'Authorization': token
    }
    parsed_url = urlparse(url)
    response = requests.get('https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'.format(bitlink=f"{parsed_url.netloc}{parsed_url.path}"), headers=headers)
    return response.ok


def shorten_link(token, link):
    headers = {
        'Authorization': token
    }
    
    payload = {
        'long_url': link
    }
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, link):
    headers = {
        'Authorization': token
    }
    parsed_link = urlparse(link)
    clicks_count = requests.get('https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'.format(bitlink=f"{parsed_link.netloc}{parsed_link.path}"), headers=headers)
    clicks_count.raise_for_status()
    return clicks_count.json()['total_clicks']


def main():
    token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser(description='переделывает ссылки в битлинки и считает количество переходов по битлинкам')
    parser.add_argument('link_or_bitlink', help='link or bitlink')
    args = parser.parse_args()
    link = args.link_or_bitlink
    try:
        if is_bitlink(link, token):
            print(count_clicks(token, link))
        else:
            print('Битлинк', shorten_link(token, link))
    except requests.exceptions.HTTPError:
        print("Вы ввели неправильную ссылку.")

if __name__ == '__main__':
    main()
