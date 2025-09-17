import numpy as np

class VignereCipher():
    def prepare_string(self, ciphertext):
        return "".join(i.upper() for i in ciphertext if i.isalpha())
    def encode(self, plaintext, key):
        ciphertext = ""
        for i in range(len(plaintext)):
            plaintext = self.prepare_string(plaintext)
            current_key_char = i % len(key)
            encoded_char = self.encode_char(plaintext[i], key[current_key_char])
            ciphertext += encoded_char
        self.ciphertext = ciphertext
        return ciphertext
    def encode_char(self, char, key_char):
        num_char = self.standardize_char(char)
        num_key_char = self.standardize_char(key_char)
        return self.ascii_char((num_char + num_key_char) % 26) 
    def find_coincidences(self, displacement):
        count = 0
        for i in range(displacement, len(self.ciphertext)):
            if (self.ciphertext[i-displacement] == self.ciphertext[i]):
                count += 1
        return count  
    def find_key_length(self):
        key_length, max_displacement = 0, 0
        for i in range(1,7):
            coincidences = self.find_coincidences(i)
            if (coincidences > max_displacement):
                max_displacement = coincidences
                key_length = i
        return key_length
    def standardize_char(self, char):
        return ord(char) - 65
    def ascii_char(self, num):
        return chr(num + 65)
    def shift_vector(self, vec, displacement):
        new_vec = [0 for i in range(len(vec))]
        for i in range(len(vec)):
            new_vec[i] = vec[i-displacement]
        return new_vec
    def calc_freq_vector(self, key_length, displacement):
        v = [0 for i in range(26)]
        w = [0 for i in range(26)]
        # Set v to count of every key_length + displacement
        count = 0
        for i in range(displacement, len(self.ciphertext), key_length):
            char_num = self.standardize_char(self.ciphertext[i])
            v[char_num] += 1
            count += 1
        for i in range(len(v)):
            w[i] = v[i]/count
        return w
    def get_max_freq(self, w):
        a_0 = np.array([0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020, 0.061, 0.070, 0.002, 0.008, 0.040, 0.024, 0.067, 0.075, 0.019, 0.001, 0.060, 0.063, 0.091, 0.028, 0.010, 0.023, 0.001, 0.020, 0.001])
        w = np.array(w)
        max_freq, max_disp = 0, 0
        for i in range(26):
            a_n = self.shift_vector(a_0, i)
            current = round(np.dot(w, a_n),3)
            if current > max_freq:
                max_freq = current
                max_disp = i
        return max_disp
    def get_key_char_num(self, key_length, displacement):
        w = self.calc_freq_vector(key_length, displacement)
        max_disp = self.get_max_freq(w)
        return max_disp
    def get_key(self, ciphertext=None):
        if ciphertext is not None:
            self.ciphertext = self.prepare_string(ciphertext)
        key_length = self.find_key_length()
        key = ""
        for i in range(key_length):
            char_num = self.get_key_char_num(key_length, i)
            key += self.ascii_char(char_num)
        return key
    def decode_string(self, ciphertext, key):
        if (self.ciphertext is None):
            self.ciphertext = self.prepare_string(ciphertext)
        decoded_string = ""
        for i in range(len(self.ciphertext)):
            current_key_char = i % len(key)
            decoded_char = self.decode_char(self.ciphertext[i], key[current_key_char])
            decoded_string += decoded_char
        return decoded_string
    def decode_char(self, char, key_char):
        num_char = self.standardize_char(char)
        num_key_char = self.standardize_char(key_char)
        return self.ascii_char((num_char - num_key_char) % 26)      
    def crack_code(self, ciphertext):
        self.ciphertext = self.prepare_string(ciphertext)
        key = self.get_key()
        decoded_string = self.decode_string(ciphertext, key)
        return decoded_string
ciphertext = "VVHQWVVRHMUSGJGTHKIHTSSEJCHLSFCBGVWCRLRYQTFSVGAHWKCUHWAUGLQHNSLRLJSHBLTSPISPRDXLJSVEEGHLQWKASSKUWEPWQTWVSPGOELKCQYFNSVWLJSNIQKGNRGYBWLWGOVIOKHKAZKQKXZGYHCECMEIUJOQKWFWVEFQHKIJRCLRLKBIENQFRJLJSDHGRHLSFQTWLAUQRHWDMWLGUSGIKKFLRYVCWVSPGPMLKASSJVOQXEGGVEYGGZMLJCXXLJSVPAIVWIKVRDRYGFRJLJSLVEGGVEYGGEIAPUUISFPBTGNWWMUCZRVTWGLRWUGUMNCZVILE"
plaintext = "THEMETHODUSEDFORTHEPREPARATIONANDREADINGOFCODEMESSAGESISSIMPLEINTHEEXTREMEANDATTHESAMETIMEIMPOSSIBLEOFTRANSLATIONUNLESSTHEKEYISKNOWNTHEEASEWITHWHICHTHEKEYMAYBECHANGEDISANOTHERPOINTINFAVOROFTHEADOPTIONOFTHISCODEBYTHOSEDESIRINGTOTRANSMITIMPORTANTMESSAGESWITHOUTTHESLIGHTESTDANGEROFTHEIRMESSAGESBEINGREADBYPOLITICALORBUSINESSRIVALSETC"
decoder = VignereCipher()
cipher = decoder.encode(plaintext, "CODES")
print("----------------------------------------")
print(cipher)
print("----------------------------------------")
print(decoder.decode_string(cipher, "CODES"))
print("----------------------------------------")
print(decoder.crack_code(cipher))