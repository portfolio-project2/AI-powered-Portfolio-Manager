import yfinance as yf

# Define the stock symbol (Example: Tesla - TSLA)
ticker = "TSLA"

# Fetch historical data (last 1 year)
stock_data = yf.download(ticker, period="1y", interval="1d")




# Get stock information
stock = yf.Ticker("TSLA")

# Fetch Balance Sheet
balance_sheet = stock.balance_sheet
print("Balance Sheet:\n", balance_sheet)

# Fetch Income Statement
income_statement = stock.financials
print("Income Statement:\n", income_statement)

# Fetch Cash Flow Statement
cash_flow = stock.cashflow
print("Cash Flow Statement:\n", cash_flow)

# Fetch latest stock-related news
news = stock.news
for article in news[:5]:  # Show first 5 news articles
    print(f"Title: {article['title']}")
    print(f"Published: {article['providerPublishTime']}")
    print(f"URL: {article['link']}\n")
