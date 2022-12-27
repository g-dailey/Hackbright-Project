

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json

api_file = "sendgrid_api.json"
cred_file = open(api_file, 'r')
cred_json = json.load(cred_file)
sendgrid_api_key = cred_json["sendggrid_api_key"]

# import sendgrid
# import os

# sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('sendgrid_api_key'))
# response = sg.client._("suppression/bounces").get()
# print(response.status_code)
# print(response.body)
# print(response.headers)
message = Mail(
    from_email='gulafroz.test@gmail.com',
    to_emails='gulafroz.test@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(os.environ.get(sendgrid_api_key))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)

