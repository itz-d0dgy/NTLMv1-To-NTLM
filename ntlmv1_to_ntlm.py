#!/usr/bin/env python3

"""
    This tool is a variant of EvilMogs ntlmv1-multi tool which was based on "forum posts by atom the author of hashcat and research by moxie marlinspike". 
    Whereby it converts NTLMv1/NTLMv1-ESS hashes into its respective DES key parts to be cracked. 

    Credit:
        1. EvilMog (Team Hashcat) #REF: [https://github.com/evilmog/](https://github.com/evilmog/ntlmv1-multi)
        2. Atom (Team Hashcat) #REF: [https://hashcat.net](https://hashcat.net/forum/thread-5832.html)
    
    Copyright: itz_d0dgy
"""

from argparse import ArgumentParser, BooleanOptionalAction
from modules.get_des_keys import process_hash
from modules.write_des_keys import write_file
from modules.get_ntlm import process_keys

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("--ntlmv1")

    function_group = parser.add_mutually_exclusive_group(required=True)
    function_group.add_argument("--get_des_keys", action=BooleanOptionalAction)
    function_group.add_argument("--get_ntlm", action=BooleanOptionalAction)\
    
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument("--hashcat", action=BooleanOptionalAction)
    output_group.add_argument("--hashtopolis", action=BooleanOptionalAction)

    group = parser.add_argument_group()
    group.add_argument("--cracked_des_key_1", help="Cracked DES Key 1")
    group.add_argument("--cracked_des_key_2", help="Cracked DES Key 2")
    group.add_argument("--ntlm_challenge_type_3", help="NTLM Challenge Type 3")
    group.add_argument("--ntlm_challenge", help="NTLM Challenge")

    arguments = parser.parse_args()

    if arguments.get_des_keys:
        if arguments.hashcat or arguments.hashtopolis:
            write_file(process_hash(arguments.ntlmv1), arguments.hashcat, arguments.hashtopolis)
        else:
            print("\n[!] Please include necessary flags: --hashcat or --hashtopolis")

    if arguments.get_ntlm:
        if arguments.cracked_des_key_1 and arguments.cracked_des_key_2 and arguments.ntlm_challenge_type_3 and arguments.ntlm_challenge:
            process_keys(arguments.cracked_des_key_1, arguments.cracked_des_key_2, arguments.ntlm_challenge_type_3, arguments.ntlm_challenge)
