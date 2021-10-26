# Niek van Leeuwen
# 0967267
# Minor Security Lab @ Rotterdam University of Applied Sciences

from challenge_3 import calculate_english_error, xor_with_key


def detect_single_character_xor(lines: list) -> str:
    """Brute force list of strings on single-byte XOR 
    
    Args:
        lines: list of strings (hex encoded) to test for single-character XOR
    
    Returns:
        str: best found result
    """
    best_result = None
    lowest_error = 9999999999

    for line in lines:
        decoded_str = bytes.fromhex(line)
        # Loop trough every key option (bytes must be in range 0-256)
        for i in range(256):
            result = xor_with_key(decoded_str, i)
            error = calculate_english_error(result)

            if error < lowest_error:
                lowest_error = error
                best_result = result
    print(f'Best result: {best_result} (score {lowest_error})') 
    return best_result    

def test_detect_single_character_xor():
    # Read the input file
    with open('4.txt') as f:
        result = detect_single_character_xor(f.readlines())

    # Verify the results
    assert result == b'Now that the party is jumping\n'

    print("Passed")

if __name__ == "__main__":
    test_detect_single_character_xor()