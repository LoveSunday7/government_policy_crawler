# 政府政策爬虫

## 注意事项

> 开发者请不要上传垃圾文件，开发周期比较紧张，尽量不要浪费时间处理项目文件

## 项目声明

严禁将该爬虫用于非法用途，违法者必受到法律制裁 ！！！

## 项目简介

这是一个用于爬取政府政策信息的网络爬虫程序，能够自动从指定的政府网站抓取最新政策文件、公告通知等相关信息。（下面的说明是乱写的）

## 环境要求

Python 3.8+

火狐驱动 latest

## 安装步骤

1. 克隆项目

```
git clone https://github.com/LoveSunday7/government_policy_crawler.git
cd government-policy-crawler
```

2. 安装依赖（最好使用python虚拟环境）

```
pip install -r requirements.txt
```

3. 运行爬虫（需要完成[安装火狐驱动](https://blog.csdn.net/yinshuilan/article/details/90713084)）

```
python areaname.py
```

## 项目结构

```
government-policy-crawler/
├── utils/           # 爬虫工具模块（如果有新的类别，可以添加文件）
├── 农业分类目录/     # 数据存储目录
├── areaname.py      # 主程序
├── requirements.txt # 依赖列表
└── README.md        # 说明文档
```

## 数据格式

爬取的政策数据包含以下字段：

```
{
    'title': '标题',
    'pub_date': '发布日期',
    'content_source': '文章来源',
    'content': '正文'
}
{附件}
```

## 面临问题

* [ ] 江西省九江市农业局网站链接到的网站页面结构差异很大，无法解析
