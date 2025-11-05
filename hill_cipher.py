import numpy as np
from sympy import Matrix

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
    def decode(self, ciphertext, matrix=None):
        matrix = matrix if matrix is not None else self.matrix
        inv_matrix = Matrix(matrix).inv_mod(26).tolist()
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

hill = HillCipher()
print(hill.decode("FOPDDXIJDVALPKGRSUJNBDJUKSENABVNYBUDMKEEADWMEASI", [[1,3,9],[3,8,9],[2,7,7]]))

# IFELGAMALENCRYPTSLLAMALLAMAGREENPAJAMAANDREUSESK