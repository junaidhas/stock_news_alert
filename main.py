import requests
import os

from twilio.rest import Client



STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

Stock_news_api = "196IY9VO32EZN8OY"
NEWS_API_KEY ="e3a1581fa1c44c5d8eff4b12a9606acd"

TWILLIO_SID =os.environ.get("twilio_sid")
TWILLIO_AUTH_TOKEN =os.environ.get("twilio_auth_token")
TWILLIO_Phone_number = "+13613101217"
MY_Phone_number = os.environ.get("my_phone_number")
print(TWILLIO_SID)
print(TWILLIO_AUTH_TOKEN)
print(MY_Phone_number)



    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 1% between yesterday and the day before yesterday then print("Get News").

stock_parameters ={
    "function":"TIME_SERIES_DAILY_ADJUSTED",
    "symbol":STOCK_NAME,
    "apikey":Stock_news_api,
}

response = requests.get(STOCK_ENDPOINT,params=stock_parameters)
data = response.json()["Time Series (Daily)"]

data_list = [value for (key,value) in data.items()]
print(data_list)
yesterday_data = data_list[0]
yesterday_close_data = yesterday_data["4. close"]
print(yesterday_close_data)
# - Get the day before yesterday's closing stock price
daybefore_yesterday_data = data_list[1]
daybefore_yesterday_close_data =daybefore_yesterday_data["4. close"]
print(daybefore_yesterday_close_data)

last_twodays_difference = (float(yesterday_close_data) - float(daybefore_yesterday_close_data))
print(last_twodays_difference)
UP_DOWN = None
if last_twodays_difference > 0:
    UP_DOWN = "⬆"
else:
    UP_DOWN ="⬇"


difference_percentage = (last_twodays_difference/float(yesterday_close_data))*100
difference_percentage = round(difference_percentage,2)
print(difference_percentage)

#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if abs(difference_percentage) >1: # abs function is like modulus operator, gives only the positive value of it 
    print("Get News")

    news_parameters = {
        "apiKey":NEWS_API_KEY,
        "q":STOCK_NAME
    }
        ## STEP 2: https://newsapi.org/
    news_response = requests.get(NEWS_ENDPOINT,news_parameters)
    articles = (news_response.json()["articles"])
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    three_articles = articles[:3]
    print(three_articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.


    #"Headline: {article_title}. \n description:{article description}"
    formatted_messages = [f"TSLA: {UP_DOWN}{difference_percentage} \n Headline: {article['title']}. \n Brief:{article['description']}" for article in three_articles]
    print(formatted_messages)

    for msg in formatted_messages:
        client = Client(TWILLIO_SID,TWILLIO_AUTH_TOKEN)

        message = client.messages.create(
            body=msg,
            from_='+13613101217',
            to=MY_Phone_number
        )



# Formated sms would look like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

