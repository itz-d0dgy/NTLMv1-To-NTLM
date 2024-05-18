# NTLMv1 To NTLM

This tool is a rewrite of EvilMogs ntlmv1-multi tool which was based on "forum posts by atom the author of hashcat and research by moxie marlinspike around the conversion of NTLMv1 to NTLM hashes". Whereby it converts NTLMv1/NTLMv1-ESS/MSCHAPv2 hash into its respective DES key parts to be cracked.

I wrote my own version of this tool based of off EvilMogs tool and research to further my understanding of the NTLMv1/NTLMv1-ESS/MSCHAPv2 hash and make it a bit more usable for myself.

Requirements:
 1. Python 3.12.2
 2. [ct3_to_ntlm.bin](https://github.com/hashcat/hashcat-utils/blob/master/src/ct3_to_ntlm.c)

Credit:
 1. [EvilMog (Team Hashcat)](https://github.com/evilmog/ntlmv1-multi)
 2. [Atom (Team Hashcat)](https://hashcat.net/forum/thread-5832.html)
 3. [Hashcat](https://hashcat.net/)

Example:
```
// Step 0 - Test Hashes:
NTLMv1: itz_d0dgy::D0DGY-1234567:76365E2D142B5612980C67D057EB9EFEEE5EF6EB6FF6E04D:727B4E35F947129EA52B9CDEDAE86934BB23EF89F50FC595:1122334455667788

NTLMv1-ESS: itz_d0dgy::D0DGY-1234567:85D5BC2CE95161CD00000000000000000000000000000000:892F905962F76D323837F613F88DE27C2BBD6C9ABCD021D0:1122334455667788

// Step 1 - Convert NTLMv1 to DES Keys (Using NTLMv1 as example)
python ntlmv1_to_ntlm.py \
    --get_des_keys \
    --hashcat \
    --ntlmv1 itz_d0dgy::D0DGY-1234567:76365E2D142B5612980C67D057EB9EFEEE5EF6EB6FF6E04D:727B4E35F947129EA52B9CDEDAE86934BB23EF89F50FC595:1122334455667788

This will produce a hash file with the following output for cracking:
    727B4E35F947129E:1122334455667788:$HEX[8923BDFDAF753F63]
    A52B9CDEDAE86934:1122334455667788:$HEX[17D741D7DDC1C36F]

    or if you used the NtLMv1-ESS:

    892F905962F76D32:B36D2B9A8607EA77:$HEX[8923BDFDAF753F63]
    3837F613F88DE27C:B36D2B9A8607EA77:$HEX[17D741D7DDC1C36F]

// Step 2 - Convert DES Keys to NTLM
python ntlmv1_to_ntlm.py \
    --get_ntlm \
    --cracked_des_key_1 8923BDFDAF753F63 \
    --cracked_des_key_2 17D741D7DDC1C36F \
    --ntlm_challenge_type_3 BB23EF89F50FC595 \
    --ntlm_challenge 1122334455667788

This will produce the following output:
    8846f7eaee8fb117ad06bdd830b7586c
```

