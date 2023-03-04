import boto3
from botocore.config import Config
from datetime import datetime
from src.storage import update_dynamo_stats, get_dynamo_stats, insert_dynamo_dna
from typing import List

config = Config(region_name="us-west-2")

dynamo_client = boto3.resource("dynamodb", config=config)

HAS_MUTATION_KEY = "count_mutations"
NO_MUTATION_KEY = "count_no_mutation"
STATS_TABLE_NAME = "DnaStats"
KEY_STATS_TABLE = "StatName"
STATS_FIELD_NAME = "CountOcurrences"
DNA_TABLE_NAME = "DnaStorage"


def update_stats(has_mutation: bool):
    keyValue = HAS_MUTATION_KEY if has_mutation else NO_MUTATION_KEY
    return update_dynamo_stats(
        client=dynamo_client,
        table=STATS_TABLE_NAME,
        key=KEY_STATS_TABLE,
        keyValue=keyValue,
    )


def get_stats():
    stats = get_dynamo_stats(
        client=dynamo_client,
        table=STATS_TABLE_NAME,
        key=KEY_STATS_TABLE,
    )
    items = stats.get("response", {}).get("Items", [])
    response = {}
    for item in items:
        response[item.get(KEY_STATS_TABLE)] = int(item.get(STATS_FIELD_NAME))
    no_mutation_count = response.get(NO_MUTATION_KEY)
    response["ratio"] = float(
        response.get(HAS_MUTATION_KEY) / no_mutation_count if no_mutation_count else 0
    )
    return response


def insert_dna(dict_sequence: List[str]):
    date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    sequence_str = "".join(dict_sequence)
    response = insert_dynamo_dna(
        client=dynamo_client, table=DNA_TABLE_NAME, value=sequence_str, date=date
    )
    return response
