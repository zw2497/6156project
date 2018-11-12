import json
import os
import boto3
import send
import jwt

def response(text):
    response = {
        'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": '*'},
        "statusCode": 200,
        "body":{"code" : 1}
    }
    response['body']['body'] = text
    response["body"] = json.dumps(response["body"])
    return response

def error(number):
    errorno = {
        'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": '*'},
        "body":{"code" : 0}
    }
    errorno["statusCode"] = number
    return errorno

def lambda_handler(event, context):
    eb = "http://6156.us-east-2.elasticbeanstalk.com"
    local = "http://localhost:5000"
    if ("MessageAttributes" in event["Records"][0]["Sns"]):
        event = event["Records"][0]["Sns"]["MessageAttributes"]
        if ("email" in event) :
            receiver = event["email"]["Value"]
            print(receiver)
            try:
                payload = {"email": receiver}
                print(payload)
                token = jwt.encode(payload, 'dev', algorithm='HS256')
            except Exception as e:
                return error(401)
            else:
                url = eb + "/auth/confirm?context=" + token.decode()
                send.send(receiver, url)
    else:
        return error(401)
