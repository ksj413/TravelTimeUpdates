import os
import requests
from twilio.rest import Client
import schedule
import time

def send():
    r = requests.get('https://maps.googleapis.com/maps/api/directions/json?'
            + 'origin=place_id:' + os.environ['GOOGLE_MAPS_ORIGIN_ID'] +'&destination=place_id:' + os.environ['GOOGLE_MAPS_DESTINATION_ID']
            + '&avoid=tolls&key=' + os.environ["GOOGLE_MAPS_API_KEY"])

    result = r.json()
    travel_time = result['routes'][0]['legs'][0]['duration']['text']

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    account_auth_token = os.environ["TWILIO_AUTH_TOKEN"]

    client = Client(account_sid, account_auth_token)

    client.messages.create(
        to=os.environ["MY_TWILIO_NUMBER"],
        from_=os.environ["TWILIO_NUMBER"],
        body=travel_time)

schedule.every().day.at("08:00").do(send)

while True:
    schedule.run_pending()
    time.sleep(1)
