def binary_to_base64(binary_string):
    base64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    
    # Convert binary string to bytes
    byte_chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    byte_values = [int(b, 2) for b in byte_chunks]
    byte_data = bytes(byte_values)

    encoded = ""
    i = 0
    while i < len(byte_data):
        block = byte_data[i:i+3]
        pad_len = 3 - len(block)
        block += b'\x00' * pad_len  # pad with null bytes for processing

        buffer = int.from_bytes(block, byteorder='big')

        for j in range(18, -1, -6):
            index = (buffer >> j) & 0b111111
            encoded += base64_alphabet[index]

        i += 3

    if pad_len == 1:
        encoded = encoded[:-1] + "="
    elif pad_len == 2:
        encoded = encoded[:-2] + "=="

    return encoded

def ascii_to_binary(ascii_string):
    return ''.join(format(ord(char), '08b') for char in ascii_string)

def hex_to_ascii(hex_string):
    return ''.join([chr(int(hex_string[i:i+2], 16)) for i in range(0, len(hex_string), 2)])

if __name__ == "__main__":
    decoded = str(input("What is your hex string? "))

    decoded = hex_to_ascii(decoded)
    decoded = ascii_to_binary(decoded)
    decoded = binary_to_base64(decoded)

    print(decoded)
