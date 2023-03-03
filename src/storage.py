from botocore.exceptions import ClientError


def update_dynamo_stats(client, table: str, key: str, keyValue: str):
    try:
        dynamo_tb = client.Table(table)
        response = dynamo_tb.update_item(
            Key={key: keyValue},
            UpdateExpression="SET CountOcurrences = CountOcurrences + :inc",
            ExpressionAttributeValues={":inc": 1},
            ReturnValues="UPDATED_NEW",
        )
        return {"status": "OK", "response": response}
    except ClientError as err:
        return {"status": "ERROR", "response": err}


def get_dynamo_stats(client, table: str, key: str):
    try:
        dynamo_tb = client.Table(table)
        response = dynamo_tb.scan()
        return {"status": "OK", "response": response}
    except ClientError as err:
        return {"status": "ERROR", "response": err}


def insert_dynamo_dna(client, table: str, value: str, date: str):
    try:
        dynamo_tb = client.Table(table)
        response = dynamo_tb.put_item(
            Item={
                "DNA": value,
                "CreatedDate": date,
            }
        )
        return {"status": "OK", "response": response}
    except ClientError as err:
        return {"status": "ERROR", "response": err}
