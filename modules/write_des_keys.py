#!/usr/bin/env python3

"""
    This python script aims to take the processed NTLMv1 and write a DES key file for cracking.
    If the file already exists, it skips the writing process and prints a message indicating the file was found and skipped.
    Additionally it will provide instructions on how to crack the DES Key file.
"""

def write_file(processed_hash, hashcat_output, hashtopolis_output):
    """
    Rudimentary function to:
        1. Write DES keys to file
    """
    
    try:
        with open(file=f"output_{processed_hash['user_name']}.hash", mode="x", encoding="utf8") as keys:
            keys.write(f"{processed_hash['challenge_type_1']}:{processed_hash['challenge']}\n")
            keys.write(f"{processed_hash['challenge_type_2']}:{processed_hash['challenge']}\n")
            keys.close()
        print("\n[!] DES KEY FILE NOT FOUND - WRITING \n")

    except FileExistsError:
        print("\n[!] DES KEY FILE FOUND - SKIPPING \n")

    if hashcat_output:
        print(f"[~] CRACK DES KEYS: ./hashcat -m 14000 -w 4 -a 3 -1 DES_full.hcchr --hex-charset output_{processed_hash['user_name']}.hash ?1?1?1?1?1?1?1?1")

    if hashtopolis_output:
        print("[~] CRACK DES KEYS: -a 3 -1 DES_full.hcchr --hex-charset #HL# ?1?1?1?1?1?1?1?1")

    print(f"[~] FRAME DES KEYS: ./ntlmv1_to_ntlm.py --get_ntlm --cracked_des_key_1 FIRST_KEY --cracked_des_key_2 SECOND_KEY --ntlm_challenge_type_3 {processed_hash['challenge_type_3']} --ntlm_challenge {processed_hash['challenge']}")

    print("[!] PLEASE BE AWARE THE DES KEY FILE HAS THE KEYS ORDERED AND WHEN CRACKED THE ORDER MUST BE MAINTAINED :)")
