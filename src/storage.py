from botocore.exceptions import ClientError


def update_dynamo_stats(client, table: str, key: str, keyValue: str) -> dict:
    """
    Updates the dynamo given table for the given key where all the stats are stored
    """
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


def get_dynamo_stats(client, table: str) -> dict:
    """
    Gets all the elements from the given table
    """
    try:
        dynamo_tb = client.Table(table)
        response = dynamo_tb.scan()
        return {"status": "OK", "response": response}
    except ClientError as err:
        return {"status": "ERROR", "response": err}


def insert_dynamo_dna(client, table: str, value: str, has_mutation: bool) -> dict:
    """
    Insert the dna sequence into the given table
    """
    try:
        dynamo_tb = client.Table(table)
        response = dynamo_tb.put_item(
            Item={
                "DNA": value,
                "Mutation": has_mutation,
            }
        )
        return {"status": "OK", "response": response}
    except ClientError as err:
        return {"status": "ERROR", "response": err}


def get_dynamo_dna(client, table: str, value: str) -> dict:
    """
    Performs a query to get the dna sequence in the given table
    """
    try:
        dynamo_tb = client.Table(table)
        response = dynamo_tb.get_item(Key={"DNA": value})
        return {"status": "OK", "response": response}
    except ClientError as err:
        return {"status": "ERROR", "response": err}
