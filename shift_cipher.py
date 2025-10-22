ciphertext = "JSBLVULPAZIHKPMVAWBZLKADPJLJSBLADVPMAOLYLHYLADLUAFZPESLAALYZJVBSKILZBIZAJPWOLYRLF"

def rot_n(cipher, n):
    result = ""
    for i in range(len(cipher)):
        if cipher[i] == " ":
            result += " "
        else:
            result += chr(((ord(cipher[i]) - 65 + n) % 26) + 65)
    return result

print(ciphertext)
print("==============================")
for i in range(0,27):
    print(rot_n(ciphertext, i))
    print("------------------------")