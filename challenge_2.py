# Niek van Leeuwen
# 0967267
# Minor Security Lab @ Rotterdam University of Applied Sciences

import codecs


def xor(buf1: bytes, buf2: bytes) -> bytes:
    """Produces the XOR combination for two equal-length buffers
    
    Args:
        buf1: first buffer (should be the same size as buf2)
        buf2: second buffer (should be the same size as buf1)
    """
    # Loop trough each byte of both byte strings
    result = []
    for a,b in zip(buf1, buf2):
        # Use the XOR operator on the two bytes
        xor_byte = a ^ b
        # Store the resulting byte in an array
        result.append(xor_byte)

    # Convert the result to bytes
    result = bytes(result) 

    # Encode the result in hexadecimal
    return codecs.encode(result, 'hex')

def test_xor():
    # The buffers to decode in hexadecimal
    str1 = '1c0111001f010100061a024b53535009181c'
    str2 = '686974207468652062756c6c277320657965'
    # Convert the buffers to bytes
    buf1 = codecs.decode(str1, 'hex')
    buf2 = codecs.decode(str2, 'hex')

    result = xor(buf1, buf2)
    
    # Verify the results
    assert result == b'746865206b696420646f6e277420706c6179'
    
    print(str1)
    print(str2)
    print('====================================')
    print(result.decode())
    
    print("Passed")


if __name__ == "__main__":
    test_xor()