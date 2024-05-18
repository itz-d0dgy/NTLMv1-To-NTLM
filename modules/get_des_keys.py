#!/usr/bin/env python3

"""
    This Python script script aims to process an NTLMv1 hash and extracts relevant information from it. 
    It splits the hash into parts and identifies components such as the username, domain, LM response, NT response, and challenge. 
    Depending on whether the hash is NTLMv1-ESS/SSP or not, it computes the challenge differently. Finally, it returns a dictionary containing the extracted data.
"""

import hashlib
import binascii

def process_hash(ntlmv1_hash):
    """
    Rudimentary function to:
        1. Convert NTLMv1/NTLMv1-ESS into DES keys
    """

    hash_identifiers = ["user_name", "", "domain", "lm_response", "nt_response", "challenge"]
    split_hash = ntlmv1_hash.split(":")
    hash_data = {}

    for delimiter, identifiers in enumerate(hash_identifiers):
        if identifiers == "user_name":
            hash_data[identifiers] = split_hash[delimiter]

        if identifiers == "lm_response":
            # If the NTLMv1 is not NTLMv1-ESS/SSP (Client Challenge is Accepted)
            if split_hash[delimiter][20:48] != "0000000000000000000000000000":
                hash_data["challenge"] = split_hash[delimiter + 2].upper()
                hash_data["challenge_type_1"] = split_hash[delimiter + 1][0:16]
                hash_data["challenge_type_2"] = split_hash[delimiter + 1][16:32]

            # If the NTLMv1 is NTLMv1-ESS/SSP (Server Challenge is Enforced)
            if split_hash[delimiter][20:48] == "0000000000000000000000000000":
                md5 = hashlib.md5()
                md5.update(binascii.unhexlify(split_hash[delimiter + 2] + split_hash[delimiter][0:16]))
                md5hash = md5.hexdigest().upper()
                hash_data["challenge"] = md5hash[0:16]
                hash_data["challenge_type_1"] = split_hash[delimiter + 1][0:16]
                hash_data["challenge_type_2"] = split_hash[delimiter + 1][16:32]

        if identifiers == "nt_response":
            hash_data["challenge_type_3"] = split_hash[delimiter][32:48]

    return hash_data