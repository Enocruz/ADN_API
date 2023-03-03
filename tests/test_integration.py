import json
import pytest
from src.handler import handler
from unittest.mock import patch

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
    dynamo_mock = {"status": "OK", "response": "Success"}
    stats_mock = {"count_no_mutation": 0, "count_mutations": 0, "ratio": 0.0}
    test_get_input = (
        {
            "httpMethod": "GET",
            "resource": "/stats",
        },
        {
            "statusCode": 200,
            "body": stats_mock,
        },
    )

    @pytest.mark.parametrize("test_input", api_calls)
    def test_handler_response_post(self, test_input):
        with patch("src.handler.insert_dna", return_value=self.dynamo_mock), patch(
            "src.handler.update_stats", return_value=self.dynamo_mock
        ):
            api_call, expected_response = test_input
            response = handler(event=api_call, context=None)
            assert response == expected_response
            assert isinstance(response, dict)

    def test_handler_response_get(self):
        with patch("src.handler.get_stats", return_value=self.stats_mock):
            api_call, expected_response = self.test_get_input
            response = handler(event=api_call, context=None)
            assert response == expected_response
            assert isinstance(response, dict)
            assert response.get("body") == self.stats_mock
