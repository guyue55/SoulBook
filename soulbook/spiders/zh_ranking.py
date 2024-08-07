#!/usr/bin/env python
"""
 Created by howie.hu at 29/11/2017.
"""
import time

from ruia import Spider, Item, AttrField, HtmlField, TextField
from ruia_ua import middleware

from soulbook.database.mongodb import MotorBaseOld


class RankingItem(Item):
    target_item = TextField(css_select='div.rank_i_p_list')
    ranking_title = TextField(css_select='div.rank_i_p_tit')
    more = AttrField(css_select='div.rank_i_more a', attr='href')
    book_list = HtmlField(css_select='div.rank_i_p_list>div.rank_i_li', many=True)


class NameItem(Item):
    top_name = TextField(css_select='div.rank_i_bname a.rank_i_l_a_book', default='')
    other_name = TextField(css_select='div.rank_i_bname a', default='')


class ZHRankingSpider(Spider):
    start_urls = ['http://book.zongheng.com/rank.html']

    concurrency = 3

    async def parse(self, res):
        result = []
        res_dic = {}

        async for item in RankingItem.get_items(html=res.html):
            each_book_list = []
            # 只取排名前十的书籍数据
            for index, value in enumerate(item.book_list[:10]):
                item_data = await NameItem.get_item(html=value)
                name = item_data.top_name or item_data.other_name
                each_book_list.append({
                    'num': index + 1,
                    'name': name
                })
            data = {
                'title': item.ranking_title,
                'more': item.more,
                'book_list': each_book_list,
                'updated_at': time.strftime("%Y-%m-%d %X", time.localtime()),
            }
            result.append(data)

        res_dic['data'] = result
        res_dic['target_url'] = res.url
        res_dic['type'] = "人气榜单"
        res_dic['spider'] = "zongheng"
        await self.save(res_dic)

    async def save(self, res_dic):
        try:
            motor_db = MotorBaseOld().db
            await motor_db.novels_ranking.update_one({
                'target_url': res_dic['target_url']},
                {'$set': {
                    'data': res_dic['data'],
                    'spider': res_dic['spider'],
                    'type': res_dic['type'],
                    'finished_at': time.strftime("%Y-%m-%d %X", time.localtime())
                }},
                upsert=True)
        except Exception as e:
            self.logger.exception(e)


if __name__ == '__main__':
    ZHRankingSpider.start(middleware=middleware)
