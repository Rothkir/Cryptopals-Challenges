import fixed_xor
import hex_to_base64
import repeating_xor
import xor_cipher
import base64

def base_64_to_hex(base64_string):
    # Decode base64 string
    decoded_bytes = base64.b64decode(base64_string)

    # Convert to hex string
    hex_string = decoded_bytes.hex()
    return hex_string

def hamming_distance(b1: bytes, b2: bytes) -> int:
    """Return the Hamming distance between two bytes."""
    if len(b1) != len(b2):
        raise ValueError("Bytes must be of equal length.")
    return sum(bin(x ^ y).count('1') for x, y in zip(b1, b2))

def decode_repeating_xor_cipher(cipher_string: str):

    # Turns cipher string (base64 encoded) to binary string
    cipher_bytes = base64.b64decode(cipher_string)
    
    best_keysize = 0
    smallest_distance = 10000
    num_blocks = 10
    # Finding probable KEYSIZE
    for keysize in range(2, 40):
        distances = []
        for i in range(0,num_blocks):
            block1 = cipher_bytes[i * keysize: (i+1) * keysize]
            block2 = cipher_bytes[(i+1) * keysize: (i+2) * keysize]
            if len(block1) != keysize or len(block2) != keysize:
                break
            distances.append(hamming_distance(block1, block2) / keysize)
        if len(distances) < num_blocks:
            continue
        distance = sum(distances) / len(distances)
        if distance < smallest_distance:
            smallest_distance = distance
            best_keysize = keysize
    
    print(f"Guessed keysize: {best_keysize}")

    blocks = []

    for i in range(0, best_keysize):
        block = bytes()
        for y in range(i, len(cipher_bytes), best_keysize):
            block += bytes([cipher_bytes[y]])
        blocks.append(block)

    final_key = b''
    for i in range(len(blocks)):
        key, plaintext, score = xor_cipher.decode_cipher(blocks[i])
        final_key+=key

    print(final_key)

    full_key_repeated = bytes([final_key[i%len(final_key)] for i in range(len(cipher_bytes))])
    plaintext = fixed_xor.xor(cipher_bytes, full_key_repeated)
    print(plaintext.decode('utf-8'))

if __name__ == '__main__':

    with open("6.txt", "r") as file:
        cipher = ''.join(line.strip() for line in file)

    decode_repeating_xor_cipher(cipher)