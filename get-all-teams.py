import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'nba-db' 
    
    table = dynamodb.Table(table_name)
    
    try:
        response = table.scan(ProjectionExpression='teamName')
        
        teamNames = [item['teamName'] for item in response.get('Items', [])]

        res_body = {
            'allTeams': teamNames
        }

        http_res = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(res_body)
        }

        return http_res
    except Exception as e:
        http_res = {
            'statusCode': 500,  # Internal Server Error
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': "Failure"})
        }

        return http_res
