import os
from dotenv import load_dotenv, find_dotenv
import smtplib
import requests
from datetime import datetime

load_dotenv(find_dotenv())

MY_EMAIL = os.environ.get("FROM_ADDR")
PASSWORD = os.environ.get("PASSWORD")
TO_ADDRS = os.environ.get("TO_ADDRS")
MY_LAT = 48.210033
MY_LONG = 16.363449

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
current_hour = time_now.hour

if ((MY_LAT + 5 == iss_latitude or MY_LAT-5 == iss_latitude) and (MY_LONG + 5 == iss_longitude or MY_LONG - 5 == iss_longitude)) and (current_hour >= sunset):
    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=MY_EMAIL, password=PASSWORD)
    connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TO_ADDRS,
            msg=f"Subject:ISS Satellite\n\nGuck mal im Himmel! eine Satellite!"
    )
    connection.close()
