import json
from src.mutation import has_mutation

MUTATION_RESOURCE = "/mutation"
STATS_RESOURCE = "/stats"


def response(status_code: int) -> dict:
    return {"statusCode": status_code}


def handler(event, context=None):
    try:
        method = event.get("httpMethod")
        resource = event.get("resource")
        json_body = event.get("body")
        if method == "POST" and resource == MUTATION_RESOURCE:
            dict_body = json.loads(json_body)
            has_mutation_response = has_mutation(
                dna_sequence=dict_body.get("dna", None)
            )
            status_code = 200 if has_mutation_response else 403
            return response(status_code=status_code)
        elif method == "GET" and resource == STATS_RESOURCE:
            return response(status_code=200)
        else:
            return response(status_code=404)
    except Exception as e:
        print(e)
        return response(status_code=500)
