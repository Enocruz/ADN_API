import json


def handler(event, context):
    print(event)
    dna_list = event.get("dna")
    print(dna_list)
    return {  # <---- RETURN THIS RIGHT AWAY
        "statusCode": 200,
        "body": json.dumps("Hello from Lambda! Real Test"),
    }
