# -*- coding:utf-8 -*-
import requests


def translate(string: str):
    data = {
        'doctype': 'json',
        'type': 'AUTO',
        'i': string,
    }
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url, params=data)
    result = r.json()
    translate_result = result['translateResult'][0][0]["tgt"]
    return translate_result


if __name__ == '__main__':
    print(translate(input('Press a word: ')))
