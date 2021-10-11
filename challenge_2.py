# Niek van Leeuwen
# 0967267
# Minor Security Lab @ Rotterdam University of Applied Sciences

import codecs

str_1 = codecs.decode('1c0111001f010100061a024b53535009181c', 'hex')
str_2 = codecs.decode('686974207468652062756c6c277320657965', 'hex')

# Loop trough each byte of both byte strings
result = []
for a,b in zip(str_1, str_2):
    # Use the XOR operator on the two bytes
    xor_byte = a ^ b
    # Store the resulting byte in an array
    result.append(xor_byte)

# Convert the result to bytes
result = bytes(result) 

# Encode the result in hexadecimal
result = codecs.encode(result, 'hex')

print(result)