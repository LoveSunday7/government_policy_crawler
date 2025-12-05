# 宜春地区的搜索全是静态页面只需要使用request库
import requests
from utils.settings import *
from utils.Tools import*

# from utils.InitSpider import MakeDir


import re
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from math import ceil

# MakeDir()
def parse_one(html_text: str):
    """
    解析单个页面
    :param html_text: 页面源码
    :param file_name: 文件名（仅用于日志/标识）
    :return: dict
    """
    soup = BeautifulSoup(html_text, "html.parser")

    # 1. 正文：取 class 为 article-content-body 的 div 下纯文本
    content_div = soup.select_one("div.article-content-body")
    content = content_div.get_text(strip=True, separator="\n") if content_div else ""

    # 2. 附件：在 class 为 fj-a 的 div 里找 <a>
    attachments = []
    fj_div = soup.select_one("div.fj-a")
    if fj_div:
        for a in fj_div.find_all("a", href=True):
            # href 可能是相对路径，这里保留原始值，如有需要可自行拼绝对路径
            attachments.append({
                "name": a.get_text(strip=True),
                "url": a["href"]
            })

    return {
        "content": content,
        "attachments": attachments
    }

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

num = 0

if __name__ == '__main__':
    for key1 in KEY_MAP:
            for key2 in KEY_MAP[key1]:
                for key3 in KEY_MAP[key1][key2]:
                    page = 0
                    search_count = 0
                    while True:
                        try:
                            print("[robort]: 正在下载和解析页面")
                            response = requests.get(GOV_LINKS['宜春市农业农村局'].format(key3,page))
                            print("[robort]: 下载页面成功")
                            response.encoding = response.apparent_encoding
                            parsed_data = parse_yichun_search_page(response.content)
                            print("[robort]: 解析页面成功")
                        except Exception as e:
                            print(f"[error]: 页面解析失败，退出程序，错误原因：\n{e}")
                            exit(0)
                        
                        print("[robot]: 正在获取主页面信息")
                        search_count = parsed_data['total_results']
                        for card in parsed_data['news_list']:
                            title = card["title"]
                            date = card["date"]
                            publisher = card["source"]
                            link = card["detail_url"]
                            
                            print("[robot]: 下载详细页面",end="",flush=True)
                            detail_html = requests.get(link)
                            detail_html.encoding = detail_html.apparent_encoding
                            detail_html = detail_html.content
                            print("[robot]: 下载详细页面-----[√]")
                            
                            print("[robot]: 解析详情页面",end="",flush=True)
                            detail = parse_one(detail_html)
                            print("[robot]: 解析详情页面-----[√]")

                            links = {}
                            block= link.split("/")
                            for detail_attachment in detail["attachments"]:
                                if 'http' not in detail_attachment["url"]:
                                    url = f"{block[0]}//{block[2]}/{block[3]}/{block[4]}/{block[5]}/"+detail_attachment["url"]
                                links[detail_attachment["name"]] = url

                            print(links)

                            info = Information(
                                title=title,
                                publisher=publisher,
                                time=date,
                                content=detail['content'],
                                file_class=f'./农业分类目录/{key1}/{key2}/{key3}',
                                attachment_links=links
                            )
                            
                            if len(links) != 0:
                                info.download_attachment()
                            
                            info.write_to_file()

                        page += 1
                        if page == ceil(search_count/10):
                            break           

                        