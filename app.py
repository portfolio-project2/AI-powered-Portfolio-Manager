# Install required libraries (run these commands in your environment before running the app)
# pip install streamlit prophet yfinance pandas matplotlib feedparser torch transformers scipy

import streamlit as st
import yfinance as yf
from prophet import Prophet
import matplotlib.pyplot as plt
import feedparser
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# Load FinBERT model once at startup
MODEL_NAME = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Streamlit app configuration
st.set_page_config(page_title="Stock Analysis Suite", layout="wide")
st.title("📈 Stock Prediction & News Sentiment Analysis")

# Sidebar inputs
st.sidebar.header("User Input")
ticker = st.sidebar.text_input("Enter stock ticker symbol (e.g., AAPL):", "AAPL")
years = st.sidebar.slider("Years of historical data:", 1, 10, 5)
forecast_years = st.sidebar.slider("Years to forecast:", 1, 5, 1)

def main():
    if ticker:
        # Stock Prediction Section
        st.header(f"{ticker} Stock Price Prediction")
        
        with st.spinner("Analyzing historical data and generating forecast..."):
            try:
                # Fetch and prepare data
                data = yf.download(ticker, period=f"{years}y")
                df = data.reset_index()[['Date', 'Close']]
                df.columns = ['ds', 'y']

                # Create and fit Prophet model
                m = Prophet(
                    yearly_seasonality=True,
                    weekly_seasonality=True,
                    daily_seasonality=False,
                    changepoint_prior_scale=0.05
                )
                m.add_country_holidays(country_name='US')
                m.fit(df)

                # Generate forecast
                future = m.make_future_dataframe(periods=365 * forecast_years)
                forecast = m.predict(future)

                # Display forecast plot
                fig1 = m.plot(forecast)
                st.pyplot(fig1)

                # Show forecast components
                st.subheader("Forecast Breakdown")
                fig2 = m.plot_components(forecast)
                st.pyplot(fig2)

            except Exception as e:
                st.error(f"Error in stock prediction: {str(e)}")

        # News Analysis Section
        st.header(f"📰 Latest News Sentiment Analysis for {ticker}")
        
        with st.spinner("Scanning financial news and analyzing sentiment..."):
            try:
                # Fetch and analyze news
                news_list = fetch_news(ticker)
                
                if news_list:
                    cols = st.columns(3)
                    for idx, news in enumerate(news_list):
                        sentiment, confidence = analyze_sentiment(news["title"])
                        
                        with cols[idx % 3]:
                            st.markdown(f"### {news['source']}")
                            st.markdown(f"**{news['title']}**")
                            st.caption(f"Published: {news['published']}")
                            
                            # Color-coded sentiment display
                            if "Bullish" in sentiment:
                                st.success(f"{sentiment} ({max(confidence):.0%})")
                            elif "Bearish" in sentiment:
                                st.error(f"{sentiment} ({max(confidence):.0%})")
                            else:
                                st.info(f"{sentiment} ({max(confidence):.0%})")
                            
                            st.markdown(f"[Read Article]({news['url']})")
                            st.markdown("---")
                else:
                    st.warning("No recent news articles found for this ticker")

            except Exception as e:
                st.error(f"Error in news analysis: {str(e)}")

def fetch_news(ticker):
    """Fetch financial news for given ticker from multiple sources"""
    news_items = []
    
    rss_feeds = {
        "Yahoo Finance": f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US",
        "Google Finance": f"https://news.google.com/rss/search?q={ticker}+stock",
        "Reuters": f"https://www.reuters.com/companies/{ticker}/news/rss"
    }
    
    for source, url in rss_feeds.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:  # Get top 3 from each source
            news_items.append({
                "source": source,
                "title": entry.title,
                "published": entry.get('published', 'N/A'),
                "url": entry.link
            })
    
    return news_items

def analyze_sentiment(text):
    """Analyze text sentiment using FinBERT model"""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs).logits
    probs = softmax(outputs.numpy().flatten())
    labels = ["Neutral ⚪", "Bullish 🟢", "Bearish 🔴"]
    return labels[probs.argmax()], probs

if __name__ == "__main__":
    main()