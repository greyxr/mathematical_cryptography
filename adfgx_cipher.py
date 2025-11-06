from itertools import permutations

class AdfgxCipher():
    def prepare_string(self, string):
        return "".join(i.upper() for i in string if i.isalpha()).replace("J", "I")
    def prepare_key(self, key):
        seen = set()
        seen_add = seen.add
        return "".join([x for x in key if not (x in seen or seen_add(x))])
    def create_matrix(self, key):
        letters = dict()
        alpha_set = [i for i in 'ABCDEFGHIKLMNOPQRSTUVWXYZ']
        alpha_set.reverse()
        key_set = [i for i in key]
        key_set.reverse()
        matrix = [[] for i in range(5)]
        for i in range(25):
            if (key_set):
                char = key_set.pop()
            else:
                char = alpha_set.pop()
                while (char in key):
                    char = alpha_set.pop()
            letters[char] = tuple([i//5, i%5])
            matrix[i//5].append(char)
        return matrix, letters
    def create_key_matrix(self, inter, key):
        key_matrix = {i:[] for i in key}
        for i in range(len(inter)):
            key_matrix[key[i%len(key)]].append(inter[i])
        key_matrix = dict(sorted(key_matrix.items()))
        return key_matrix
    def recreate_key_matrix(self, ciphertext, key):
        key_matrix = {i:[] for i in key}
        base_columns = len(ciphertext) // len(key)
        leftover = len(ciphertext) % len(key)
        key_numbers = {i:base_columns for i in key}
        for i in range(leftover):
            key_numbers[key[i]] += 1
        # print(key_numbers)
        last_index = 0
        for i in sorted(key):
            key_matrix[i] = [j for j in ciphertext[last_index:last_index+key_numbers[i]]]
            last_index += key_numbers[i]
        # print(key_matrix)
        return key_matrix
    def substitute_characters(self, plaintext, letters):
        intermediate = ""
        for i in plaintext:
            intermediate += self.create_digraph(i, letters)
        # print(intermediate)
        return intermediate
    def create_digraph(self, char, letters):
        [row, col] = letters[char]
        code = "ADFGX"
        return code[row] + code[col]
    def read_matrix(self, matrix):
        string = []
        for i in matrix:
            string.append("".join(matrix[i]))
        return "".join(string)
    def read_across_matrix(self, matrix, key):
        digrams = []
        while any(matrix.values()):
            row = []
            for i in key:
                if any(matrix[i]):
                    row.append(matrix[i].pop(0))
            digrams = digrams + row
        return "".join(digrams)
    def create_digrams(self, ciphertext):
        return [ciphertext[i]+ciphertext[i+1] for i in range(0,len(ciphertext),2)]
    def encode(self, plaintext, key1, key2):
        plaintext = self.prepare_string(plaintext)
        key1 = self.prepare_key(key1)
        key1 = key1.upper()
        matrix, letters = self.create_matrix(key1)
        self.matrix = matrix
        self.key_word = key2
        inter = self.substitute_characters(plaintext, letters)
        # Columnar transposition
        key_matrix = self.create_key_matrix(inter, key2)
        return self.read_matrix(key_matrix)
    def decrypt_digram(self, digram):
        code = "ADFGX"
        if digram[0] not in code or digram[1] not in code:
            raise Exception("Invalid ciphertext")
        row, col = code.index(digram[0]), code.index(digram[1])
        return self.matrix[row][col]
    def decode(self, ciphertext):
        key_matrix = self.recreate_key_matrix(ciphertext, self.key_word)
        digrams = self.create_digrams(self.read_across_matrix(key_matrix, self.key_word))
        decrypted = []
        for i in digrams:
            decrypted.append(self.decrypt_digram(i))
        return "".join(decrypted)
    def brute_force_decode(self, ciphertext, matrix, testWord):
        self.matrix = matrix
        self.key_word = testWord
        key_matrix = self.recreate_key_matrix(ciphertext, self.key_word)
        digrams = self.create_digrams(self.read_across_matrix(key_matrix, testWord))
        decrypted = []
        for i in digrams:
            decrypted.append(self.decrypt_digram(i))
        return "".join(decrypted)
decoder = AdfgxCipher()
# decoder.encode("Celebrate your success", "abcd", "test")
cipher = "GDGDAADDGDGFAXDFAXDFAFDXGDFGFAAFDGDADGDADAGDDFAAGFDDADGDAFDDAFXAADADGGFGDDDGFXFXFXFDXGAAXXDGAGXGDDGDDXGDGD"

matrix = [
    ['C', 'E', 'L', 'B', 'R'],
     ['A', 'T', 'Y', 'O', 'U'],
     ['S', 'D', 'F', 'G', 'H'],
     ['I', 'K', 'M', 'N', 'P'],
     ['Q', 'V', 'W', 'X', 'Z']
]

# print(decoder.brute_force_decode(cipher, matrix, "ABC"))

# for i in range(1,6): # Try all keys of length 10
#     # Try every permutation of length i
#     for p in permutations(range(1,i+1)):
#         print(p)

for p in permutations(range(1, 6)):
        key = "".join(chr(i+64) for i in p)
        print(decoder.brute_force_decode(cipher, matrix, key))

# key = "PGCENBQOZRSLAFTMDVIWKUYXH"

# c = decoder.encode("Kaiser Wilhelm", key, "RHEIN")
# print(c)
# print(decoder.decode(c))

# WINTERTIMEVERSIONOFDCONETWENTYONETHIRTYFOURTHIRTYFIVE