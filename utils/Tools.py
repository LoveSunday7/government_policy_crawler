from .settings import KEY_MAP
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import re
from bs4 import BeautifulSoup
from time import sleep

class Information:
    title:str
    publisher:str
    time:str
    content:str
    attachment_links:dict
    file_path:str
    file_class:str

    def __init__(self, title:str, publisher:str, time:str, content:str, attachment_links:dict, file_class:str):
        self.title = title
        self.publisher = publisher
        self.time = time
        self.content = content
        self.attachment_links = attachment_links
        self.file_class = file_class
        self.file_path = file_class+f"/{self.title}.txt"

    def write_to_file(self):
        print(f"[file]: 正在写入文件：{self.file_path}")
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write("="*20+'\n')
                f.write(f"标题：{self.title}\n")
                f.write("="*20+'\n')
                f.write(f"发布时间：{self.time}\n")
                f.write("="*20+'\n')
                f.write(f"来源：{self.publisher}\n")
                f.write("="*20+'\n')
                f.write(f"正文：\n{self.content}\n")
                f.write("="*20+'\n')
                f.write(f"附件：\n")
                count = 1
                for key in self.attachment_links:
                    f.write(f"{count}:{key}\n")
                    count += 1
                f.write("="*20+'\n')
                f.write("\n")
        except Exception as e:
            print(f"[file]: 写入文件失败：{self.file_path}，原因：{e}")
        print(f"[file]: 写入文件成功：{self.file_path}")

    def download_attachment(self):
        print(f"[file]: 开始下载附件")
        for key in self.attachment_links:
            try:

                print(f"[file]: 正在下载附件：{key}")
                url = self.attachment_links[key]
                response = requests.get(url)

                # 判断一key中有没有后缀名，如果没有则用key+url的后缀名
                if '.' not in key:
                    
                    key += '.'+url.split('.')[-1]

                with open(self.file_class+f"/附件/{key}", 'wb') as f:
                    f.write(response.content)
                print(f"[file]: 下载附件：{key} 成功")
            except Exception as e:
                print(f"[file]: 下载附件：{key} 失败，原因：{e}")

        print(f"[file]: 下载附件结束")

def check_ok(driver:WebDriver,xpath:str,time=1):
    print("[driver]: 等待页面加载",end="",flush=True)
    while True:
        try:
            print("\r[driver]: 等待页面加载...",end="",flush=True)
            count = driver.find_element(By.XPATH, xpath).text
            print(f"\r[driver]: 页面加载完成，共有{count}条搜索结果")
            return int(count)
        except:
            sleep(time)
            print("\r[driver]: 等待页面加载",end="",flush=True)

def search_keywords(SearchBox:WebElement):
    for key1 in KEY_MAP:
        for key2 in KEY_MAP[key1]:
            for key3 in KEY_MAP[key1][key2]:
                # 删除搜索框中的内容
                # 确保搜索框删除完毕
                while True:
                    sleep(1)
                    try:
                        SearchBox.send_keys(Keys.BACKSPACE)
                        SearchBox.clear()
                        SearchBox.clear()
                        SearchBox.clear()
                        if SearchBox.get_attribute('value') == '':
                            break
                    except Exception as e:
                        print(f"[search]: 清除搜索框失败，原因{e}，睡眠1s重新清除")
                
                # 输入关键字并回车搜索
                SearchBox.send_keys(key3) # key3
                SearchBox.send_keys(Keys.ENTER)
                # 返回关键词目录
                print(f"[search]: 搜索关键字：{key1}->{key2}->{key3} 成功")
                yield f"./农业分类目录/{key1}/{key2}/{key3}"

def search_keywords_by_url(driver:WebDriver,url:str):
    for key1 in KEY_MAP:
        for key2 in KEY_MAP[key1]:
            for key3 in KEY_MAP[key1][key2]:
                # 在当前页面打开url
                driver.get(url+ key3)
                # 返回关键词目录
                print(f"[search]: 搜索关键字：{key1}->{key2}->{key3} 成功")
                yield f"./农业分类目录/{key1}/{key2}/{key3}"

def parse_html(html_content):
    """
    更高级的解析方法，尝试从多个位置提取信息
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    result = {
        'title': '',
        'pub_date': '',
        'content_source': '',
        'content': ''
    }
    
    # 从script变量中提取信息
    scripts = soup.find_all('script')
    for script in scripts:
        script_text = script.get_text()
        
        # 提取标题
        if 'title = ' in script_text:
            match = re.search(r"title\s*=\s*'([^']+)'", script_text)
            if match:
                result['title'] = match.group(1)
        
        # 提取发布时间
        if 'pubDate = ' in script_text:
            match = re.search(r"pubDate\s*=\s*'([^']+)'", script_text)
            if match:
                result['pub_date'] = match.group(1)
    
    # 从meta标签补充信息
    meta_title = soup.find('meta', {'name': 'ArticleTitle'})
    if meta_title and not result['title']:
        result['title'] = meta_title.get('content', '')
    
    meta_pubdate = soup.find('meta', {'name': 'PubDate'})
    if meta_pubdate and not result['pub_date']:
        result['pub_date'] = meta_pubdate.get('content', '')
    
    meta_source = soup.find('meta', {'name': 'ContentSource'})
    if meta_source:
        result['content_source'] = meta_source.get('content', '')
    
    # 提取正文内容 - 多种方法
    content_methods = [
        # 方法1: 通过id="zoom"
        lambda: soup.find('div', id='zoom'),
        # 方法2: 通过class包含article
        lambda: soup.find('div', class_=re.compile('article')),
        # 方法3: 查找包含正文的div
        lambda: soup.find('div', style=re.compile('min-height'))
    ]
    
    content_div = None
    for method in content_methods:
        content_div = method()
        if content_div:
            break
    
    if content_div:
        # 移除不需要的标签
        for unwanted in content_div.find_all(['script', 'style', 'div', 'span']):
            if unwanted.get('class') and any(cls in ['prevPage', 'nextPage'] for cls in unwanted.get('class', [])):
                unwanted.decompose()
            elif unwanted.name == 'div' and unwanted.get('style') and 'float:right' in unwanted.get('style', ''):
                unwanted.decompose()
        
        # 提取文本内容
        paragraphs = []
        for p in content_div.find_all('p'):
            text = p.get_text(strip=True)
            if text and len(text) > 10:  # 过滤掉太短的文本
                paragraphs.append(text)
        
        # 如果没有找到p标签，直接提取所有文本
        if not paragraphs:
            text = content_div.get_text(separator='\n', strip=True)
            # 分割成段落
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            paragraphs = [line for line in lines if len(line) > 10]
        
        result['content'] = '\n\n'.join(paragraphs)
    
    return result

def parse_article_html(html_content):
    """
    解析HTML页面，提取文章信息,解析新疆的内容
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. 提取标题 - 从多个可能的位置
    title = None
    
    # 首先尝试从<meta name="ArticleTitle">提取
    article_title_meta = soup.find('meta', {'name': 'ArticleTitle'})
    if article_title_meta and article_title_meta.get('content'):
        title = article_title_meta['content']
    else:
        # 从<title>标签提取
        title_tag = soup.find('title')
        if title_tag:
            # 去掉标题中的栏目信息
            title = title_tag.text.split('-')[0].strip()
        else:
            # 从detail-title类提取
            detail_title = soup.find('p', class_='detail-title')
            if detail_title:
                title = detail_title.text.strip()
    
    # 2. 提取发布日期 - 从多个可能的位置
    pub_date = None
    
    # 首先尝试从<meta name="PubDate">提取
    pub_date_meta = soup.find('meta', {'name': 'PubDate'})
    if pub_date_meta and pub_date_meta.get('content'):
        pub_date = pub_date_meta['content']
    else:
        # 从detail-meta-left中的发布时间提取
        detail_meta_left = soup.find('div', class_='detail-meta-left')
        if detail_meta_left:
            spans = detail_meta_left.find_all('span')
            for span in spans:
                if '发布时间：' in span.text:
                    pub_date = span.text.replace('发布时间：', '').strip()
                    break
    
    # 3. 提取文章来源
    content_source = None
    
    # 首先尝试从<meta name="ContentSource">提取
    source_meta = soup.find('meta', {'name': 'ContentSource'})
    if source_meta and source_meta.get('content'):
        content_source = source_meta['content']
    else:
        # 从detail-meta-left中的信息来源提取
        detail_meta_left = soup.find('div', class_='detail-meta-left')
        if detail_meta_left:
            spans = detail_meta_left.find_all('span')
            for span in spans:
                if '信息来源：' in span.text:
                    content_source = span.text.replace('信息来源：', '').strip()
                    break
    
    # 4. 提取正文内容
    content = ''
    detail_content = soup.find('div', class_='detail-content')
    
    if detail_content:
        # 移除不需要的元素
        for element in detail_content.find_all(['script', 'style', 'img', 'a', 'h4']):
            element.decompose()
        
        # 获取所有文本内容
        paragraphs = detail_content.find_all('p')
        if paragraphs:
            for p in paragraphs:
                text = p.get_text(strip=True)
                if text:  # 跳过空段落
                    # 清理文本中的多余空白和特殊字符
                    text = re.sub(r'\s+', ' ', text)
                    content += text + '\n'
        else:
            # 如果没有p标签，直接获取文本
            content = detail_content.get_text(strip=True)
            content = re.sub(r'\s+', ' ', content)
    
    # 清理内容中的特殊HTML字符
    if content:
        content = content.replace('\u00a0', ' ')  # 替换&nbsp;
        content = content.replace('\u3000', ' ')  # 替换中文空格
    
    # 构建结果字典
    result = {
        'title': title or '',
        'pub_date': pub_date or '',
        'content_source': content_source or '',
        'content': content.strip()
    }
    
    return result