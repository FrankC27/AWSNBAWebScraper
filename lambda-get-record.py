import json
import boto3

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    tableName = 'nba-db'
    table = dynamodb.Table(tableName)

    

    teamName = event["queryStringParameters"]['team']



    # print(f"Team Name: {teamName}")
    
    team_record = table.get_item(TableName=tableName,Key={'teamName': teamName})
    
    res_body = {}

    # print(team_record)
    
    wins = int(team_record['Item']['Home_Win']) + int(team_record['Item']['Away_Win'])
    loses = int(team_record['Item']['Home_Loss']) + int(team_record['Item']['Away_Loss'])
    
    res_body['record'] = { 
                "wins": wins,
                "loses": loses
                }
    print(res_body)
    res_body['homeWL'] = f"{int(team_record['Item']['Home_Win'])}-{int(team_record['Item']['Home_Loss'])}"
    res_body['awayWL'] = f"{int(team_record['Item']['Away_Win'])}-{int(team_record['Item']['Away_Loss'])}"
    

    http_res = {}
    http_res['statusCode'] = 200
    http_res['headers'] = {}
    http_res['headers']['Content-Type'] = 'application/json'

    http_res['body'] = json.dumps(res_body)
    return http_res
