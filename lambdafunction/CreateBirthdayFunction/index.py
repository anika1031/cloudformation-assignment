import json
import boto3
import uuid
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    try:
        # Handle different event formats
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
        
        # Validate required fields
        if 'name' not in body:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Methods': '*'
                },
                'body': json.dumps({'error': 'Missing required field: name'})
            }
        
        if 'birthDate' not in body:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Methods': '*'
                },
                'body': json.dumps({'error': 'Missing required field: birthDate'})
            }
        
        # Prepare the item for DynamoDB
        item = {
            "personId": body.get("personId", str(uuid.uuid4())),
            "name": body["name"],
            "birthDate": body["birthDate"]
        }
        
        # Add optional fields if they exist
        if "email" in body:
            item["email"] = body["email"]
        if "phone" in body:
            item["phone"] = body["phone"]
        
        # Save to DynamoDB
        table.put_item(Item=item)
        
        # Return success response
        return {
            'statusCode': 201,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': json.dumps({
                'message': 'Birthday added successfully',
                'personId': item['personId']
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': json.dumps({'error': str(e)})
        }
