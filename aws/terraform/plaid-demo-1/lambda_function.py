import os
import sys
import boto3
import datetime
import json

parent_dir = os.path.abspath(os.path.dirname(__file__))
lib_dir = os.path.join(parent_dir, 'lib')

sys.path.append(lib_dir)

import plaid

def lambda_handler(event, context):
    ssm = boto3.client('ssm', 'us-west-2')
    response = ssm.get_parameters_by_path(Path='/plaid',WithDecryption=True)

    for item in response['Parameters']:
        if item['Name'] == '/plaid/client_id':
            client_id = item['Value']
        elif item['Name'] == '/plaid/secret':
            secret = item['Value']
        elif item['Name'] == "/plaid/public_key":
            public_key = item['Value']

    client = plaid.Client(client_id=client_id, secret=secret,
                      public_key=public_key, environment="development")

    response = ssm.get_parameter(Name='/plaid-demo/user-4947192/access_token/acct-6535023',WithDecryption=True)
    access_token = response['Parameter']['Value']

    start_date = "{:%Y-%m-%d}".format(datetime.datetime.now() + datetime.timedelta(-30))
    end_date = "{:%Y-%m-%d}".format(datetime.datetime.now())

    transactions = client.Transactions.get(access_token, start_date, end_date)
    return transactions
