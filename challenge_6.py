# Niek van Leeuwen
# 0967267
# Minor Security Lab @ Rotterdam University of Applied Sciences

import base64

from challenge_3 import brute_force_single_byte_xor
from challenge_5 import repeating_key_xor
        

def hamming_distance(input1: bytes, input2: bytes) -> int:
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
        # Count the number of 1's in the result represented in binary
        for bit in bin(xor_byte):
            if bit == '1':
                distance += 1
    return distance

def break_repeating_key_xor(encrypted_content: bytes) -> tuple:
    """Breaking repeating-key XOR encryped contents
    
    Args:
        encrypted_content: with repeating-key XOR encrypted contents
    Returns:
        tuple: key and decrypted contents
    """
    normalized_edit_distances = {}
    for keysize in range(2,41):
        # Divide the contents in fragments of length keysize
        fragments = [encrypted_content[i:i+keysize] for i in range(0, len(encrypted_content), keysize)]

        normalized_distances = []
        for i in range(len(fragments)-1):
            # Calculate the hamming distance for the two fragments
            distance = hamming_distance(fragments[i], fragments[i+1])
            # Normalize the distance by dividing with the keysize
            normalized_distance = distance/keysize
            # Add to the sum for this keysize
            normalized_distances.append(normalized_distance)
        # Store the average normalized distance        
        normalized_edit_distances[keysize] = sum(normalized_distances) / len(normalized_distances)

    # Move further with the keysize that has the lowest value
    min_key = min(normalized_edit_distances, key=normalized_edit_distances.get)
    
    # Break the encrypted contents into blocks of KEYSIZE length
    fragments = [encrypted_content[i:i+min_key] for i in range(0, len(encrypted_content), min_key)]

    # Transpose the fragements
    transposed_fragments = []
    for i in range(min_key):
        fragement = b''
        for j in range(i, len(encrypted_content), min_key):
            fragement += bytes([encrypted_content[j]])
        transposed_fragments.append(fragement)

    # Break the key
    key = b''
    for fragement in transposed_fragments:
        key += bytes([brute_force_single_byte_xor(fragement)[0]])
    
    # Decrypt the message with the found key
    return key, repeating_key_xor(encrypted_content, key)

def test_hamming_distance():
    input1 = b'this is a test'
    input2 = b'wokka wokka!!!'

    assert hamming_distance(input1, input2) == 37
    
    print('Passed test')

def test_break_repeating_key_xor():
    # Open the txt file and decode the contents
    with open('6.txt') as f:
        encrypted_content = base64.b64decode(f.read())
    
    key, result = break_repeating_key_xor(encrypted_content)
    
    assert key == b'Terminator X: Bring the noise'
    assert result == b"I'm back and I'm ringin' the bell \nA rockin' on the mike while the fly girls yell \nIn ecstasy in the back of me \nWell that's my DJ Deshay cuttin' all them Z's \nHittin' hard and the girlies goin' crazy \nVanilla's on the mike, man I'm not lazy. \n\nI'm lettin' my drug kick in \nIt controls my mouth and I begin \nTo just let it flow, let my concepts go \nMy posse's to the side yellin', Go Vanilla Go! \n\nSmooth 'cause that's the way I will be \nAnd if you don't give a damn, then \nWhy you starin' at me \nSo get off 'cause I control the stage \nThere's no dissin' allowed \nI'm in my own phase \nThe girlies sa y they love me and that is ok \nAnd I can dance better than any kid n' play \n\nStage 2 -- Yea the one ya' wanna listen to \nIt's off my head so let the beat play through \nSo I can funk it up and make it sound good \n1-2-3 Yo -- Knock on some wood \nFor good luck, I like my rhymes atrocious \nSupercalafragilisticexpialidocious \nI'm an effect and that you can bet \nI can take a fly girl and make her wet. \n\nI'm like Samson -- Samson to Delilah \nThere's no denyin', You can try to hang \nBut you'll keep tryin' to get my style \nOver and over, practice makes perfect \nBut not if you're a loafer. \n\nYou'll get nowhere, no place, no time, no girls \nSoon -- Oh my God, homebody, you probably eat \nSpaghetti with a spoon! Come on and say it! \n\nVIP. Vanilla Ice yep, yep, I'm comin' hard like a rhino \nIntoxicating so you stagger like a wino \nSo punks stop trying and girl stop cryin' \nVanilla Ice is sellin' and you people are buyin' \n'Cause why the freaks are jockin' like Crazy Glue \nMovin' and groovin' trying to sing along \nAll through the ghetto groovin' this here song \nNow you're amazed by the VIP posse. \n\nSteppin' so hard like a German Nazi \nStartled by the bases hittin' ground \nThere's no trippin' on mine, I'm just gettin' down \nSparkamatic, I'm hangin' tight like a fanatic \nYou trapped me once and I thought that \nYou might have it \nSo step down and lend me your ear \n'89 in my time! You, '90 is my year. \n\nYou're weakenin' fast, YO! and I can tell it \nYour body's gettin' hot, so, so I can smell it \nSo don't be mad and don't be sad \n'Cause the lyrics belong to ICE, You can call me Dad \nYou're pitchin' a fit, so step back and endure \nLet the witch doctor, Ice, do the dance to cure \nSo come up close and don't be square \nYou wanna battle me -- Anytime, anywhere \n\nYou thought that I was weak, Boy, you're dead wrong \nSo come on, everybody and sing this song \n\nSay -- Play that funky music Say, go white boy, go white boy go \nplay that funky music Go white boy, go white boy, go \nLay down and boogie and play that funky music till you die. \n\nPlay that funky music Come on, Come on, let me hear \nPlay that funky music white boy you say it, say it \nPlay that funky music A little louder now \nPlay that funky music, white boy Come on, Come on, Come on \nPlay that funky music \n"
    
    print(f'Passed test \nKey: {key} \nMessage: \n' + result.decode('UTF-8'))

if __name__ == "__main__":
    test_hamming_distance()
    test_break_repeating_key_xor()