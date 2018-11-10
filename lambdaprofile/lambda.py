import json
import boto3
import jwt
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        if "headers" in event:
            if "UserAuthorization" in event["headers"]:
                auth_header = event["headers"]["UserAuthorization"]
                if (auth_header):
                    try:
                        payload = jwt.decode(auth_header, 'dev', algorithms='HS256')
                    except:
                        return {"statusCode": 200,
                            "body": "invalid token"
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
                        return {"statusCode": 200,
                            "body": str(response['Item'])
                            }
            else:
                return {
                "statusCode": 200,
                "body": "No Authorization"
    }
        
        else:
            return {
                "statusCode": 200,
                "body": "No headers"
        }
if event['httpMethod'] == 'POST':
    if "headers" in event:
        if "UserAuthorization" in event["headers"]:
            auth_header = event["headers"]["UserAuthorization"]
            if (auth_header):
                try:
                    payload = jwt.decode(auth_header, 'dev', algorithms='HS256')
                    except:
                        return {"statusCode": 200,
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
                            "body": event["body"]
                    }
                            else:
        return {
            "statusCode": 200,
                "body": "No Authorization"
        }
        
        else:
            return {
                "statusCode": 200,
                "body": event["body"]
        }



