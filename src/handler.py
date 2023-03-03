import json
from src.mutation import has_mutation
from src.stats import update_stats, get_stats, insert_dna

MUTATION_RESOURCE = "/mutation"
STATS_RESOURCE = "/stats"


def simple_response(status_code: int) -> dict:
    return {"statusCode": status_code}


def response(status_code: int, body: dict) -> dict:
    return {"statusCode": status_code, "body": body}


def handler(event, context=None):
    try:
        method = event.get("httpMethod")
        resource = event.get("resource")
        json_body = event.get("body")
        if method == "POST" and resource == MUTATION_RESOURCE:
            return handle_mutation(body=json_body)
        elif method == "GET" and resource == STATS_RESOURCE:
            return handle_stats()
        else:
            return simple_response(status_code=404)
    except Exception as e:
        print(e)
        return simple_response(status_code=500)


def handle_mutation(body: str):
    dict_body = json.loads(body).get("dna", None)

    if not dict_body:
        return response(status_code=404, body={"message": "Missing dna body"})

    has_mutation_response = has_mutation(dna_sequence=dict_body)
    insert_dynamo_response = insert_dna(dict_sequence=dict_body)
    print(f"Sequence inserted: {insert_dynamo_response}")

    if insert_dynamo_response.get("status") == "OK":
        dynamo_response = update_stats(has_mutation=has_mutation_response)
        print(f"Stats updated: {dynamo_response}")

    status_code = 200 if has_mutation_response else 403
    return simple_response(status_code=status_code)


def handle_stats():
    dynamo_response = get_stats()
    return response(status_code=200, body=dynamo_response)
