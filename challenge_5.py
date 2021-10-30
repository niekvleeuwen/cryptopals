# Niek van Leeuwen
# 0967267
# Minor Security Lab @ Rotterdam University of Applied Sciences

import itertools

def repeating_key_xor(input: bytes, key: bytes) -> str:
    """Encrypt the given input with repeating-key XOR
    
    Args:
        input: input to encrypt
        key: key used during encryption
    
    Returns:
        str: hex encoded string with the encrypted input 
    """
    # Loop trough each byte of the input and iterate over the key in a cycle (so for key ICE: ICEICEICEICE...)
    result = []
    for byte, key_byte in zip(input, itertools.cycle(key)):
        print(f'Encrypting {chr(byte)} with {chr(key_byte)}')
        # Use the XOR operator on the two bytes
        xor_byte = byte ^ key_byte
        # Store the resulting byte in an array
        result.append(xor_byte)
    # Return the result in hexadecimal  
    return bytes(result).hex()


def test_repeating_key_xor():
    key = b'ICE'
    input = b"Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"

    result = repeating_key_xor(input, key)

    assert result == '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20690a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'

    print('Passed')

if __name__ == "__main__":
    test_repeating_key_xor()    