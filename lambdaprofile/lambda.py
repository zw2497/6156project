import json
import boto3
import jwt
from boto3.dynamodb.conditions import Key, Attr


response = {
    'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": '*'},
    "statusCode": 200,
    "body":{"code" : 1}
}

def error(number):
    error = {
        'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": '*'},
        "body":{"code" : 0}
    }
    error["statusCode"] = number
    return error

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
            return error()
                auth_header = event["headers"]["credentials"]
                if (auth_header):
                    try:
                        payload = jwt.decode(auth_header, 'dev', algorithms='HS256')
                    except:
                        return {"statusCode": 200,
                            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": '*'},
                            "body": json.dumps("invalid token")
                        }
                    else:
                        user_id = payload["user_id"]
                        status = payload["status"]
                        client = boto3.resource('dynamodb')
                        table = client.Table("6156")
                        response = table.get_item(
                                        Key={
                                            'id': user_id,
                                            'status': str(status)
                                        }
                                    )
                        if 'Item' not in response:
                            return {
                                "statusCode": '200',
                                "headers": { "Access-Control-Allow-Origin": "*"},
                                "body": json.dumps("no profile1")
                            }
                        return {"statusCode": '200',
                        'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"},
                            "body": str(response['Item'])
                        }
            else:
                return {
                        "statusCode": '200',
                        "headers": { "Access-Control-Allow-Origin": "*"},
                        "body": json.dumps("no profile2")
                }

        else:
            return {
                "statusCode": 200,
               'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": '*'},
                "body": json.dumps("No headers")
            }
    return {
            "statusCode": 200,
           'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": '*'},
            "body": json.dumps("No data")
        }

    if event['httpMethod'] == 'POST':
        if "headers" in event:
            if "credentials" in event["headers"]:
                auth_header = event["headers"]["credentials"]
                if (auth_header):
                    try:
                        payload = jwt.decode(auth_header, 'dev', algorithms='HS256')
                    except:
                        return {"statusCode": 200,
                        'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": '*'},
                            "body": "invalid token"
                        }
                    else:
                        user_id = payload["user_id"]
                        client = boto3.resource('dynamodb')
                        table = client.Table("6156")
                        item = {}
                        item["id"] = int(payload["user_id"])
                        item["status"] = str(payload["status"])
                        item["profile"] = json.loads(event["body"])
                        response = table.put_item(Item = item)
                        return {"statusCode": 200,
                                'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": '*'},
                                "body": "add success"
                        }
            else:
                return {
                "statusCode": 200,
                'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": '*'},
                "body": json.dumps("No Authorization")
            }

        else:
            return {
                "statusCode": 200,
                'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": '*'},
                "body": event["body"]
            }
    return {
        "statusCode": 200,
        'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": '*'},
        "body": json.dumps("No Authorization")
    }
