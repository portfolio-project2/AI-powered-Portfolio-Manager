import feedparser

# Define RSS Feeds
rss_feeds = {
    "Yahoo Finance": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=TSLA&region=US&lang=en-US",
    "Google Finance": "https://news.google.com/rss/search?q=Tesla+stock"
}

# Function to fetch and display news
def fetch_news():
    all_news = []
    
    for source, rss_url in rss_feeds.items():
        print(f"\n🔹 Fetching news from {source}...\n")
        
        # Parse the RSS feed
        feed = feedparser.parse(rss_url)
        
        # Extract first 5 articles
        for entry in feed.entries[:5]:
            news_item = {
                "source": source,
                "title": entry.title,
                "published": entry.published if 'published' in entry else "N/A",
                "url": entry.link
            }
            all_news.append(news_item)
    
    return all_news

# Fetch and print news
news_list = fetch_news()

# Display the news
for news in news_list:
    print(f" Source: {news['source']}")
    print(f"Title: {news['title']}")
    print(f"Published: {news['published']}")
    print(f"URL: {news['url']}\n")
