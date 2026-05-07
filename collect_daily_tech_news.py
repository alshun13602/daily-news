import requests
from bs4 import BeautifulSoup
from datetime import date
import os

def get_36kr_news():
    url = 'https://36kr.com/newsflashes'
    headers = {"User-Agent": "Mozilla/5.0"}
    news_list = []
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.find_all('div', class_='newsflash-item-title')
        for item in items[:10]:
            news_list.append(item.get_text(strip=True))
    except Exception as e:
        news_list.append(f"36氪抓取失败: {e}")
    return news_list

def get_sina_tech_news():
    url = 'https://tech.sina.com.cn/'
    headers = {"User-Agent": "Mozilla/5.0"}
    news_list = []
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.find_all('h2')
        count = 0
        for item in items:
            a = item.find('a')
            if a and a.get_text():
                news_list.append(a.get_text(strip=True))
                count += 1
            if count >= 10: break
    except Exception as e:
        news_list.append(f"新浪科技抓取失败: {e}")
    return news_list

def get_techcrunch_news():
    url = 'https://techcrunch.com/'
    headers = {"User-Agent": "Mozilla/5.0"}
    news_list = []
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.find_all('a', class_='post-block__title__link')
        for item in items[:10]:
            news_list.append(item.get_text(strip=True))
    except Exception as e:
        news_list.append(f"TechCrunch抓取失败: {e}")
    return news_list

def generate_markdown(news_dict):
    today = date.today().strftime('%Y-%m-%d')
    md = [f'# 每日科技新闻日报 {today}\n']
    for site, news in news_dict.items():
        md.append(f'## {site}\n')
        for n in news:
            md.append(f'- {n}')
        md.append('')
    return '\n'.join(md)

def main():
    news_dict = {
        '36氪快讯': get_36kr_news(),
        '新浪科技': get_sina_tech_news(),
        'TechCrunch': get_techcrunch_news(),
    }
    md_content = generate_markdown(news_dict)
    # 保存为 markdown
    today = date.today().strftime('%Y-%m-%d')
    out_dir = 'daily_reports'
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.join(out_dir, f'daily_news_{today}.md')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"日报已生成: {filename}")

if __name__ == '__main__':
    main()
