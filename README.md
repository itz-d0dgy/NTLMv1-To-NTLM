# NTLMv1 To NTLM

This tool implements EvilMogs research around the conversion of NTLMv1 to NTLM hashes demonstrated in his ntlm_multi.py program. 
Whereby it converts NTLMv1/NTLMv1-ESS/MSCHAPv2 hash into its respective DES key parts to be cracked.
I implemented this research/rewrote EvilMogs tool to further my understanding of the NTLMv1/NTLMv1-ESS/MSCHAPv2 hash and make it a bit more usable for myself.

Credit:
1. EvilMog (Team Hashcat) #REF: https://github.com/evilmog/
2. Atom (Team Hashcat) #REF: https://hashcat.net/forum/thread-5832.html

Example:
```
python3 ntlm_multi_d0dgy_rewrite.py --crack \
    --ntlmv1 itz_d0dgy::D0DGY-1234567:76365E2D142B5612980C67D057EB9EFEEE5EF6EB6FF6E04D:727B4E35F947129EA52B9CDEDAE86934BB23EF89F50FC595:1122334455667788

#################### Create You Hashlist ####################
DES Key 1: 727B4E35F947129E:1122334455667788 >> deskeys.hash
DES Key 2: A52B9CDEDAE86934:1122334455667788 >> deskeys.hash

####################   Cracker Lacking   ####################
Hashtopolis: -a 3 -1 DES_full.hcchr --hex-charset #HL# ?1?1?1?1?1?1?1?1
Hashcat: ./hashcat -w 4 -a 3 -1 DES_full.hcchr --hex-charset deskeys.hash ?1?1?1?1?1?1?1?1

####################      Get NTLM      ####################
Run: python3 ntlm_multi_d0dgy_rewrite.py --stitch --cracked_des_key_1 X --cracked_des_key_2 X --ntlm_challenge_type_3 BB23EF89F50FC595 --ntlm_challenge 1122334455667788
//NOTE: The values for ntlm_challenge_type_3 and ntlm_challenge will be in the output file
```
