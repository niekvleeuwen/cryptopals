# Niek van Leeuwen
# 0967267
# Minor Security Lab @ Rotterdam University of Applied Sciences

import base64
import itertools

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
    letter_frequency = dict.fromkeys(english_letter_frequency.keys(), 0)

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

def break_single_character_xor(input_bytes):
    best_key = None
    lowest_error = 9999999999

    # Loop trough every key option (bytes must be in range 0-256)
    for i in range(256):
        # Loop trough each byte of the input
        result = []
        for a in input_bytes:
            # Use the XOR operator on the two bytes
            xor_byte = a ^ i
            # Store the resulting byte in an array
            result.append(xor_byte)
        
        result = bytes(result)
        error = calc_english_score(result)

        if error < lowest_error:
            lowest_error = error
            best_key = i
    return best_key
        

def hamming_distance(input1, input2):
    """Calculate the Hamming distance between two strings. First the XOR operation 
    is preformed and then the total number of 1s will be counted and returned
    
    Args:
        input1 (bytes): first string to compare
        input2 (bytes): second string to compare 
    Returns:
        int: hamming distance
    """
    distance = 0
    for i1, i2 in zip(input1, input2):
        xor_byte = i1 ^ i2
        for bit in bin(xor_byte):
            if bit == '1':
                distance += 1
    return distance

def repeating_key_xor(input_bytes, key):
    # Loop trough each byte of the input and iterate over the key in a cycle (so ICEICEICEICE...)
    result = []
    for byte, key_byte in zip(input_bytes, itertools.cycle(key)):
        # Use the XOR operator on the two bytes
        xor_byte = byte ^ key_byte
        # Store the resulting byte in an array
        result.append(xor_byte)
    # return the result in hexadecimal  
    return bytes(result)

def break_repeating_key_xor(encrypted_content):
    normalized_edit_distances = {}
    for keysize in range(2,41):
        # divide the contents in fragments
        fragments = [encrypted_content[i:i+keysize] for i in range(0, len(encrypted_content), keysize)]

        normalized_distances = []
        for i in range(len(fragments)-1):
            # Calculate the hamming distance for the two fragments
            distance = hamming_distance(fragments[i], fragments[i+1])
            # Normalize the distance by dividing with the keysize
            normalized_distance = distance/keysize
            # Add to the sum for this keysize
            normalized_distances.append(normalized_distance)
        # Store the result
        normalized_edit_distances[keysize] = sum(normalized_distances) / len(normalized_distances)

    # take the keysize with the lowest value
    min_key = min(normalized_edit_distances, key=normalized_edit_distances.get)
    
    # break the ciphertext into blocks of KEYSIZE length.
    fragments = [encrypted_content[i:i+min_key] for i in range(0, len(encrypted_content), min_key)]

    # transpose the fragements
    transposed_fragments = []
    for i in range(min_key):
        fragement = b''
        for j in range(i, len(encrypted_content), min_key):
            fragement += bytes([encrypted_content[j]])
        transposed_fragments.append(fragement)

    # break the key
    key = b''
    for fragement in transposed_fragments:
        key += bytes([break_single_character_xor(fragement)]) 
    print(f'Found key: {key}')
    
    # decrypt the message with the key
    return repeating_key_xor(encrypted_content, key)

if __name__ == "__main__":
    # Open the txt file and decode the contents
    with open('6.txt') as f:
        encrypted_content = base64.b64decode(f.read())
    
    result = break_repeating_key_xor(encrypted_content)

    print(f'Found message: \n' + result.decode('UTF-8'))