import requests
import datetime
import time
import email.message
import smtplib

my_email = "[]"
password = "[]"

MESSAGE = email.message.EmailMessage()
MESSAGE['Subject'] = 'The ISS is above you'
MESSAGE['From'] = '[]'
MESSAGE['To'] = '[]'
MESSAGE.set_content(f"The ISS is above you")
parameters = {
    "lat": 28.144270,
    "lng": -82.379850,
    "formatted": 0
}
cool_down = 0
while True:
    time.sleep(5)
    if cool_down >= 0:
        cool_down -= 1
    print(cool_down)
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    data = response.json()
    current_hour = datetime.datetime.now().time().hour
    sunrise = data['results']['sunrise']
    sunset = data['results']['sunset']
    sunrise_hour = (int(sunrise.split('T')[1].split(':')[0]) - 4) % 24
    sunset_hour = (int(sunset.split('T')[1].split(':')[0]) - 4) % 24
    if sunrise_hour > current_hour or current_hour > sunset_hour:
        iss_location = requests.get("http://api.open-notify.org/iss-now.json").json()
        longitude = iss_location["iss_position"]["longitude"]
        latitude = iss_location["iss_position"]["latitude"]
        print(abs(float(latitude) - parameters["lat"]))
        print(abs(float(longitude) - parameters["lng"]))
        if abs(float(latitude) - parameters["lat"]) < 4 and abs(float(longitude) - parameters["lng"]) < 4 \
                and cool_down < 1:
            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.send_message(MESSAGE)
            connection.close()
            cool_down = 1000
