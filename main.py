import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv

api_key = os.getenv("API_KEY")

MY_LAT = os.getenv("MY_LAT")
MY_LONG = os.getenv("MY_LONG")

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")

params = {
  "lat": MY_LAT,
  "lon": MY_LONG,
  "appid": api_key,
  "exclude": "current,minutely,daily",
}

response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False
condition_code = 0

for hour_data in weather_slice:
  cc = int(hour_data["weather"][0]["id"])
  
  if cc < 700:
    will_rain = True
    condition_code = cc

if will_rain == True:
  
  client = Client(account_sid, auth_token)
  message = client.messages \
              .create(
                    body=f"It's going to rain today. Remember to bring your umbrella! ☂️",
                    from_="+18145463433",
                    to="+19706890661"
                )
  print(message.status)
