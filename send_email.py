import smtplib
from email.mime.text import MIMEText
from email.header import Header
import json
import sys
from datetime import date

def send_email(subject, content, config):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = Header(config['sender_name'], 'utf-8')
    msg['To'] = Header(config['receiver_name'], 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    try:
        with smtplib.SMTP_SSL(config['smtp_host'], config['smtp_port']) as server:
            server.login(config['smtp_user'], config['smtp_pass'])
            server.sendmail(config['smtp_user'], config['receiver_email'], msg.as_string())
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")

def main():
    today = date.today().strftime('%Y-%m-%d')
    filename = f'daily_reports/daily_news_{today}.md'
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception:
        print("配置文件 config.json 读取失败")
        sys.exit(1)
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        print(f"日报内容文件 {filename} 读取失败")
        sys.exit(1)
    send_email(subject=f'每日科技新闻日报 {today}', content=content, config=config)

if __name__ == '__main__':
    main()
