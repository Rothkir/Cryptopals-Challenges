# Takes 2 byte objects -> result of the xor in bytes
def xor(xor_in, xor_against):
    
    if len(xor_in) != len(xor_against):
        raise ValueError("Inputs need to be of equal length.")
    
    res = bytes(a ^ b for (a,b) in zip(xor_in, xor_against))
    return res

if __name__ == '__main__':
    hex_string = bytes.fromhex("1c0111001f010100061a024b53535009181c")
    xor_against = bytes.fromhex("686974207468652062756c6c277320657965")
    
    res = xor(hex_string, xor_against)
    print(res.hex())