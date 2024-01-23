# NTLMv1 To NTLM

This tool is a rewrite of EvilMogs ntlmv1-multi tool which was based on "forum posts by atom the author of hashcat and research by moxie marlinspike around the conversion of NTLMv1 to NTLM hashes". 
Whereby it converts NTLMv1/NTLMv1-ESS/MSCHAPv2 hash into its respective DES key parts to be cracked.
I rewrote this tool/research based on EvilMogs tool to further my understanding of the NTLMv1/NTLMv1-ESS/MSCHAPv2 hash and make it a bit more usable for myself.

Requirements:
 1. Python 3.9
 2. [ct3_to_ntlm.bin](https://github.com/hashcat/hashcat-utils/blob/master/src/ct3_to_ntlm.c)

Credit:
 1. [EvilMog (Team Hashcat)](https://github.com/evilmog/ntlmv1-multi)
 2. [Atom (Team Hashcat)](https://hashcat.net/forum/thread-5832.html)
 3. [Hashcat](https://hashcat.net/)

Example:
```
python3 ntlmv1-to-ntlm.py --crack \
    --ntlmv1 itz_d0dgy::D0DGY-1234567:76365E2D142B5612980C67D057EB9EFEEE5EF6EB6FF6E04D:727B4E35F947129EA52B9CDEDAE86934BB23EF89F50FC595:1122334455667788

Upon running the above, there should be a file written to the directory that looks like the following.

#################### Create You Hashlist ####################
DES Key 1: 727B4E35F947129E:1122334455667788 >> deskeys.hash
DES Key 2: A52B9CDEDAE86934:1122334455667788 >> deskeys.hash

####################   Cracker Lacking   ####################
Hashtopolis: -a 3 -1 DES_full.hcchr --hex-charset #HL# ?1?1?1?1?1?1?1?1
Hashcat: ./hashcat -w 4 -a 3 -1 DES_full.hcchr --hex-charset deskeys.hash ?1?1?1?1?1?1?1?1

####################      Get NTLM      ####################
Run: python3 ntlmv1-to-ntlm.py --stitch --cracked_des_key_1 XXX --cracked_des_key_2 XXX --ntlm_challenge_type_3 XXX --ntlm_challenge XXX
NOTE: The values for ntlm_challenge_type_3 and ntlm_challenge will be auto populated in the output file, all you need todo is populate the cracked desk keys
```

