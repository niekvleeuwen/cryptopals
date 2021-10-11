# Niek van Leeuwen
# 0967267
# Minor Security Lab @ Rotterdam University of Applied Sciences

import codecs

# The string to decode in hexadecimal 
encoded_hex = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
# Decode the hexadecimal to bytes
decoded_hex = codecs.decode(encoded_hex, 'hex')
# Encode the bytes to base64 
encoded_b64 = codecs.encode(decoded_hex, 'base64')

print(f'{encoded_hex} = {decoded_hex} = {encoded_b64.decode()}')