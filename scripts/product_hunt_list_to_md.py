import os

# from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta, timezone
from openai import OpenAI
from bs4 import BeautifulSoup
import pytz

# 加載 .env 文件
# load_dotenv()

# 創建 OpenAI 客戶端實例
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

producthunt_client_id = os.getenv("PRODUCTHUNT_CLIENT_ID")
producthunt_client_secret = os.getenv("PRODUCTHUNT_CLIENT_SECRET")
product_hunt_token = os.getenv("PRODUCT_HUNT_TOKEN")


class Product:
    def __init__(
        self,
        id: str,
        name: str,
        tagline: str,
        description: str,
        votesCount: int,
        createdAt: str,
        featuredAt: str,
        website: str,
        url: str,
        **kwargs,
    ):
        self.name = name
        self.tagline = tagline
        self.description = description
        self.votes_count = votesCount
        self.created_at = self.convert_to_beijing_time(createdAt)
        self.featured = "是" if featuredAt else "否"
        self.website = website
        self.url = url
        self.og_image_url = self.fetch_og_image_url()
        self.keyword = self.generate_keywords()
        self.translated_tagline = self.translate_text(self.tagline)
        self.translated_description = self.translate_text(self.description)

    def fetch_og_image_url(self) -> str:
        """獲取產品的Open Graph圖片URL"""
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            og_image = soup.find("meta", property="og:image")
            if og_image:
                return og_image["content"]
        return ""

    def generate_keywords(self) -> str:
        """生成產品的關鍵詞，顯示在一行，用逗號分隔"""
        prompt = f"根據以下內容生成適合的中文關鍵詞，用英文逗號分隔開：\n\n產品名稱：{self.name}\n\n標語：{self.tagline}\n\n描述：{self.description}"

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Generate suitable Chinese keywords based on the product information provided. The keywords should be separated by commas.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=50,
                temperature=0.7,
            )
            keywords = response.choices[0].message.content.strip()
            if "," not in keywords:
                keywords = ", ".join(keywords.split())
            return keywords
        except Exception as e:
            print(f"Error occurred during keyword generation: {e}")
            return "無關鍵詞"

    def translate_text(self, text: str) -> str:
        """使用OpenAI翻譯文本內容"""
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "你是世界上最專業的翻譯工具，擅長英文和中文互譯。你是一位精通英文和中文的專業翻譯，尤其擅長將IT公司黑話和專業詞彙翻譯成簡潔易懂的地道表達。你的任務是將以下內容翻譯成流暢的繁體中文，風格與科普雜誌或日常對話相似。",
                    },
                    {"role": "user", "content": text},
                ],
                max_tokens=500,
                temperature=0.7,
            )
            translated_text = response.choices[0].message.content.strip()
            return translated_text
        except Exception as e:
            print(f"Error occurred during translation: {e}")
            return text

    def convert_to_beijing_time(self, utc_time_str: str) -> str:
        """將UTC時間轉換為台灣時間"""
        utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")
        beijing_tz = pytz.timezone("Asia/Taipei")
        beijing_time = utc_time.replace(tzinfo=pytz.utc).astimezone(beijing_tz)
        return beijing_time.strftime("%Y年%m月%d日 %p%I:%M (台灣時間)")

    def to_markdown(self, rank: int) -> str:
        """返回產品數據的Markdown格式"""
        og_image_markdown = f"![{self.name}]({self.og_image_url})"
        return (
            f"## [{rank}. {self.name}]({self.url})\n"
            f"**標語**：{self.translated_tagline}\n"
            f"**介紹**：{self.translated_description}\n"
            f"**產品網站**: [立即訪問]({self.website})\n"
            f"**Product Hunt**: [View on Product Hunt]({self.url})\n\n"
            f"{og_image_markdown}\n\n"
            f"**關鍵詞**：{self.keyword}\n"
            f"**票數**: 🔺{self.votes_count}\n"
            f"**是否精選**：{self.featured}\n"
            f"**發佈時間**：{self.created_at}\n\n"
            f"---\n\n"
        )

    # def get_producthunt_token():
    """通過 client_id 和 client_secret 獲取 Product Hunt 的 access_token"""
    url = "https://api.producthunt.com/v2/oauth/token"
    # payload = {
    #     "client_id": producthunt_client_id,
    #     "client_secret": producthunt_client_secret,
    #     "grant_type": "client_credentials",
    # }

    # headers = {
    #     "Content-Type": "application/json",
    # }

    # response = requests.post(url, json=payload, headers=headers)

    # if response.status_code != 200:
    #     raise Exception(
    #         f"Failed to obtain access token: {response.status_code}, {response.text}"
    #     )

    # token = response.json().get("access_token")
    # return token


def fetch_product_hunt_data():
    """從 Product Hunt 取得取前一天的Top 30數據"""
    token = product_hunt_token
    print(product_hunt_token)
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    date_str = yesterday.strftime("%Y-%m-%d")
    url = "https://api.producthunt.com/v2/api/graphql"
    headers = {"Authorization": f"Bearer {token}"}

    base_query = """
    {
      posts(order: VOTES, postedAfter: "%sT00:00:00Z", postedBefore: "%sT23:59:59Z", after: "%s") {
        nodes {
          id
          name
          tagline
          description
          votesCount
          createdAt
          featuredAt
          website
          url
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
    """

    all_posts = []
    has_next_page = True
    cursor = ""

    while has_next_page and len(all_posts) < 30:
        query = base_query % (date_str, date_str, cursor)
        response = requests.post(url, headers=headers, json={"query": query})

        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch data from Product Hunt: {response.status_code}, {response.text}"
            )

        data = response.json()["data"]["posts"]
        posts = data["nodes"]
        all_posts.extend(posts)

        has_next_page = data["pageInfo"]["hasNextPage"]
        cursor = data["pageInfo"]["endCursor"]

    # 只保留前30個產品
    return [
        Product(**post)
        for post in sorted(all_posts, key=lambda x: x["votesCount"], reverse=True)[:30]
    ]


def generate_markdown(products, date_str):
    """生成Markdown內容並保存到data目錄"""
    # 獲取今天的日期並格式化
    today = datetime.now(timezone.utc)
    date_today = today.strftime("%Y-%m-%d")

    markdown_content = f"# 今日熱門榜單 | {date_today}\n\n"
    for rank, product in enumerate(products, 1):
        markdown_content += product.to_markdown(rank)

    # 確保 data 目錄存在
    os.makedirs("data", exist_ok=True)

    # 修改文件保存路徑到 data 目錄
    file_name = f"data/producthunt-daily-{date_today}.md"

    # 如果文件存在，直接覆蓋
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(markdown_content)
    print(f"文件 {file_name} 產生成功並更新。")


def main():
    # 獲取昨天的日期並格式化
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    date_str = yesterday.strftime("%Y-%m-%d")

    # 獲取Product Hunt數據
    products = fetch_product_hunt_data()

    # 生成Markdown文件
    generate_markdown(products, date_str)


if __name__ == "__main__":
    main()
