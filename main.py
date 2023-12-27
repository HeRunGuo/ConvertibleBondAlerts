# -*- coding: utf-8 -*-
import time
from datetime import datetime
import requests
import pytz
import traceback
import os


def get_res():
    """
    获取数据

    Returns:
        dict: 包含数据的字典对象
    """
    current_time = int(round(time.time() * 1000))
    url = 'https://www.jisilu.cn/webapi/cb/pre/?history=N?t={}'.format(
        current_time)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
    }
    res = requests.post(url, headers=headers)
    return res.json()


def make_info(data, today):
    """
    从给定的数据中提取当天的信息。

    参数：
    data (dict): 包含数据的字典。
    today (datetime.datetime): 当天的日期。

    返回值：
    list: 包含当天信息的列表。
    """
    data = [x for x in data['data'] if x['progress_dt'] == today.strftime('%Y-%m-%d') and x['apply_date'] == today.strftime('%Y-%m-%d')]
    result = [x['bond_nm'] for x in data]
    return result


def make_msg(data):
    """
    生成消息字符串。

    Args:
        data (list): 可转债数据列表。

    Returns:
        str: 消息字符串，如果data为空则返回空字符串。
    """
    msg = u'[可转债打新提醒]:今日可申购{}只可转债:{}'.format(len(data), ','.join(data)) if data else ''
    return msg


def send_msg(token, content):
    """
    发送消息。

    Args:
        token (str): 消息推送的令牌。
        content (str): 消息内容。
    """
    url = u'https://api.day.app/{}/可转债提醒/{}'.format(token, content)
    requests.get(url)


if __name__ == '__main__':
    token = os.environ.get('BARK_TOKEN')
    beijing_tz = pytz.timezone('Asia/Shanghai')
    today = datetime.now(beijing_tz)

    try:
        data = get_res()  # 获取数据
    except:
        send_msg(token, u'可转债接口请求出错')
        quit()

    try:
        processed_data = make_info(data, today)  # 处理数据
    except:
        traceback.print_exc()
        send_msg(token, u'[可转债打新提醒]:数据处理出错')
        quit()

    msg = make_msg(processed_data)  # 生成消息字符串
    if msg:
        send_msg(token, msg)  # 发送消息
