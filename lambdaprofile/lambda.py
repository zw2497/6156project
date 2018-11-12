import json
import boto3
import jwt
from boto3.dynamodb.conditions import Key, Attr

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
    errorno["statusCode"] = str(number)
    return errorno

def headerCheck(event):
    try:
        if "headers" in event:
            if "credentials" in event["headers"]:
                return True
    except:
        return False

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        if not headerCheck(event):
            return error(403)
        
        auth_header = event["headers"]["credentials"]
        try:
            payload = jwt.decode(auth_header, 'dev', algorithms='HS256')
        except:
            return error(401)
        else:
            user_id = payload["user_id"]
            client = boto3.resource('dynamodb')
            table = client.Table("61562")
            res = table.get_item(
                                 Key={
                                 'id': user_id
                                 }
                                 )
                                 if 'Item' not in res:
                                     return response("no profile")
                                 return response(str(res['Item']))

if event['httpMethod'] == 'POST':
    if not headerCheck(event):
        return error(403)
        
        auth_header = event["headers"]["credentials"]
        
        try:
            payload = jwt.decode(auth_header, 'dev', algorithms='HS256')
        except:
            return error(401)
    else:
        user_id = payload["user_id"]
        client = boto3.resource('dynamodb')
        table = client.Table("61562")
        item = {}
            item["id"] = int(payload["user_id"])
            item["profile"] = event["body"]
            res = table.put_item(Item = item)
            return response("success add")
