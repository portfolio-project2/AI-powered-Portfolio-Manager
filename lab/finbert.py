import feedparser
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# Load FinBERT model and tokenizer
MODEL_NAME = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Define RSS Feeds
rss_feeds = {
    "Yahoo Finance": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=TSLA&region=US&lang=en-US",
    "Google Finance": "https://news.google.com/rss/search?q=Tesla+stock"
}

# Function to fetch news headlines
def fetch_news():
    all_news = []
    
    for source, rss_url in rss_feeds.items():
        print(f"\n🔹 Fetching news from {source}...\n")
        
        # Parse RSS feed
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

# Function to analyze sentiment using FinBERT
def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs).logits
    probabilities = softmax(outputs.numpy()[0])

    # FinBERT class order: Neutral, Positive (Bullish), Negative (Bearish)
    labels = ["Neutral ⚪", "Bullish 🟢", "Bearish 🔴"]
    sentiment = labels[probabilities.argmax()]
    
    return sentiment, probabilities

# Fetch news headlines
news_list = fetch_news()

# Analyze sentiment for each headline
for news in news_list:
    sentiment, confidence = analyze_sentiment(news["title"])
    
    print(f"📌 Source: {news['source']}")
    print(f"Title: {news['title']}")
    print(f"Published: {news['published']}")
    print(f"URL: {news['url']}")
    print(f"Sentiment: {sentiment} (Confidence: {max(confidence):.2f})\n")
