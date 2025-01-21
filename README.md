# Product Hunt 每日中文熱榜

[English](README.en.md) | [中文](README.md)

![License](https://img.shields.io/github/license/ViggoZ/producthunt-daily-hot) ![Python](https://img.shields.io/badge/python-3.x-blue)

Product Hunt 每日熱榜是一個基於 GitHub Action 的自動化工具，它能夠每天定時生成 Product Hunt 上的熱門產品榜單 Markdown 文件，並自動提交到 GitHub 倉庫中。該項目旨在幫助用戶快速查看每日的 Product Hunt 熱門榜單，並提供更詳細的產品信息。

榜單會在每天下午4點自動更新，可以在 [🌐 這裡查看](https://decohack.com/category/producthunt/)。

## 預覽

![Preview](./preview.gif)

## 功能概述

- **自動獲取數據**：每天自動獲取前一天的 Product Hunt Top 30 產品數據。
- **關鍵詞生成**：生成簡潔易懂的中文關鍵詞，幫助用戶更好地理解產品內容。
- **高質量翻譯**：使用 OpenAI 的 GPT-4 模型對產品描述進行高質量翻譯。
- **Markdown 文件生成**：生成包含產品數據、關鍵詞和翻譯描述的 Markdown 文件，方便在網站或其他平台上發布。
- **每日自動化**：通過 GitHub Actions 自動生成並提交每日的 Markdown 文件。
- **可配置工作流**：支持手動觸發或通過 GitHub Actions 定時生成內容。
- **靈活定制**：腳本易於擴展或修改，可以包括額外的產品細節或調整文件格式。
- **自動發布到 WordPress**：生成的 Markdown 文件可以自動發布到 WordPress 網站。

## 快速開始

### 前置條件

- Python 3.x
- GitHub 賬戶及倉庫
- OpenAI API Key
- Product Hunt API 憑證
- WordPress 網站及憑證（用於自動發布）

### 安裝

1. **克隆倉庫：**

```bash
git clone https://github.com/ViggoZ/producthunt-daily-hot.git
cd producthunt-daily-hot
```

2. **安裝 Python 依賴：**

確保您的系統已安裝 Python 3.x。然後安裝所需的依賴包：

```bash
pip install -r requirements.txt
```

### 設置

1. **GitHub Secrets：**

   在您的 GitHub 倉庫中添加以下 Secrets：

   - `OPENAI_API_KEY`: 您的 OpenAI API 密鑰。
   - `PRODUCTHUNT_CLIENT_ID`: 您的 Product Hunt API 客戶端 ID。
   - `PRODUCTHUNT_CLIENT_SECRET`: 您的 Product Hunt API 客戶端密鑰。
   - `PAT`: 用於推送更改到倉庫的個人訪問令牌。
   - `WORDPRESS_URL`: 您的 WordPress 網站 URL。
   - `WORDPRESS_USERNAME`: 您的 WordPress 用戶名。
   - `WORDPRESS_PASSWORD`: 您的 WordPress 密碼。

2. **GitHub Actions 工作流：**

   工作流定義在 `.github/workflows/generate_markdown.yml` 和 `.github/workflows/publish_to_wordpress.yml` 中。該工作流每天 UTC 時間 07:01（北京時間 15:01）自動運行，也可以手動觸發。

### 使用

設置完成後，GitHub Action 將自動生成並提交包含 Product Hunt 每日熱門產品的 Markdown 文件，並自動發布到 WordPress 網站。文件存儲在 `data/` 目錄下。

### 自定義

- 您可以修改 `scripts/product_hunt_list_to_md.py` 文件來自定義生成文件的格式或添加額外內容。
- 如果需要，可以在 `.github/workflows/generate_markdown.yml` 中調整定時任務的運行時間。

### 示例輸出

生成的文件存儲在 `data/` 目錄下。每個文件以 `PH-daily-YYYY-MM-DD.md` 的格式命名。

### 貢獻

歡迎任何形式的貢獻！如有任何改進或新功能的建議，請提交 issue 或 pull request。

### 許可證

本項目基於 MIT 許可證開源 - 有關詳細信息，請參閱 [LICENSE](LICENSE) 文件。

