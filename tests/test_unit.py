import pytest

from src.mutation import check_sequence, matrix_sequence, has_mutation
from typing import List

dna_sequences = [
    ("ATGCGA", False),
    ("CAGTGC", False),
    ("TTATGT", False),
    ("AGAAGG", False),
    ("CCCCTA", True),
    ("TCACTG", False),
]

string_to_matrix = [
    (["AT", "TA"], [["A", "T"], ["T", "A"]]),
    ([], []),
    (["TAT", "CCC", "TGA"], [["T", "A", "T"], ["C", "C", "C"], ["T", "G", "A"]]),
]

dna = [
    (["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"], True),
    (["ATGCGA", "CAGTGC", "TTATTT", "AGACGG", "GCGCTA", "TCACTG"], False),
    (["AAAAAA", "CAGTGC", "TTATTT", "AGACGG", "GCGCTA", "TCACTG"], False),
    (["AAAAAA", "AAAAAA", "AAAAAA", "AAAAAA", "AAAAAA", "AAAAAA"], True),
]


class TestMutation:
    @pytest.mark.parametrize("test_input", dna_sequences)
    def test_check_sequence(self, test_input):
        dna_sequence, expected = test_input
        response = check_sequence(sequence=dna_sequence)
        assert response == expected

    @pytest.mark.parametrize("test_input", string_to_matrix)
    def test_convert_to_matrix(self, test_input):
        dna_sequence, expected = test_input
        response = matrix_sequence(dna_sequence=dna_sequence)
        assert response == expected
        assert isinstance(response, List)

    @pytest.mark.parametrize("test_input", dna)
    def test_has_mutation(self, test_input):
        dna_sequence, expected = test_input
        response = has_mutation(dna_sequence=dna_sequence)
        assert isinstance(response, bool)
        assert response == expected
