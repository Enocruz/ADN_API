import json
import pytest
from src.handler import handler

api_calls = [
    (
        {
            "httpMethod": "POST",
            "body": json.dumps(
                {"dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]}
            ),
            "resource": "/mutation",
        },
        {"statusCode": 200},
    ),
    (
        {
            "httpMethod": "POST",
            "body": json.dumps(
                {"dna": ["ATGCGA", "CAGTGC", "TTATTT", "AGACGG", "GCGCTA", "TCACTG"]}
            ),
            "resource": "/mutation",
        },
        {"statusCode": 403},
    ),
    (
        {
            "httpMethod": "POST",
            "body": json.dumps(
                {"dna": ["AAAAAA", "CAGTGC", "TTATTT", "AGACGG", "GCGCTA", "TCACTG"]}
            ),
            "resource": "/mutation",
        },
        {"statusCode": 403},
    ),
    (
        {
            "httpMethod": "POST",
            "body": json.dumps(
                {"dna": ["AAAAAA", "AAAAAA", "AAAAAA", "AAAAAA", "AAAAAA", "AAAAAA"]}
            ),
            "resource": "/mutation",
        },
        {"statusCode": 200},
    ),
    (
        {
            "httpMethod": "DELETE",
            "body": json.dumps(
                {"dna": ["AAAAAA", "AAAAAA", "AAAAAA", "AAAAAA", "AAAAAA", "AAAAAA"]}
            ),
            "resource": "/mutation",
        },
        {"statusCode": 404},
    ),
    (
        {
            "httpMethod": "PATCH",
            "body": json.dumps({"dna": [""]}),
        },
        {"statusCode": 404},
    ),
    (
        {
            "httpMethod": "PUT",
            "body": json.dumps({"dna": ["AAAAA"]}),
        },
        {"statusCode": 404},
    ),
]


class TestIntegration:
    @pytest.mark.parametrize("test_input", api_calls)
    def test_handler_response(self, test_input):
        api_call, expected_response = test_input
        response = handler(event=api_call, context=None)
        assert response == expected_response
        assert isinstance(response, dict)
