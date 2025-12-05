# 宜春地区的搜索全是静态页面只需要使用request库
import requests
from utils.settings import *

import re
from bs4 import BeautifulSoup
from typing import List, Dict, Any

def parse_yichun_search_page(html_content: str) -> Dict[str, Any]:
    """
    解析宜春市农业农村局搜索结果页面
    
    Args:
        html_content: HTML页面内容
        
    Returns:
        包含相关结果数量、新闻列表等信息的字典
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    result = {
        'total_results': 0,
        'news_list': []
    }
    
    # 1. 提取相关结果数量
    # 查找包含"相关结果"的文本
    results_div = soup.find('div', class_='results-list')
    if results_div:
        results_text = results_div.get_text(strip=True)
        # 使用正则表达式提取数字
        match = re.search(r'相关结果\s*(\d+)\s*个', results_text)
        if match:
            result['total_results'] = int(match.group(1))
    
    # 2. 提取所有新闻条目
    # 查找所有 class 为 "wordGuide Residence-permit" 的 div
    news_divs = soup.find_all('div', class_='wordGuide Residence-permit')
    
    for news_div in news_divs:
        news_item = {}
        
        # 提取详情页链接和标题
        # 标题在 class 为 "titleFont permitT titleSelf" 的 a 标签中
        title_link = news_div.find('a', class_='titleFont permitT titleSelf')
        if title_link:
            news_item['title'] = title_link.get('title', '').strip()
            news_item['detail_url'] = title_link.get('href', '').strip()
        
        # 如果上面的方法没找到标题，尝试另一种方式
        if not news_item.get('title'):
            title_link = news_div.find('a', class_='permitT')
            if title_link:
                # 获取完整的标题文本（包括span标签内的内容）
                title_text = title_link.get_text(strip=True)
                news_item['title'] = title_text
                news_item['detail_url'] = title_link.get('href', '').strip()
        
        # 提取日期
        # 日期在 class 为 "sourceDateFont" 的 span 标签中
        date_span = news_div.find('span', class_='sourceDateFont')
        if date_span:
            news_item['date'] = date_span.get_text(strip=True)
        
        # 提取栏目信息（可选）
        column_span = news_div.find('span', class_='columnLabel styleColor')
        if column_span:
            news_item['column'] = column_span.get_text(strip=True)
        
        # 提取来源（可选）
        source_link = news_div.find('a', class_='sourceDateFont permitU')
        if source_link:
            news_item['source'] = source_link.get_text(strip=True)
        
        # 提取摘要（可选）
        summary_p = news_div.find('p', class_='summaryFont')
        if summary_p:
            news_item['summary'] = summary_p.get_text(strip=True)
        
        # 只添加有标题和链接的新闻
        if news_item.get('title') and news_item.get('detail_url'):
            result['news_list'].append(news_item)
    
    return result

for key1 in KEY_MAP:
        for key2 in KEY_MAP[key1]:
            for key3 in KEY_MAP[key1][key2]:
                response = requests.get(GOV_LINKS['宜春市农业农村局'].format(key3,0))
                with open("index.html","wb") as file:
                    file.write(response.content)
                     