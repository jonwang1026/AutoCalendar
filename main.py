import requests, schedule, time
from twilio.rest import Client
import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import auth_info
from Get_Calender import *
scopes = ['https://www.googleapis.com/auth/calendar.readonly']


def send_message():
    account_sid = auth_info.account_sid
    token = auth_info.auth_token
    receiver_number = auth_info.receiver_number
    sender_number = auth_info.sender_number

    client = Client(account_sid, token)
    message = client.messages.create(
        to = receiver_number,
        from_= sender_number,
        body = "testing program")


get_service = prompt_login()
event_list = get_calender_events(get_service)
timed_dict = {}
untimed_dict = {}

for key in event_list:
    match_time = re.findall("\d[T]\d", event_list.get(key))
    if match_time:
        timed_dict[key] = event_list.get(key)
    else:
        untimed_dict[key] = event_list.get(key)
print(timed_dict)
print("untimed...")
print(untimed_dict)




"""change start to the key/value
hour_before =
schedule.every().day.get.at(day_start).do(send_message)
while True:
    #need to fix later to check if there is an event in the next hour
    schedule.run_pending()
    time.sleep(2)"""