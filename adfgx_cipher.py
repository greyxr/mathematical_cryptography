class AdfgxCipher():
    def prepare_string(self, string):
        return "".join(i.upper() for i in string if i.isalpha()).replace("J","I")
    def create_matrix(self):
        # Create two structures, a list to map coords to letters
        # And a dict to map letters to coords
        letters = dict()
        alpha_set = [i for i in 'ABCDEFGHIKLMNOPQRSTUVWXYZ']
        alpha_set.reverse()
        matrix = [[] for i in range(5)]
        for i in range(25):
            char = alpha_set.pop()
            letters[char] = tuple([i//5, i%5])
            matrix[i//5].append(char)
        # print(letters)
        # print(matrix)
        return matrix, letters
    def create_digrams(self, plaintext):
        digrams = []
        for i in range(0,len(plaintext),2):
            # print(plaintext[i],end="")
            if (i+1 < len(plaintext)):
                if (plaintext[i] == plaintext[i+1]):
                    digrams.append(plaintext[i] + "X")
                    digrams.append(plaintext[i+1] + "X")
                else:
                    digrams.append(plaintext[i] + plaintext[i+1])
            else:
                digrams.append(plaintext[i] + "X")
                # print('X',end=" ")
        # print(digrams)
        return digrams
    def substitute_characters(self, plaintext, letters):
        intermediate = ""
        for i in plaintext:
            intermediate += self.create_digraph(i, letters)
        return intermediate
    def create_digraph(self, char, letters):
        [row, col] = letters[char]
        code = "ADFGX"
        return code[row] + code[col]
    def transpose_columns(self, inter, keyword):
        key_length = len(keyword)
        key_map = {i:[] for i in keyword}
        # Split inter into columns and keep track in a map
        # so we can sort them later
        for i in range(len(inter)):
            current_col = i % key_length
            key_map[keyword[current_col]] = inter[i]
        print(key_map)
        print(sorted(key_map))
        return sorted(key_map)
    def unpose_columns(self, matrix, keyword):
        # I know that's not a word but it's late
        key_map = {i:[] for i in keyword}
        for i in keyword:
            key_map[i] = matrix[i]
        return self.read_matrix(key_map)
    def read_matrix(self, matrix):
        string = []
        # Reverse columns to pop elements more efficiently later
        for i in matrix:
            matrix[i].reverse()
        while any(matrix):
            for col in matrix:
                if col:
                    string.append(matrix[col].pop())
        return "".join(string)
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
    def encode(self, plaintext, key):
        plaintext = self.prepare_string(plaintext)
        matrix, letters = self.create_matrix()
        self.matrix = matrix
        self.letters = letters
        inter = self.substitute_characters(plaintext, letters)

        return encrypted
    def decode(self, ciphertext):
        digrams = self.create_digrams(ciphertext)
        decrypted = ""
        for i in digrams:
            decrypted += self.decrypt_digram(i, self.matrix, self.letters)
        return decrypted
decoder = AdfgxCipher()
# cipher = decoder.encode("Did he play fair at St Andrews golf course.", "cryptography")
# print(cipher)
# print(decoder.decode(cipher))
print(decoder.read_matrix({}, "test"))