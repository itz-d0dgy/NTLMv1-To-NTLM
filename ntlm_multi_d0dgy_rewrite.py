#!/usr/bin/env python3

"""
    This tool is a rewrite of EvilMogs ntlmv1-multi tool which was based on "forum posts by atom the author of hashcat and research by moxie marlinspike around the conversion of NTLMv1 to NTLM hashes". 
    Whereby it converts NTLMv1/NTLMv1-ESS/MSCHAPv2 hash into its respective DES key parts to be cracked.
    I rewrote this tool/research based on EvilMogs tool to further my understanding of the NTLMv1/NTLMv1-ESS/MSCHAPv2 hash and make it a bit more usable for myself.

    Credit:
        1. EvilMog (Team Hashcat) #REF: [https://github.com/evilmog/](https://github.com/evilmog/ntlmv1-multi)
        2. Atom (Team Hashcat) #REF: [https://hashcat.net](https://hashcat.net/forum/thread-5832.html)
    
    Copyright: itz_d0dgy
"""

import argparse
import hashlib
import binascii
import os

# ------------------------------------------------------------------------------------------------------------------------------------------------------------ #

def keys_to_ntlm(cracked_des_key_1, cracked_desk_key_2, challenge_type_3, challenge):
    """
    Rudementry function to:
        1. Convert DES keys back into NTLM format
    """

    cracked_des_keys = [cracked_des_key_1, cracked_desk_key_2]
    converted_des_keys = []

    for keys in cracked_des_keys:
        if len(keys) != 16 or not all(c in '0123456789abcdefABCDEF' for c in keys):
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

    converted_des_keys.append(os.popen(f"./ct3_to_ntlm.bin {challenge_type_3} {challenge}").read().strip())
    # Note: Yes, there is RCE here. But hey if you want to shell your own box be my guest.
    # Also if you are running this on a server and allow individuals to execute this script you should really be asking yourself.
    # Why am I formating cracked DES keys on a production server????
    # Ethan if you see this, I see the irony and it is not lost on me

    print("".join(converted_des_keys))

# ------------------------------------------------------------------------------------------------------------------------------------------------------------ #

def write_des_keys(user_name, challenge_type_1, challenge_type_2, challenge_type_3, challenge):
    """
    Rudementry function to:
        1. Write NTLM Challenge Types into DES format
        NOTE:
    """

    try:
        with open(file=f"output_{user_name}.txt", mode="x", encoding="utf8") as steps:
            steps.write("#################### Create You Hashlist ####################\n")
            steps.write(f"DES Key 1: {challenge_type_1}:{challenge} >> deskeys.hash\n")
            steps.write(f"DES Key 2: {challenge_type_2}:{challenge} >> deskeys.hash\n")
            steps.write("\n")
            steps.write("####################   Cracker Lacking   ####################\n")
            steps.write("Hashtopolis: -a 3 -1 DES_full.hcchr --hex-charset #HL# ?1?1?1?1?1?1?1?1\n")
            steps.write("Hashcat: ./hashcat -w 4 -a 3 -1 DES_full.hcchr --hex-charset deskeys.hash ?1?1?1?1?1?1?1?1\n")
            steps.write("\n")
            steps.write("####################      Get NTLM      ####################\n")
            steps.write(f"Run: python3 ntlm_multi_d0dgy_rewrite.py --stitch --cracked_des_key_1 X --cracked_des_key_2 X --ntlm_challenge_type_3 {challenge_type_3} --ntlm_challenge {challenge}\n")
        steps.close()

    except FileExistsError:
        print("Hey, so I hate to tell you this but that file already exists.")
        return

# ------------------------------------------------------------------------------------------------------------------------------------------------------------ #

def create_des_keys(ntlmv1):
    """
    Rudementry function to:
        1. Split NTLMv1 into respective componenets
        NOTE:
    """

    hash_identifiers = ["user_name", "", "domain", "lm_response", "nt_response", "challenge"]
    split_hash = ntlmv1.split(":")
    hash_data = {}

    for delimiter, identifiers in enumerate(hash_identifiers):
        if identifiers != "":
            hash_data[identifiers] = split_hash[delimiter]

        if identifiers == "lm_response":
            # If the NTLMv1 is not NTLMv1-ESS/SSP (Client Challenge is Accepted)
            if split_hash[delimiter][20:48] != "0000000000000000000000000000":
                hash_data["challenge_type_1"] = split_hash[delimiter + 1][0:16]
                hash_data["challenge_type_2"] = split_hash[delimiter + 1][16:32]

            # If the NTLMv1 is NTLMv1-ESS/SSP (Server Challenge is Enforced)
            if split_hash[delimiter][20:48] == "0000000000000000000000000000":
                m = hashlib.md5()
                m.update(binascii.unhexlify(split_hash[delimiter + 2] + split_hash[delimiter][0:16]))
                md5hash = m.hexdigest()
                hash_data["srv_challenge"] = md5hash[0:16]
                hash_data["challenge_type_1"] = split_hash[delimiter + 1][0:16]
                hash_data["challenge_type_2"] = split_hash[delimiter + 1][16:32]

        if identifiers == "nt_response":
            hash_data["challenge_type_3"] = split_hash[delimiter][32:48]

    if "srv_challenge" in hash_data:
        write_des_keys(hash_data["user_name"], hash_data["challenge_type_1"], hash_data["challenge_type_2"], hash_data["challenge_type_3"], hash_data["srv_challenge"])

    else:
        write_des_keys(hash_data["user_name"], hash_data["challenge_type_1"], hash_data["challenge_type_2"], hash_data["challenge_type_3"], hash_data["challenge"])

# ------------------------------------------------------------------------------------------------------------------------------------------------------------ #

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--ntlmv1')

    crack_or_stich_group = parser.add_mutually_exclusive_group(required=True)
    crack_or_stich_group.add_argument("--crack", action=argparse.BooleanOptionalAction)
    crack_or_stich_group.add_argument("--stitch", action=argparse.BooleanOptionalAction)

    group = parser.add_argument_group()
    group.add_argument("--cracked_des_key_1", help="Cracked DES Key 1")
    group.add_argument("--cracked_des_key_2", help="Cracked DES Key 2")
    group.add_argument("--ntlm_challenge_type_3", help="NTLM Challenge Type 3")
    group.add_argument("--ntlm_challenge", help="NTLM Challenge")

    arguments = parser.parse_args()

    if arguments.crack:
        create_des_keys(arguments.ntlmv1)

    if arguments.stitch:
        keys_to_ntlm(arguments.cracked_des_key_1, arguments.cracked_des_key_2, arguments.ntlm_challenge_type_3, arguments.ntlm_challenge)
