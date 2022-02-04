# Niek van Leeuwen
# 0967267
# Minor Security Lab @ Rotterdam University of Applied Sciences

import codecs


# Letter frequency retrieved from https://en.wikipedia.org/wiki/Letter_frequency
english_letter_frequency = {
    'a': 0.08167, 
    'b': 0.01492, 
    'c': 0.02782, 
    'd': 0.04253,
    'e': 0.12702, 
    'f': 0.02228, 
    'g': 0.02015, 
    'h': 0.06094,
    'i': 0.06094, 
    'j': 0.00153, 
    'k': 0.00772, 
    'l': 0.04025,
    'm': 0.02406, 
    'n': 0.06749, 
    'o': 0.07507, 
    'p': 0.01929,
    'q': 0.00095, 
    'r': 0.05987, 
    's': 0.06327, 
    't': 0.09056,
    'u': 0.02758, 
    'v': 0.00978, 
    'w': 0.02360, 
    'x': 0.00150,
    'y': 0.01974, 
    'z': 0.00074,
}


def calculate_english_error(input: bytes) -> int:
    """Calculate an error based on English letter frequency for the given input.
       The lower the error is, the more the letter freqeuncy matches the English
       letter frequency.
    
    Args:
        input: input to calculate score for
    
    Returns:
        int: error (the lower the better)
    """
    # Create a dict with the alphabet
    letter_frequency = dict.fromkeys(english_letter_frequency.keys(), 0)

    # Count the frequency of each letter in the input string    
    for i in input:
        c = chr(i)
        if c in english_letter_frequency:
            letter_frequency[c] += 1
    
    # Convert absolute count to percentage
    for key, item in letter_frequency.items():
        letter_frequency[key] = item / len(input)
    
    # Calculate the error of the string to the relative letter frequency in the English language
    error = 0
    for i,j in zip(letter_frequency.values(), english_letter_frequency.values()):
        error += abs(i - j)
    return error


def xor_with_key(buf: bytes, key: int) -> bytes:
    """Produces the XOR combination for a buffer and a key
    
    Args:
        buf: the buffer to apply the key to
        key: the key to apply to the buffer
    
    Returns:
        bytes: result of the buffer xor'd with the key
    """
    # Loop trough each byte of the input
    result = []
    for a in buf:
        # Use the XOR operator on the two bytes
        xor_byte = a ^ key
        # Store the resulting byte in an array
        result.append(xor_byte)
    return bytes(result)


def brute_force_single_byte_xor(input: bytes) -> tuple:
    """Brute force single-byte XOR encrypted bytes 
    
    Args:
        bytes: encrypted bytes with single-byte XOR
    
    Returns:
        tuple: key and result of the result with the lowest error 
    """
    best_result = None
    best_key = None
    lowest_error = 9999999999

    # Loop trough every key option (bytes must be in range 0-256)
    for key in range(256):
        result = xor_with_key(input, key)
        error = calculate_english_error(result)

        # store the result with the lowest recorded error
        if error < lowest_error:
            lowest_error = error
            best_result = result
            best_key = key
    return best_key, best_result


def test_brute_force_single_byte_xor():
    input = codecs.decode('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736', 'hex')
    
    key, result = brute_force_single_byte_xor(input)

    # Verify the results
    assert key == 88
    assert result == b"Cooking MC's like a pound of bacon"

    print(f'Passed test. Result: {result} with key {key}') 

if __name__ == "__main__":
    test_brute_force_single_byte_xor()