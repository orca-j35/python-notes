import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pprint import pprint

base_url = 'https://www.zhihu.com/'
seed_url = urljoin(base_url, 'explore')
headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}

resp = requests.get(seed_url, headers=headers)
soup = BeautifulSoup(resp.text, 'lxml')

href_regex = re.compile(r'^/question/\d*/answer')
link_set = set()
for a_tag in soup.find_all('a', {'href': href_regex}):
    href = a_tag.attrs['href']
    full_url = urljoin(base_url, href)
    link_set.add(full_url)

print('Total %d question pages found.' % len(link_set))
pprint(link_set)
'''Out:
Total 13 question pages found.
{'https://www.zhihu.com/question/274765997/answer/681777503',
 'https://www.zhihu.com/question/274765997/answer/711290759',
 'https://www.zhihu.com/question/312092758/answer/681756749',
 'https://www.zhihu.com/question/320932685/answer/681784892',
 'https://www.zhihu.com/question/32313367/answer/711651328',
 'https://www.zhihu.com/question/324110344/answer/681825350',
 'https://www.zhihu.com/question/324119156/answer/681845106',
 'https://www.zhihu.com/question/32489241/answer/712402812',
 'https://www.zhihu.com/question/325144561/answer/711363253',
 'https://www.zhihu.com/question/328063582/answer/711408993',
 'https://www.zhihu.com/question/328779709/answer/711415682',
 'https://www.zhihu.com/question/328843561/answer/712802363',
 'https://www.zhihu.com/question/328855314/answer/712755745'}
'''
