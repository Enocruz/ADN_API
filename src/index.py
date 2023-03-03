import json


def handler(event, context):
    dna_list = event.get("dna")
    print(dna_list)
    return
