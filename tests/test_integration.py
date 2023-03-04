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

api_calls_found_dna = [
    (
        {
            "httpMethod": "POST",
            "resource": "/mutation",
            "body": json.dumps(
                {"dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]}
            ),
        },
        True,
        {"statusCode": 200},
    ),
    (
        {
            "httpMethod": "POST",
            "resource": "/mutation",
            "body": json.dumps(
                {"dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]}
            ),
        },
        False,
        {"statusCode": 403},
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
    def test_handler_response_post_new_dna(self, test_input):
        with patch("src.handler.get_dna", return_value=None), patch(
            "src.handler.insert_dna", return_value=self.dynamo_mock
        ), patch("src.handler.update_stats", return_value=self.dynamo_mock):
            api_call, expected_response = test_input
            response = handler(event=api_call, context=None)
            assert response == expected_response
            assert isinstance(response, dict)

    @pytest.mark.parametrize("test_input", api_calls_found_dna)
    def test_handler_response_post_existing_dna(self, test_input):
        api_call, get_dna_mock, expected_response = test_input
        with patch("src.handler.get_dna", return_value=get_dna_mock):
            response = handler(event=api_call)
            assert response == expected_response
            assert isinstance(response, dict)

    def test_handler_response_get(self):
        with patch("src.handler.get_stats", return_value=self.stats_mock):
            api_call, expected_response = self.test_get_input
            response = handler(event=api_call, context=None)
            assert response == expected_response
            assert isinstance(response, dict)
            assert response.get("body") == self.stats_mock
