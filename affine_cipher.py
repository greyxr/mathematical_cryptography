class AffineCipher():
    def standardize_char(self, char):
        return ord(char) - 65
    def ascii_char(self, num):
        return chr(num + 65)
    def decode(self, ciphertext, a_1, b):
        return "".join(self.ascii_char((a_1*(self.standardize_char(i) - b)) % 26) for i in ciphertext)


# Inverse of 9 mod 26 is 3
# Decode cipher by a^-1(x - b) mod 26
# Inverse of 11 mod 26 is 19

potential_ciphertexts = [
    "TKXPGWCFNCTXKLFCNCPUMNUUFXPWKCULFGUFUQKGTUBFPPFGU",
    "GHTMTKHODWNZVGHFAREWLYSTYQBSCEZZZJZUQCYLVXEZDCSGKDDOZLJLQABTWAFRHAKDRCWEQJEXFTXRUPNIPVTJRUHZBRXHQFMVLYHWXYRGWKJNMAYLDGMZZVOYHKUHGWYRWZPMOVYJCAE",
    "XOTQSIOJZBTZFBABUOJKBNHVOZVFFBZZ",
    "EWFOHUFMZEZYFVATLYATYKLWGXPFAMTR",
    "YKUQULGZZLNQLAHJFTPLIOJIZDQBQETICTOKYGNWMGADDCCXUZHPXUBBTPGWWLNQIDIKHAMTUCUHRWOPCECEOJMKOLZULGORKHMVXKEKUTSRMXLNZBRUANNWFNBVMTUNCQJHHKORIJLDBQK"
]
a = 11
b = 9
a_1 = 19
b_1 = 3 # Just in case parameters are backwards

cipher = AffineCipher()
for ciphertext in potential_ciphertexts:
    print(cipher.decode(ciphertext, a_1, b))
    print("---------------------")