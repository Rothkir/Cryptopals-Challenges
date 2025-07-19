import fixed_xor as fx

# Takes a key (string) and plaintext (string) and returns the hex string of the XOR
def xor_encrypt(key, plaintext):
    # First turn the plaintext into byte object
    plaintext_bytes = bytes(plaintext, 'utf-8')

    # Then we turn the key into a byte object the same size as the plaintext
    # Example. key = 'ICE' then we want to encrypt the first byte of the plaintext with 'I', the second with 'C' and so on.
    key_bytes = bytes(key, 'utf-8')
    repeated_key = bytes([key_bytes[i%len(key_bytes)] for i in range(len(plaintext_bytes))])
    
    cipher_bytes = fx.xor(repeated_key, plaintext_bytes)
    return cipher_bytes.hex()


if __name__ == '__main__':
    key = 'ICE'
    plaintext = "Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"
    cipher = xor_encrypt(key=key, plaintext=plaintext)

    print(cipher)