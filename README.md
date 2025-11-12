# goldpapers
# 📘 OpenAlex Paper Scraper & PDF Merger - Algomoneyfest.com

This single Python project automates the process of downloading **open-access academic papers from OpenAlex** and **merging them into one PDF file**.

## 🚀 Quick Start
pip install requests beautifulsoup4 tqdm PyPDF2
python openalexscraper.py
cd openalex_papers
python ../merger.py

## ⚙️ Features
- Queries the OpenAlex API for open-access papers.
- Detects direct and embedded PDF links automatically.
- Extracts PDF links from HTML landing pages using BeautifulSoup.
- Displays tqdm progress bars during downloads.
- Skips duplicates and sanitizes filenames.
- Merges all PDFs alphabetically into merged_books.pdf.

## 🧩 Configuration
In `openalexscraper.py`, edit:
QUERY = "title_and_abstract.search:gold+forecast,primary_topic.id:t11326,open_access.is_oa:true"
Modify this query to your topic. See OpenAlex API filters for examples.

## 🧰 Requirements
- Python 3.8+
- Libraries: requests, beautifulsoup4, tqdm, PyPDF2

## 📄 Example Output
🔎 Página 1
⬇️ Downloading: Gold price forecasting using deep learning
✅ Saved: openalex_papers/Gold_price_forecasting_using_deep_learning.pdf
Agregando: Paper_01.pdf
✅ all PDFs merged here: merged_books.pdf

## 📜 License
Free for educational and research use. Attribution appreciated. - I am just a magical student. Follow me on X: Amoneyfest

