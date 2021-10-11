# Niek van Leeuwen
# 0967267
# Minor Security Lab @ Rotterdam University of Applied Sciences


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

def calc_english_score(input_bytes):
    # Create a dict with the alphabet
    letter_frequency = dict.fromkeys(english_letter_frequency.keys(),0)

    # Count the frequency of each letter in the input string    
    for i in input_bytes:
        c = chr(i)
        if c in english_letter_frequency:
            letter_frequency[c] += 1
    
    # Convert absolute count to percentage
    for key, item in letter_frequency.items():
        letter_frequency[key] = item / len(input_bytes)
    
    # Calculate the error of the string to the relative letter frequency in the English language
    error = 0
    for i,j in zip(letter_frequency.values(),english_letter_frequency.values()):
        error += abs(i-j)
    return error

def xor_str_with_key(input_bytes, key):
    # Loop trough each byte of the input
    result = []
    for a in input_bytes:
        # Use the XOR operator on the two bytes
        xor_byte = a ^ key
        # Store the resulting byte in an array
        result.append(xor_byte)
    return bytes(result)

if __name__ == "__main__":
    best_result = None
    lowest_error = 9999999999

    with open('4.txt') as f:
        for line in f.readlines():
            decoded_str = bytes.fromhex(line)
            # Loop trough every key option (bytes must be in range 0-256)
            for i in range(256):
                result = xor_str_with_key(decoded_str, i)
                error = calc_english_score(result)

                if error < lowest_error:
                    lowest_error = error
                    best_result = result
    print(f'Best result: {best_result} (score {lowest_error})') 