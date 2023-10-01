import requests
from datetime import datetime
import smtplib
import time

my_email = "tedmbangudemy@gmail.com"
app_password = "gyqwqlwobzfktjrh"  # fill the password for the email here
MY_LAT = 3.839258
MY_LONG = 11.482464


response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


# Your position is within +5 or -5 degrees of the ISS position.
def is_iss_close(lat, long, iss_lat, iss_long):
    return abs(lat - iss_lat) <= 5 and abs(long - iss_long) <= 5


# Function to check if it's currently dark at your location
def is_dark(local_sunrise, local_sunset, current_time):
    # returns true if it's the day
    # return local_sunrise <= current_time < local_sunset
    # returns true if it's night
    return not (local_sunrise <= current_time < local_sunset)


# Function to send an email
def send_email(address, subject, msg):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()  # encryption
        connection.login(user=my_email, password=app_password)
        connection.sendmail(from_addr=my_email, to_addrs=f"{address}", msg=f"Subject:{subject} \n\n{msg}")


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

time_now = datetime.now().hour

while True:
    # Wait for 60 seconds before the next check
    time.sleep(60)
    if is_iss_close(lat=MY_LAT, long=MY_LONG, iss_lat=iss_latitude, iss_long=iss_longitude) and is_dark(local_sunrise=sunrise, local_sunset=sunset, current_time=time_now):
        send_email(address="tdark237@gmail.com", subject="Look up!", msg="The ISS is passing by your location")
