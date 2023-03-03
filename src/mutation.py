from typing import List

MAX_BASES = 4
MAX_MUTATION_SEQUENCES = 1


def has_mutation(dna_sequence: List[str]) -> bool:
    if not dna_sequence:
        return False
    matrix: List[List[str]] = matrix_sequence(dna_sequence=dna_sequence)
    mutation_count = 0
    for i in range(len(matrix)):
        if mutation_count > MAX_MUTATION_SEQUENCES:
            return True
        row = matrix[i]
        column = [row[i] for row in matrix]
        mutation_count += int(check_sequence(sequence=row)) + check_sequence(
            sequence=column
        )
    return False


def matrix_sequence(dna_sequence: List[str]) -> List[List[str]]:
    matrix: List[List[str]] = []
    for sequence in dna_sequence:
        matrix.append(list(sequence))
    return matrix


def check_sequence(sequence: List[str]) -> bool:
    count: int = 1
    for i in range(1, len(sequence)):
        if count == MAX_BASES:
            break
        if sequence[i] == sequence[i - 1]:
            count += 1
        else:
            count = 1

    return True if count == MAX_BASES else False
