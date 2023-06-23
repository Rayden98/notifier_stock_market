from twilio.rest import Client
from datetime import date, timedelta
import requests

# ---------------------------------- CONSTANTS ------------------------------------#
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHAVANTAGE_KEY = "KEY"
TWILIO_KEY = "KEY"
NEWS_API = "KEY"
today = str(date.today())
yesterday = str(date.today() - timedelta(days=1))
before_yesterday = str(date.today() - timedelta(days=2))
data = None

# ------------------------------- FUNCTIONS --------------------------------------#
def get_trading():
    global percentage
    parameters_alpha = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": "TSLA",
        # "interval": "60min",
        "apikey": ALPHAVANTAGE_KEY,

    }

    url = 'https://www.alphavantage.co/query?'
    r = requests.get(url, parameters_alpha)
    data_trading = r.json()

    price_yesterday = float(data_trading["Time Series (Daily)"][yesterday]["2. high"])
    price_before_yesterday = float(data_trading["Time Series (Daily)"][before_yesterday]["3. low"])

    percentage = price_yesterday - price_before_yesterday

def get_news():
    global data, percentage
    parameters_news = {
        "q": "Tesla",
        "from": yesterday,
        "sort": "relevancy",
        "apikey": NEWS_API,
    }

    url = ('https://newsapi.org/v2/everything?')

    response = requests.get(url, parameters_news)

    data = response.json()

def get_messages():
    account_sid = 'AC22320bb350b73a8c2765a420e0043118'
    auth_token = TWILIO_KEY
    client = Client(account_sid, auth_token)

    for n in range(3):
        global data, percentage
        title = data["articles"][n]["title"]
        description = data["articles"][n]["description"]

        message = client.messages.create(
            from_='+15418978752',
            body=f'TSLA: {int(percentage)}\nHeadline:{title}\nBrief:{description}',
            to='+50372360860'
        )
        print(message.sid)

# ----------------------- GETTING READY ------------------------#
get_trading()

if percentage > 7 or percentage < -7:
    get_news()
    get_messages()