import os
import smtplib
import requests
from email.message import EmailMessage


API_KEY = os.environ.get("OPENWEATHER_API_KEY")
CITY = "Palakkad"

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

try:
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temp = data["main"]["temp"]
        weather_condition = data["weather"][0]["main"].lower()
        description = data["weather"][0]["description"]

        print(f"Current temperature in {CITY}: {temp}°C, Condition: {description}")

        is_hot = temp > 35
        is_raining = "rain" in weather_condition or "drizzle" in weather_condition

        if True:
            subject = f"⚠️ Weather Alert for {CITY}!"
            body = f"Alert conditions met!\n\nTemperature: {temp}°C\nCondition: {description.capitalize()}\n\nStay safe!"
            
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = SENDER_EMAIL
            msg["To"] = RECEIVER_EMAIL
            msg.set_content(body)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(SENDER_EMAIL, EMAIL_PASSWORD)
                smtp.send_message(msg)
            
            print("Alert email sent successfully!")
        else:
            print("Weather is normal. No alert needed.")
    else:
        print(f"Failed to fetch data: {data.get('message')}")

except Exception as e:
    print(f"An error occurred: {e}")