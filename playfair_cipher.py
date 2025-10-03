class PlayfairCipher():
    def prepare_string(self, string):
        return "".join(i.upper() for i in string if i.isalpha()).replace("J","I")
    def create_matrix(self, key):
        # Create two structures, a list to map coords to letters
        # And a dict to map letters to coords
        letters = dict()
        key_list = []
        for i in self.prepare_string(key):
            if i not in key_list:
                key_list.insert(0,i)
        # print(key_list)
        alpha_set = [i for i in 'ABCDEFGHIKLMNOPQRSTUVWXYZ']
        alpha_set.reverse()
        matrix = [[] for i in range(5)]
        for i in range(25):
            # If letter in key exists and hasn't been added add it
            if len(key_list) > 0:
                char = key_list.pop()
                alpha_set.remove(char)
            else:
            # Otherwise add a letter at random from the rest of the alphabet
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
    def decrypt_digram(self, digram, matrix, letters):
        [frow, fcol] = letters[digram[0]]
        [srow, scol] = letters[digram[1]]
        new_frow, new_fcol, new_srow, new_scol = 0, 0, 0, 0
        if frow == srow:
            new_frow, new_fcol, new_srow, new_scol = frow,(fcol-1)%5,srow,(scol-1)%5
        elif fcol == scol:
            new_frow, new_fcol, new_srow, new_scol = (frow-1)%5,fcol,(srow-1)%5,scol
        else:
            new_frow, new_fcol, new_srow, new_scol = frow,scol,srow,fcol
        return matrix[new_frow][new_fcol] + matrix[new_srow][new_scol]
    def encode(self, plaintext, key):
        plaintext = self.prepare_string(plaintext)
        digrams = self.create_digrams(plaintext)
        matrix, letters = self.create_matrix(key)
        self.matrix = matrix
        self.letters = letters
        encrypted = ""
        for i in digrams:
            encrypted += self.encrypt_digram(i, matrix, letters)
        return encrypted
    def decode(self, ciphertext):
        digrams = self.create_digrams(ciphertext)
        decrypted = ""
        for i in digrams:
            decrypted += self.decrypt_digram(i, self.matrix, self.letters)
        return decrypted
decoder = PlayfairCipher()
cipher = decoder.encode("Did he play fair at St Andrews golf course.", "cryptography")
print(cipher)
print(decoder.decode(cipher))