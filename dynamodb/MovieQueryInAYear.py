from __future__ import print_function  # Python 2/3 compatibility

import decimal
import json

import boto3
from boto3.dynamodb.conditions import Key


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

table = dynamodb.Table('Movies')

print("Movies from 2015")

response = table.query(
    KeyConditionExpression=Key('year').eq(2015)
)

for i in response['Items']:
    print(i['year'], ":", i['title'])
