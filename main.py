# -*- coding: utf-8 -*-
import time
from datetime import datetime
import requests
import pytz
import traceback
import os
import logging
import requests
from requests.exceptions import RequestException

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_res():
    logging.info('开始获取数据')
    current_time = int(round(time.time() * 1000))
    url = 'https://www.jisilu.cn/webapi/cb/pre/?history=N?t={}'.format(current_time)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
    }
    res = requests.post(url, headers=headers)
    if res.status_code != 200:
        logging.error('数据获取失败')
        raise Exception('数据获取失败')
    data = res.json()
    logging.info('获取可转债数据数量:{}'.format(len(data['data'])))
    logging.info('数据获取成功')
    return data

def make_info(data, today):
    logging.info('开始处理数据')
    data = [x for x in data['data'] if x['progress_dt'] == today.strftime('%Y-%m-%d') and x['apply_date'] == today.strftime('%Y-%m-%d')]
    result = [x['bond_nm'] for x in data]
    logging.info("今日可申购可转债数量:{}".format(len(result)))
    logging.info('数据处理完成')
    return result

def make_msg(data):
    logging.info('开始生成消息')
    msg = u'今日可申购{}只可转债:{}'.format(len(data), ','.join(data)) if data else ''
    logging.info('消息生成完成')
    return msg

def send_msg(token, content):
    logging.info('开始发送消息')
    logging.info('消息token:{}'.format(token))
    logging.info('消息内容:{}'.format(content))
    url = u'https://api.day.app/{}/可转债打新提醒/{}'.format(token, content)
    logging.info('消息发送url:{}'.format(url))
    retries = 3
    for attempt in range(retries):
        try:
            res = requests.get(url)
            res.raise_for_status()
            logging.info('消息发送状态码:{}'.format(res.status_code))
            logging.info('消息发送结果:{}'.format(res.text))
            logging.info('消息发送完成')
            return
        except RequestException as e:
            logging.info('消息发送状态码:{}'.format(res.status_code))
            logging.info('消息发送结果:{}'.format(res.text))
            logging.error('消息发送失败: {}'.format(str(e)))
            if attempt < retries - 1:
                logging.info('重试第 {} 次'.format(attempt + 1))
            else:
                raise Exception('消息发送失败')

if __name__ == '__main__':
    token = os.environ.get('BARK_TOKEN')
    beijing_tz = pytz.timezone('Asia/Shanghai')
    today = datetime.now(beijing_tz)
    # today = datetime.strptime('2023-12-29', '%Y-%m-%d')

    try:
        logging.info('开始主程序')
        data = get_res()  # 获取数据
    except:
        logging.error('可转债接口请求出错')
        send_msg(token, u'可转债接口请求出错')
        quit()

    try:
        processed_data = make_info(data, today)  # 处理数据
    except:
        logging.error('数据处理出错')
        traceback.print_exc()
        send_msg(token, u'数据处理出错')
        quit()

    if processed_data:
        msg = make_msg(processed_data)  # 生成消息字符串
        send_msg(token, msg)  # 发送消息
    logging.info('主程序执行完成')
