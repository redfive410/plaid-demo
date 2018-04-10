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
    response = ssm.get_parameter(Name='/plaid/client_id',WithDecryption=True)
    client_id = response['Parameter']['Value']

    response = ssm.get_parameter(Name='/plaid/secret',WithDecryption=True)
    secret = response['Parameter']['Value']

    response = ssm.get_parameter(Name='/plaid/public_key',WithDecryption=True)
    public_key = response['Parameter']['Value']

    client = plaid.Client(client_id=client_id, secret=secret,
                      public_key=public_key, environment="development")

    response = ssm.get_parameter(Name='/plaid-demo/user-4947192/access_token/acct-6535023',WithDecryption=True)
    access_token = response['Parameter']['Value']

    start_date = "{:%Y-%m-%d}".format(datetime.datetime.now() + datetime.timedelta(-30))
    end_date = "{:%Y-%m-%d}".format(datetime.datetime.now())

    transactions = client.Transactions.get(access_token, start_date, end_date)
    return transactions
