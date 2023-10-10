import json
from bs4 import BeautifulSoup
import requests
import boto3



URL = "https://www.basketball-reference.com/boxscores/"

def getGames(soup, dynamodb):
    gamesSoup= soup.find_all('div', class_="game_summary")
    gamesPlayed = []


    for i in gamesSoup:
        game = {
            "homeTeam": "",
            "awayTeam": "",
            "homeScore": "",
            "awayScore": ""
        }
        awayTeam = i.find('td').text

        winner = i.find('tr', class_="winner")
        winnerTeam = winner.a.text
        winnerScore = winner.find('td', class_='right').text
        # print(winnerScore)

        loser = i.find('tr', class_="loser")
        loserTeam = loser.a.text
        loserScore = loser.find('td', class_='right').text
        # print(loserScore)

        if winnerTeam == awayTeam:
            game["homeTeam"] = loserTeam
            game["homeScore"] = loserScore
            game["awayTeam"] = winnerTeam
            game["awayScore"] = winnerScore
            updateRecordAwayWin(game, dynamodb)
        elif loserTeam == awayTeam:
            game["homeTeam"] = winnerTeam
            game["homeScore"] = winnerScore
            game["awayTeam"] = loserTeam 
            game["awayScore"] = loserScore
            updateRecordHomeWin(game, dynamodb)

        gamesPlayed.append(game)
        
            
    return gamesPlayed
            
def homeWon(teamName, dynamodb):
    attribute_to_increment = 'Home_Win'
    
    existingTeam = dynamodb.get_item(TableName=tableName,Key={'teamName': teamName})
        
    if 'Item' in existingTeam:
        update_expression = f"SET {attribute_to_increment} = {attribute_to_increment} + :increment_value"
        expression_attribute_values = {':increment_value': 1}
        response = dynamodb.update_item(
            TableName='nba-db',
            Key={'teamName': teamName},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
        )
    else: 
        response = dynamodb.put_item(
            TableName='nba-db',
            Item={
                'teamName':teamName,
                'Home_Win':1,
                'Home_Loss':0,
                'Away_Win':0,
                'Away_Loss':0
            }
            )
    
    
        

def homeLoss(teamName, dynamodb):
    attribute_to_increment = 'Home_Loss'
    
    existingTeam = dynamodb.get_item(
        TableName='nba-db',
        Key={'teamName': teamName})
        
    if 'Item' in existingTeam:
        update_expression = f"SET {attribute_to_increment} = {attribute_to_increment} + :increment_value"
        expression_attribute_values = {':increment_value': 1}
        response = dynamodb.update_item(
            TableName='nba-db',
            Key={'teamName': teamName},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
        )
    else: 
        response = dynamodb.put_item(
            TableName='nba-db',
            Item={
                'teamName':teamName,
                'Home_Win':0,
                'Home_Loss':1,
                'Away_Win':0,
                'Away_Loss':0
            }
            )
    
def awayWon(teamName, dynamodb):
    attribute_to_increment = 'Away_Win'
    
    existingTeam = dynamodb.get_item(
        TableName='nba-db',
        Key={'teamName': teamName})
        
    if 'Item' in existingTeam:
        update_expression = f"SET {attribute_to_increment} = {attribute_to_increment} + :increment_value"
        expression_attribute_values = {':increment_value': 1}
        response = dynamodb.update_item(
            TableName='nba-db',
            Key={'teamName': teamName},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
        )
    else: 
        response = dynamodb.put_item(
            TableName='nba-db',
            Item={
                'teamName':teamName,
                'Home_Win':0,
                'Home_Loss':0,
                'Away_Win':1,
                'Away_Loss':0
            }
            )

def awayLoss(teamName, dynamodb):
    attribute_to_increment = 'Away_Loss'
    
    existingTeam = dynamodb.get_item(
        TableName='nba-db',
        Key={'teamName': teamName})
        
    if 'Item' in existingTeam:
        update_expression = f"SET {attribute_to_increment} = {attribute_to_increment} + :increment_value"
        expression_attribute_values = {':increment_value': 1}
        response = dynamodb.update_item(
            TableName='nba-db',
            Key={'teamName': teamName},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
        )
    else: 
        response = dynamodb.put_item(
            TableName='nba-db',
            Item={
                'teamName':teamName,
                'Home_Win':0,
                'Home_Loss':0,
                'Away_Win':0,
                'Away_Loss':1
            }
            )


def updateRecordAwayWin(game, dynamodb): 
    awayWon(game['awayTeam'],dynamodb)
    homeLoss(game['homeTeam'], dynamodb)
    
def updateRecordHomeWin(game, dynamodb):
    homeWon(game['homeTeam'], dynamodb)
    awayLoss(game['awayTeam'], dynamodb)  
    
    
def lambda_handler(event, context):
    
    table = dynamodb.Table(tableName)
    
    boxscores = requests.get(URL)
    mainSoup = BeautifulSoup(boxscores.text.encode(), "html.parser")
    
    result = getGames(mainSoup, table)
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }

