import requests
import datetime
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
day_before_yesterday = yesterday - datetime.timedelta(days=1)


# Gathering News Data

def news_data():
    news_params = {
        "q": "Tesla",
        "from": yesterday,
        "sortBy": "popularity",
        "apikey": "01ab9db590194e688f6a844cfc1125f3"
    }
    url = "https://newsapi.org/v2/everything"

    response = requests.get(url=url, params=news_params)
    news_data = response.json()
    return news_data

# Tracking the Stock

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": "EH6W1INPGHHAD6DL"
}
url = 'https://www.alphavantage.co/query'
data = requests.get(url=url, params=params).json()
time_series_data = data["Time Series (Daily)"]
yesterday_data = time_series_data[f"{yesterday}"]["1. open"]
day_before_yesterday_data = time_series_data[f"{day_before_yesterday}"]["1. open"]

Percentage_Change = ((float(yesterday_data) - float(day_before_yesterday_data)) / float(
    day_before_yesterday_data)) * 100


# Configuring Twilio to send sms updates
if Percentage_Change >= 5:
    data = news_data()
    headline = data["articles"][0]["title"]
    brief = data["articles"][0]["content"]
    print(headline)
    print(brief)

account_sid = "AC63f919d11afd5c70ffc6f27c3bf39e15"
auth_token = "bb7b95390da997ff37c04635842bbffe"  # os.environ.get("AUTH_TOKEN")

client = Client(account_sid, auth_token)
message = client.messages \
    .create(
    body=f"Headline: {headline}\nBrief: {brief}",
    from_="+16592772178",
    to="+917277679361"
)
