import json
from mutation import has_mutation
from stats import update_stats, get_stats, insert_dna, get_dna

MUTATION_RESOURCE = "/mutation"
STATS_RESOURCE = "/stats"


def simple_response(status_code: int) -> dict:
    """
    Returns status code to API GW
    """
    return {"statusCode": status_code}


def response(status_code: int, body: dict) -> dict:
    """
    Returns status code and body to API GW
    """
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
    """
    Function that handles POST /mutation API CALL
    Receives a body string and gets the dna from dynamo,
    otherwise calculates and stores the result
    """
    dict_body = json.loads(body).get("dna", None)

    if not dict_body:
        return response(status_code=404, body={"message": "Missing dna body"})
    dna_found = get_dna(dict_sequence=dict_body)

    # None means that the item was not found
    if dna_found != None:
        status_code = 200 if dna_found else 403
        return simple_response(status_code=status_code)

    has_mutation_response = has_mutation(dna_sequence=dict_body)
    insert_dynamo_response = insert_dna(
        dict_sequence=dict_body, has_mutation=has_mutation_response
    )
    print(f"Sequence inserted: {insert_dynamo_response}")

    if insert_dynamo_response.get("status") == "OK":
        dynamo_response = update_stats(has_mutation=has_mutation_response)
        print(f"Stats updated: {dynamo_response}")

    status_code = 200 if has_mutation_response else 403
    return simple_response(status_code=status_code)


def handle_stats():
    """
    Function that handles GET /stats API CALL
    Makes a query to dynamo to return the current stats
    """
    dynamo_response = get_stats()
    return response(status_code=200, body=dynamo_response)
