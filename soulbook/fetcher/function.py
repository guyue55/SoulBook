#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""

import os
import random
import time

import aiofiles
import aiohttp
import arrow
import async_timeout
import cchardet
import requests

from urllib.parse import urlparse

from soulbook.config import LOGGER, CONFIG
from soulbook.fetcher.novels_factory.ssl_factory import ssl_gen


async def _get_data(filename, default='') -> list:
    """
    Get data from a file
    :param filename: filename
    :param default: default value
    :return: data
    """
    root_folder = os.path.dirname(os.path.dirname(__file__))
    user_agents_file = os.path.join(
        os.path.join(root_folder, 'data'), filename)
    try:
        async with aiofiles.open(user_agents_file, mode='r') as f:
            data = [_.strip() for _ in await
            f.readlines()]
    except:
        data = [default]
    return data


async def get_random_user_agent() -> str:
    """
    Get a random user agent string.
    :return: Random user agent string.
    """
    return random.choice(await _get_data('user_agents.txt', CONFIG.USER_AGENT))


def get_time() -> str:
    utc = arrow.utcnow()
    local = utc.to(CONFIG.TIMEZONE)
    time = local.format("YYYY-MM-DD HH:mm:ss")
    return time


def get_timestamp() -> float:
    return time.time()


def get_netloc(url):
    """
    获取netloc
    :param url: 
    :return:  netloc
    """
    netloc = urlparse(url).netloc
    return netloc or None


def get_scheme(url):
    """
    获取scheme
    :param url:
    :return:  scheme
    """
    netloc = urlparse(url).scheme
    return netloc or None


async def target_fetch(url, headers, timeout=15):
    """
    :param url: target url
    :return: text
    """
    async with async_timeout.timeout(timeout):
        try:
            async with aiohttp.ClientSession() as client:
                # async with client.get(url, headers=headers) as response:
                async with client.get(url, headers=headers, ssl=ssl_gen()) as response:
                    assert response.status == 200
                    LOGGER.info('Task url: {}'.format(response.url))
                    try:
                        text = await response.text()
                    except:
                        try:
                            text = await response.read()
                        except aiohttp.ServerDisconnectedError as e:
                            LOGGER.exception(e)
                            text = None
                    return text
        except Exception as e:
            LOGGER.exception(str(e))
            return None


def get_html_by_requests(url, headers, timeout=15):
    """
    :param url:
    :return:
    """
    try:
        response = requests.get(url=url, headers=headers, verify=False, timeout=timeout)
        response.raise_for_status()
        content = response.content
        charset = cchardet.detect(content)
        text = content.decode(charset['encoding'])
        return text
    except Exception as e:
        LOGGER.exception(e)
        return None
