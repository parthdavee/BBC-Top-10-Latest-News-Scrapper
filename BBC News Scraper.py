import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup  # Add this import

def get_bbc_news():
    # RSS feed for BBC World News
    url = "http://feeds.bbci.co.uk/news/world/rss.xml"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve BBC News RSS feed")
        return []

    # Parse the XML response
    root = ET.fromstring(response.text)
    
    news_data = []
    for item in root.findall(".//item"):
        title = item.find("title").text
        link = item.find("link").text
        news_data.append({"title": title, "link": link})

        if len(news_data) >= 10:  # Limit to 10 headlines
            break
    
    return news_data

def read_full_article(link):
    response = requests.get(link)
    if response.status_code != 200:
        print("Failed to retrieve the full article")
        return None
    
    # Parse the HTML response and extract the article body
    soup = BeautifulSoup(response.text, "html.parser")
    article_content = soup.find("article")
    if article_content:
        return article_content.text.strip()
    return "Article content not found."

if __name__ == "__main__":
    bbc_news = get_bbc_news()

    if not bbc_news:
        print("No news found.")
    else:
        while True:
            print("\nTop 10 News Headlines from BBC News:")
            for idx, news in enumerate(bbc_news, 1):
                print(f"{idx}. {news['title']}")

            try:
                selected_number = int(input("\nEnter the number of the headline you want to read more about: "))
                if 1 <= selected_number <= len(bbc_news):
                    selected_news = bbc_news[selected_number - 1]
                    print(f"\nYou selected: {selected_news['title']}")
                    full_article = read_full_article(selected_news['link'])
                    if full_article:
                        print(f"\nFull Article:\n{full_article}")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")
                continue
            
            another = input("\nWould you like to read another article? (yes/no): ").strip().lower()
            if another != "yes":
                print("Exiting...")
                break
