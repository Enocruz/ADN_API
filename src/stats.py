import boto3
from botocore.config import Config
from datetime import datetime
from storage import (
    update_dynamo_stats,
    get_dynamo_stats,
    insert_dynamo_dna,
    get_dynamo_dna,
)
from typing import List

config = Config(region_name="us-west-2")

dynamo_client = boto3.resource("dynamodb", config=config)

HAS_MUTATION_KEY = "count_mutations"
NO_MUTATION_KEY = "count_no_mutation"
STATS_TABLE_NAME = "DnaStats"
KEY_STATS_TABLE = "StatName"
STATS_FIELD_NAME = "CountOcurrences"
DNA_TABLE_NAME = "DnaStorage"


def update_stats(has_mutation: bool) -> dict:
    """
    Updates the dynamo table where all the stats are stored
    """
    keyValue = HAS_MUTATION_KEY if has_mutation else NO_MUTATION_KEY
    return update_dynamo_stats(
        client=dynamo_client,
        table=STATS_TABLE_NAME,
        key=KEY_STATS_TABLE,
        keyValue=keyValue,
    )


def get_stats() -> dict:
    """
    Makes a query to dynamo table and builds the stats response dictionary
    Returns:
    """
    stats = get_dynamo_stats(
        client=dynamo_client,
        table=STATS_TABLE_NAME,
    )
    if stats.get("status") == "OK":
        items = stats.get("response", {}).get("Items", [])
        response = {}
        for item in items:
            response[item.get(KEY_STATS_TABLE)] = int(item.get(STATS_FIELD_NAME))
        no_mutation_count = response.get(NO_MUTATION_KEY)
        response["ratio"] = float(
            response.get(HAS_MUTATION_KEY) / no_mutation_count
            if no_mutation_count
            else 0
        )
        return response
    raise Exception("get_stats Exception occurred")


def insert_dna(dict_sequence: List[str], has_mutation: bool) -> dict:
    """
    Converts the list into a string and inserts it to dynamo
    Returns:
        status: Wheter dynamo request was successfull or not
        response: Dynamo response
    """
    sequence_str = "".join(dict_sequence)
    response = insert_dynamo_dna(
        client=dynamo_client,
        table=DNA_TABLE_NAME,
        value=sequence_str,
        has_mutation=has_mutation,
    )
    return response


def get_dna(dict_sequence: List[str]) -> bool:
    """
    Gets and build the dna sequence from dynamo. If no item is found
    this returns None, otherwise return wether the dna sequence has
    a mutation or not
    """
    sequence_str = "".join(dict_sequence)
    dna = get_dynamo_dna(
        client=dynamo_client,
        table=DNA_TABLE_NAME,
        value=sequence_str,
    )
    item = dna.get("response", {}).get("Item", None)
    return item.get("Mutation") if item else item
