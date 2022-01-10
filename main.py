import requests
import smtplib
from datetime import datetime
import time

MY_LAT = 23.264600476435948 # Your latitude
MY_LONG = 77.4623531945207 # Your longitude
UTC_OFFSET = 5
MY_EMAIL = "youremail@gmail.com" #Your email this email is not gonna work
MY_PASSWORD = "youremailpassword"  #and Your emails password

# function to convert UTC Hour to IST Hour
def utc_to_local(utc_hour):
    utc_hour += UTC_OFFSET
    if utc_hour > 23:
        utc_hour -= 24
    elif utc_hour < 0:
        utc_hour += 24
    return utc_hour


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True
    else:
        return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = utc_to_local(int(data["results"]["sunrise"].split("T")[1].split(":")[0]))
    sunset = utc_to_local(int(data["results"]["sunset"].split("T")[1].split(":")[0]))

    time_now = datetime.now()
    curr_hour = time_now.hour

    if sunset <= curr_hour <= sunrise:
        return True
    else:
        return False

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="againyouremail@gmail.com",
                msg="Subject:ISS ALERT\n\nISS is up above you go and look."
            )

