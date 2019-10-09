import json
import os
import re

import bs4
import requests

header_cookie = ""
group_id = ""
VIDEOS_TXT = group_id+'_videos.txt'
if os.path.isfile('cookies.txt'):
    header_cookie = open('cookies.txt').read().strip()
else:
    print('No cookie')
    input()
    exit(1)
session = requests.Session()
if os.path.isfile(VIDEOS_TXT):
    videos = [i.strip() for i in open(VIDEOS_TXT).readlines()]
else:
    videos = []


def save_videos():
    with open(VIDEOS_TXT, 'w') as fw:
        fw.write('\n'.join(videos))


session.headers = {
    'authority': 'mbasic.facebook.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'dnt': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-language': 'en-US,en;q=0.9,ja;q=0.8,ny;q=0.7',
    'cookie': header_cookie
}
r = re.compile(r'href=(.*multi_permalinks)')
next_page_url = f"https://mbasic.facebook.com/groups/{group_id}"
while True:
    page_content = session.get(next_page_url)
    search = re.search('<a href="([^<]*multi_permalinks&amp;refid=18)', page_content.text)
    if search is None or len(search.groups()) == 0:
        break
    next_page_url = "https://mbasic.facebook.com" + search.groups()[0]
    html = bs4.BeautifulSoup(page_content.text, "html.parser")
    for article in html.select("[role=article]"):
        if r'video_redirect' in str(article) and "data-ft" in article.attrs:
            data = json.loads(article['data-ft'])
            post_id = data['mf_story_key']
            video_url = f"https://www.facebook.com/groups/{group_id}/permalink/{post_id}/"
            if not video_url in videos:
                print('New >>>', video_url)
                videos.append(video_url)
                save_videos()
            else:
                print('Old >>>', video_url)
