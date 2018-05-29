from __future__ import print_function
import boto3
import json
import decimal

dynamodb = boto3.resource(
    'dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8000')

table = dynamodb.Table('Movies')

with open('moviedata.json') as json_file:
    movies = json.load(json_file, parse_float=decimal.Decimal)
    year = int(movies['year'])
    title = movies['title']
    info = movies['info']

    print("Adding movie:", year, title)

    table.put_item(Item={
        'year': year,
        'title': title,
        'info': info,
    })
