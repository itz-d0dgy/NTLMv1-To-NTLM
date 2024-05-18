#!/usr/bin/env python3

"""
    This python script aims to take a provided DES key, amd convert them into an NTLM hash.
    The conversion process is series of bitwise operations to derive the NTLM hash from the DES key. 
        1. The DES key is first converted from a hexadecimal string to a byte array.
        2. The NTLM hash is constructed by taking bits from the DES keys, and shifting them to align properly and combine them.
        3. The bitwise operations (<<, &, |) are used to manipulate the bits from the DES key to form the NTLM hash byte. 
        4. & 0xff is applied to ensure that the resulting value fits within a single byte (0-255).

"""

import subprocess
import platform

def process_keys(cracked_des_key_1, cracked_desk_key_2, challenge_type_3, challenge):
    """
    Rudimentary function to:
        1. Convert DES keys into NTLM
    """

    cracked_des_keys = [cracked_des_key_1, cracked_desk_key_2]
    converted_des_keys = []

    for keys in cracked_des_keys:
        if len(keys) != 16 or not all(c in "0123456789abcdefABCDEF" for c in keys):
            print("Invalid key format. Please provide a valid 8-byte key in hexadecimal.")
            return

        des_key_bin = bytes.fromhex(keys)

        ntlm = bytearray(7)

        ntlm[0] = (((des_key_bin[0] << 0) & ~0x01) | (des_key_bin[1] >> 7)) & 0xff
        ntlm[1] = (((des_key_bin[1] << 1) & ~0x03) | (des_key_bin[2] >> 6)) & 0xff
        ntlm[2] = (((des_key_bin[2] << 2) & ~0x07) | (des_key_bin[3] >> 5)) & 0xff
        ntlm[3] = (((des_key_bin[3] << 3) & ~0x0f) | (des_key_bin[4] >> 4)) & 0xff
        ntlm[4] = (((des_key_bin[4] << 4) & ~0x1f) | (des_key_bin[5] >> 3)) & 0xff
        ntlm[5] = (((des_key_bin[5] << 5) & ~0x3f) | (des_key_bin[6] >> 2)) & 0xff
        ntlm[6] = (((des_key_bin[6] << 6) & ~0x7f) | (des_key_bin[7] >> 1)) & 0xff

        converted_des_keys.append(f"{ntlm[0]:02x}{ntlm[1]:02x}{ntlm[2]:02x}{ntlm[3]:02x}{ntlm[4]:02x}{ntlm[5]:02x}{ntlm[6]:02x}")

    try:
        result = subprocess.run([f"./dependencies/ct3_to_ntlm_{platform.machine()}", challenge_type_3, challenge], capture_output=True, text=True, check=True)
        converted_des_keys.append(result.stdout.strip())

    except subprocess.CalledProcessError as subprocess_error:
        print("Error executing ct3_to_ntlm:", subprocess_error)

    print("".join(converted_des_keys))
