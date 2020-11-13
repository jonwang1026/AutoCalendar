import requests, schedule, time
from twilio.rest import Client
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import auth_info

scopes = ['https://www.googleapis.com/auth/calendar.readonly']


account_sid = auth_info.account_sid
token = auth_info.auth_token
receiver_number = auth_info.receiver_number
sender_number = auth_info.sender_number

client = Client(account_sid, token)
message = client.messages.create(
    to = receiver_number,
    from_= sender_number,
    body = "testing program"
)