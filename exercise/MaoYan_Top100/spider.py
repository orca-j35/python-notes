import requests
import re
import json
import time

TOP_URL = 'http://maoyan.com/board/4?offset='
PATTERN = re.compile(
    r'<dd>\s*<i.*?>(?P<index>\d+)</i>.*?'
    r'<img data-src="(?P<image>.*?)".*?'
    r'<p class="name">.*?title="(?P<title>.*?)".*?'
    r'主演：(?P<actor>.*?)\s*</p>.*?'
    r'上映时间：(?P<time>.*?)</p>.*?'
    r'"integer">(?P<score>\d\.\d)</i>', re.DOTALL)


def get_page(url):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    try:
        with requests.get(url, headers=headers, timeout=1) as r:
            if r.status_code is requests.codes.OK:
                return r.text
            return None
    except requests.RequestException:
        None


def parse_page(text=None):
    if isinstance(text, str):
        text = text.replace('</i><i class="fraction">', '')
        return PATTERN.finditer(text)
    else:
        raise TypeError('text must be a string')


if __name__ == '__main__':
    print('begin')
    for offset in range(0, 100, 10):
        match_iter = parse_page(get_page(f'{TOP_URL}{offset}'))
        with open(
                'result.json', 'w' if offset is 0 else 'a',
                encoding='utf-8') as fin:
            for match_obj in match_iter:
                fin.write(
                    json.dumps(match_obj.groupdict(), ensure_ascii=False) +
                    '\n')
                print(
                    f"{match_obj['index']:2}",
                    end=',' if int(match_obj['index']) % 10 != 0 else '\n')
    # time.sleep(1)
    print('end')