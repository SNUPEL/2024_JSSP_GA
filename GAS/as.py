def convert_sequence(sequence):
    return [min(op // 5 + 1, 10) for op in sequence]

sequence = [37, 21, 28, 20, 25, 0, 38, 10, 42, 49, 29, 47, 40, 48, 30, 23, 44, 7, 43, 46, 26, 4, 11, 19, 16, 31, 13, 33, 14, 34, 3, 39, 22, 35, 15, 45, 5, 18, 32, 1, 2, 36, 12, 17, 6, 8, 9, 27, 24, 41]

converted_sequence = convert_sequence(sequence)
print(converted_sequence)