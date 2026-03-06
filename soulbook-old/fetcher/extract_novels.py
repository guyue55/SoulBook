#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""

import re

from bs4 import BeautifulSoup
from collections import OrderedDict
from operator import itemgetter
from urllib.parse import urljoin, urlparse

from soulbook.config import LOGGER


def extract_chapters(chapters_url, html):
    """
    通用解析小说目录
    :param chapter_url: 小说目录页url
    :param res: 当前页面html
    :return: 
    """
    # 参考https://greasyfork.org/zh-CN/scripts/292-my-novel-reader
    chapters_reg = r'(<a\s+.*?>.*第?\s*[一二两三四五六七八九十○零百千万亿0-9１２３４５６７８９０]{1,6}\s*[章回卷节折篇幕集].*?</a>)'
    # 这里不能保证获取的章节分得很清楚，但能保证这一串str是章节目录。可以利用bs安心提取a
    chapters_res = re.findall(chapters_reg, str(html), re.I)
    str_chapters_res = '\n'.join(chapters_res)
    chapters_res_soup = BeautifulSoup(str_chapters_res, 'html5lib')
    all_chapters = []
    for link in chapters_res_soup.find_all('a'):
        each_data = {}
        url = urljoin(chapters_url, link.get('href')) or ''
        name = link.text or ''
        each_data['chapter_url'] = url
        each_data['chapter_name'] = name
        each_data['index'] = int(urlparse(url).path.split('.')[0].split('/')[-1])
        all_chapters.append(each_data)
    chapters_sorted = sorted(all_chapters, reverse=True, key=itemgetter('index'))
    return chapters_sorted


def extract_pre_next_chapter(url, chapter_url, html):
    """
    获取单章节上一页下一页
    :param chapter_url:
    :param html:
    :return:
    """
    next_chapter = OrderedDict()
    try:
        current_url = url
        next_reg = r'(<a\s+.*?>.*[第上前下后][一]?[0-9]{0,6}?[页张个篇章节步].*?</a>)'
        judge_reg = r'[第上前下后][一]?[0-9]{0,6}?[页张个篇章节步]'
        next_res = re.findall(next_reg, html.replace('<<', '').replace('>>', ''), re.I)
        str_next_res = '\n'.join(next_res)
        next_res_soup = BeautifulSoup(str_next_res, 'html5lib')
        prev_alias = ['上一章', '上一页', '前一章', '上页', '上一节', '上一回']
        next_alias = ['下一章', '下一页', '后一章', '下页', '下一节', '下一回']

        for link in next_res_soup.find_all('a'):
            text = link.text or ''
            text = text.replace(' ', '')
            href = link.get('href') or ''

            if novels_list(text):
                is_next = re.search(judge_reg, text)
                if is_next:
                    if not href or href.startswith('#') or href.lower().startswith('javascript'):
                        continue
                    link_url = urljoin(chapter_url, href) or ''
                    regex = re.compile("^http://|^https://")
                    if link_url.endswith('/'):
                        continue
                    if link_url.endswith('.html') and not re.search(r'/\d+(?:_\d+)?\.html$', link_url):
                        continue
                    if regex.sub('', current_url) == regex.sub('', link_url):
                        link_url = False

                    key = None
                    for k in prev_alias:
                        if k in text:
                            key = '上一章'
                            break
                    if not key:
                        for k in next_alias:
                            if k in text:
                                key = '下一章'
                                break
                    if not key:
                        continue
                    next_chapter[key] = link_url

        if '上一章' not in next_chapter or '下一章' not in next_chapter:
            soup_full = BeautifulSoup(html, 'html5lib')
            prev_a = soup_full.select('a#prev_url')
            next_a = soup_full.select('a#next_url')
            if '上一章' not in next_chapter and prev_a:
                href = prev_a[0].get('href') or ''
                if href and not href.startswith('#') and not href.lower().startswith('javascript'):
                    link_url = urljoin(chapter_url, href)
                    next_chapter['上一章'] = link_url
            if '下一章' not in next_chapter and next_a:
                href = next_a[0].get('href') or ''
                if href and not href.startswith('#') and not href.lower().startswith('javascript'):
                    link_url = urljoin(chapter_url, href)
                    next_chapter['下一章'] = link_url

        return next_chapter
    except Exception as e:
        LOGGER.exception(e)
        return next_chapter


def novels_list(text):
    rm_list = ['后一个', '天上掉下个']
    for i in rm_list:
        if i in text:
            return False
        else:
            continue
    return True
