import os
import markdown
import requests
from datetime import datetime, timezone

def publish_to_slack():
    slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')

    # 获取今天的日期并格式化
    today = datetime.now(timezone.utc)
    date_today = today.strftime('%Y-%m-%d')

    # 获取最新的Markdown文件内容
    file_name = f'data/producthunt-daily-{date_today}.md'
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File not found: {file_name}")
        return

    # 去掉第一行的大标题
    lines = content.splitlines()
    if lines and lines[0].startswith('#'):
        lines = lines[1:]
    content_without_title = '\n'.join(lines)

    # 将Markdown内容转换为HTML
    html_content = markdown.markdown(content_without_title)

    # 获取文件中的第一行作为标题
    title = content.splitlines()[0].strip('#').strip()

    # 构建Slack消息数据
    slack_data = {
        'text': f"*{title}*\n{html_content}"
    }

    # 发送POST请求到Slack webhook URL
    response = requests.post(slack_webhook_url, json=slack_data)

    # 检查响应状态
    if response.status_code == 200:
        print("Message posted to Slack successfully.")
    else:
        print(f"Failed to post message to Slack: {response.status_code}, {response.text}")

if __name__ == "__main__":
    publish_to_slack()
