# Niek van Leeuwen
# 0967267
# Minor Security Lab @ Rotterdam University of Applied Sciences

import codecs

def convert_hex_to_b64(hex: str) -> str:
    """Convert hexadecimal to base64
    
    Args:
        hex: a string encoded in hexadecimal
    """
    # Decode the hexadecimal to bytes
    decoded_hex = codecs.decode(hex, 'hex')
    # Encode the bytes to base64 
    result = codecs.encode(decoded_hex, 'base64').decode()
    # Remove newline
    return result.strip()


def test_convert_hex_to_b64():
    # The string to decode in hexadecimal
    input_hex = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d' 
    result = convert_hex_to_b64(input_hex)
    assert result == 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
    print(f'{input_hex} = {result}')

    print("Passed")


if __name__ == "__main__":
    test_convert_hex_to_b64()