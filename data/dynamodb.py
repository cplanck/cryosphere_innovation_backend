import json
import time
from decimal import Decimal

import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from botocore.exceptions import ClientError


def check_if_dynamodb_table_exists(table_name):
    """
    Check if DynamoDB table exists. Returns True if table exists
    and False if it doesn't.
    """
    dynamodb_client = boto3.client('dynamodb')
    try:
        dynamodb_client.describe_table(TableName=table_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return False
        else:
            print("An error occurred:", e)
            return False


def create_dynamodb_table(table_name):
    """
    Create a DynamoDB table given a table name
    """
    dynamodb_client = boto3.client('dynamodb')

    key_schema = [
        {'AttributeName': 'uniqueID', 'KeyType': 'HASH'}
    ]

    response = dynamodb_client.create_table(
        TableName=table_name,
        AttributeDefinitions=[
            {'AttributeName': 'uniqueID', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST',
        KeySchema=key_schema
    )

    while True:
        response = dynamodb_client.describe_table(TableName=table_name)
        table_status = response['Table']['TableStatus']
        if table_status == 'ACTIVE':
            break
        time.sleep(0.5)  # Wait for 0.5 seconds before checking again

    return response


def delete_dynamodb_table(table_name):
    """
    Delete a DynamoDB table given a table name
    """

    dynamodb_client = boto3.client('dynamodb')
    response = dynamodb_client.delete_table(TableName=table_name)
    return response


def post_data_to_dynamodb_table(table_name, data):
    """
    Add data to a DynamoDb table given data and a table name.
    What type/shape is 'data'? A JSON list of dictionaries?
    """

    data = json.loads(json.dumps(data), parse_float=Decimal)
    serializer = TypeSerializer()
    serialized_data = {key: serializer.serialize(
        value) for key, value in data.items()}

    dynamodb_client = boto3.client('dynamodb')
    response = dynamodb_client.put_item(
        TableName=table_name,
        Item=serialized_data
    )

    return response


def get_data_from_dynamodb(table_name):
    """
    Fetch data from DynamoDB given a table name.
    Currently this also filteres by an IMEI secondary key.
    We should remove this when we define tables based on an identifier
    """

    dynamodb_client = boto3.client('dynamodb')

    try:
        response = dynamodb_client.scan(
            TableName=table_name
        )
        print(response['NextToken'])
        deserializer = TypeDeserializer()
        deserialized_items = []
        for item in response['Items']:
            deserialized_item = {}
            for key, value in item.items():
                deserialized_item[key] = deserializer.deserialize(value)
            deserialized_items.append(deserialized_item)

        for item in deserialized_items:
            for key, value in item.items():
                if isinstance(value, Decimal):
                    item[key] = float(value)

        print(len(deserialized_items))
        return deserialized_items

    except:
        return False

    # try:
    #     deserializer = TypeDeserializer()
    #     response = dynamodb_client.query(
    #         TableName=table_name,
    #         Select='ALL_ATTRIBUTES'  # Adjust the attributes you need to retrieve
    #     )

    #     print(response)
    #     deserialized_items = []
    #     for item in response['Items']:
    #         deserialized_item = {}
    #         for key, value in item.items():
    #             deserialized_item[key] = deserializer.deserialize(value)
    #         deserialized_items.append(deserialized_item)

    #     for item in deserialized_items:
    #         for key, value in item.items():
    #             if isinstance(value, Decimal):
    #                 item[key] = float(value)

    #     print(len(deserialized_items))
    #     return deserialized_items

    # except:
    #     return False
