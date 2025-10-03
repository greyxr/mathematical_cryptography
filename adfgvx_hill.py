import numpy as np
from sympy import Matrix
import random
import string
class AdfgvxCipher():
    def prepare_string(self, string):
        return "".join(i.upper() if i.isalpha() else i for i in string).replace("J","I")
    def create_matrix(self, key):
        letters = dict()
        alpha_set = [i for i in 'ABCDEFGHIKLMNOPQRSTUVWXYZ0123456789 ']
        alpha_set.reverse()
        key_set = [i for i in key]
        key_set.reverse()
        matrix = [[] for i in range(6)]
        for i in range(36):
            if (key_set):
                char = key_set.pop()
            else:
                char = alpha_set.pop()
                while (char in key):
                    char = alpha_set.pop()
            letters[char] = tuple([i//6, i%6])
            matrix[i//6].append(char)
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
        for i in key:
            key_matrix[i] = [j for j in ciphertext[last_index:last_index+key_numbers[i]]]
            last_index += key_numbers[i]
        # print(key_matrix)
        return dict(sorted(key_matrix.items()))
    def substitute_characters(self, plaintext, letters):
        intermediate = ""
        for i in plaintext:
            intermediate += self.create_digraph(i, letters)
        # print(intermediate)
        return intermediate
    def create_digraph(self, char, letters):
        [row, col] = letters[char]
        code = "ADFGVX"
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
    def encrypt_digram(self, digram, matrix, letters):
        [frow, fcol] = letters[digram[0]]
        [srow, scol] = letters[digram[1]]
        new_frow, new_fcol, new_srow, new_scol = 0, 0, 0, 0
        if frow == srow:
            new_frow, new_fcol, new_srow, new_scol = frow,(fcol+1)%5,srow,(scol+1)%5
        elif fcol == scol:
            new_frow, new_fcol, new_srow, new_scol = (frow+1)%5,fcol,(srow+1)%5,scol
        else:
            new_frow, new_fcol, new_srow, new_scol = frow,scol,srow,fcol
        return matrix[new_frow][new_fcol] + matrix[new_srow][new_scol]
    def create_digrams(self, ciphertext):
        return [ciphertext[i]+ciphertext[i+1] for i in range(0,len(ciphertext),2)]
    def encode(self, plaintext, key1, key2):
        plaintext = self.prepare_string(plaintext)
        order = [3,5,2,4,1,0]
        key1 = "".join(key1[i] for i in order)
        matrix, letters = self.create_matrix(key1)
        self.matrix = matrix
        self.letters = letters
        self.key_sentence = key1
        self.key_word = key2
        inter = self.substitute_characters(plaintext, letters)
        # Columnar transposition
        key_matrix = self.create_key_matrix(inter, key2)
        return self.read_matrix(key_matrix)
    def decrypt_digram(self, digram):
        code = "ADFGVX"
        if digram[0] not in code or digram[1] not in code:
            raise Exception("Invalid ciphertext")
        row, col = code.index(digram[0]), code.index(digram[1])
        return self.matrix[row][col]
    def decode(self, ciphertext):
        # Recreate key matrix
        key_matrix = self.recreate_key_matrix(ciphertext, self.key_word)
        digrams = self.create_digrams(self.read_across_matrix(key_matrix, self.key_word))
        # print(self.matrix)
        # Get intermediate ciphertext
        # Decrypt digrams
        # digrams = self.create_digrams(ciphertext)
        decrypted = []
        for i in digrams:
            decrypted.append(self.decrypt_digram(i))
        return "".join(decrypted)
class HillCipher():
    def encode(self, plaintext, key):
        if len(plaintext) % 3 != 0:
            plaintext += ("Z" * (3 - (len(plaintext) % 3)))
        matrix = self.create_matrix(key)
        self.matrix = matrix
        if not (self.is_invertible(matrix)):
            raise Exception("Invalid matrix!")
        encrypted = []
        # print(matrix)
        for i in range(0,len(plaintext),3):
            block = [self.char_to_num(char) for char in plaintext[i:i+3]]
            encrypted_block = np.dot(np.array(block), np.array(matrix)) % 26
            encrypted_block = [self.num_to_char(i%26) for i in encrypted_block]
            encrypted.append(encrypted_block)
        return "".join("".join(i) for i in encrypted)
    def decode(self, ciphertext):
        inv_matrix = Matrix(self.matrix).inv_mod(26).tolist()
        decrypted = []
        for i in range(0,len(ciphertext),3):
            block = ciphertext[i:i+3]
            if len(block) < 3:
                block
            block = [self.char_to_num(char) for char in ciphertext[i:i+3]]
            decrypted_block = np.dot(np.array(block), np.array(inv_matrix)) % 26
            decrypted_block = [self.num_to_char(i%26) for i in decrypted_block]
            decrypted.append(decrypted_block)
        return "".join("".join(i) for i in decrypted)
    def char_to_num(self, char):
        return ord(char) - 65
    def num_to_char(self, num):
        return chr(num + 65)
    def create_matrix(self, key):
        digits = [self.char_to_num(i) for i in key]
        matrix = [digits[(i*3):(i*3)+3] for i in range(3)]
        return matrix
    def is_invertible(self, matrix):
        det = self.det(matrix)
        return not ((det % 2 == 0) or (det % 13 == 0))
    def det(self, matrix):
        return ((matrix[0][0]*((matrix[1][1]*matrix[2][2])-(matrix[1][2]*matrix[2][1])))-(matrix[0][1]*((matrix[1][0]*matrix[2][2])-(matrix[1][2]*matrix[2][0])))+(matrix[0][2]*((matrix[1][0]*matrix[2][1])-(matrix[1][1]*matrix[2][0]))))%26

class JointCipher():
    def __init__(self):
        self.adfgvx = AdfgvxCipher()
        self.hill = HillCipher()
    def encode(self, plaintext, key):
        intermediate_ciphertext = self.adfgvx.encode(plaintext, key[:6], key[7:])
        ciphertext = self.hill.encode(intermediate_ciphertext, key)
        return ciphertext
    def decode(self, ciphertext):
        intermediate_ciphertext = self.hill.decode(ciphertext).replace("Z","")
        plaintext = self.adfgvx.decode(intermediate_ciphertext)
        return plaintext

key = "LSXCPFUDEH"
plaintext = "ASDF MESSAGE 123 "
cipher = JointCipher()
print(plaintext)
ciphertext = cipher.encode(plaintext, key)
print(ciphertext)
decoded = cipher.decode(ciphertext)
print(decoded)