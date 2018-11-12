import json
import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send(receiver, content):
    SENDER = "zhicheng.wu@columbia.edu"
    RECIPIENT = receiver
    AWS_REGION = "us-east-1"
    SUBJECT = "Customer service contact info"
    BODY_TEXT = "Hello World"
    
    BODY_HTML = """\
        <html>
        <head></head>
        <body>
        <h1>Hello!</h1>
        <p>Your confirmation email is %s</p>
        </body>
        </html>
        """ % (content)
    
    CHARSET = "utf-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    msg = MIMEMultipart('mixed')
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = RECIPIENT
    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)
    msg.attach(msg_body)
    try:
        #Provide the contents of the email.
        response = client.send_raw_email(
                                         Source=SENDER,
                                         Destinations=[
                                                       RECIPIENT
                                                       ],
                                         RawMessage={
                                         'Data':msg.as_string(),
                                         }
                                         )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
