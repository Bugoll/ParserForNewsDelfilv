import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

seed = "https://rus.delfi.lv/57859/daily"


def get_page_content(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    
    title = soup.find("title").get_text(strip=True) if soup.find("title") else ""
    img_tag = soup.find("img", class_="headline__image")
    img = img_tag["src"] if img_tag and "src" in img_tag.attrs else ""
    author = soup.find("h3", class_="text-dark-grey").text if soup.find("h3", class_="text-dark-grey") else ""
    
    date_tag = soup.find("time", class_="col text-end text-dark-grey text-size-8")  # Используем тег <time>, который содержит дату и время
    date_text = date_tag.get_text(strip=True).split()[0] if date_tag else ""  # Извлекаем только дату (YYYY-MM-DD)
    date_pub = datetime.strptime(date_text, "%d.%m.%Y").strftime("%Y-%m-%d") if date_text else ""
    time_text = date_tag.get_text(strip=True).split()[1] if date_tag else ""
    time_pub = datetime.strptime(time_text, "%H:%M:%S").strftime("%H:%M") if time_text else "" 
    body = [p.get_text(strip=True) for p in soup.find_all('p')]

    page_info = {
        "url": link,  # ссылка на новость
        "title": title,  # заголовок новости
        "img":  img,  # ссылка на изображение
        "body": " ".join(body), # текст новости
        "author": author,  # автор новости (если указывается)",
        "date": date_pub, # дата публикации новости в формате YYYY-MM-DD
        "time": time_pub, # время публикации новости в формате HH:MM
    }
   
    return page_info


def get_links():
    r = requests.get(seed)
    soup = BeautifulSoup(r.content, "html.parser")
    articles = soup.find_all("article", class_="headline")
    news_urls = [article.a["href"] for article in articles]
     
    return news_urls
 

def main():
    links = get_links()
    top_news = []
    for link in links:
        print(f"Processing {link}")
        info = get_page_content(link)
        top_news.append(info)
    with open("rus-delfi-lv.json", "wt", encoding='utf-8') as write_file:
        json.dump(top_news, write_file, ensure_ascii=False, indent=4)
        print("Done!")

# Главная функция
if __name__ == "__main__":
    main()