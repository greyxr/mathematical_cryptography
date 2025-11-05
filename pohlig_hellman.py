from collections import deque


powers = [(2,250),(3,87)]
p = 584854824268551542129244251215026319737628782638833472789794721613792888584033562290987875013095816415051989792063489
b = 314811926012036328603194721537601297971079834385946685176741300295789282515229688791455667699028070058047553926133593
a = 7


# p = 41
# a = 7
# b = 12
# powers = [(2,3),(5,1)]

# p = 17
# a = 3
# b = 14
# powers = [(2,4)]
# beta = alpha ^ x
coefficient_array = deque()
for q, e in powers:
    coefficients = []
    b_prime = b
    for i in range(1,e+1):
        p_b = (p - 1) // (pow(q,i)) # (p-1)/q^2
        # print("Checking",q,i,q**i,p_b)
        # Use currently calculated b_prime
        # Calculate b_prime^p_b
        b_1 = pow(b_prime,p_b,p)
        # Calculate a^p_b
        a_1 = pow(a,(p-1)//q,p)
        # a_1^x = b_1
        # Calculate coefficient
        # print(a_1,b_1)
        c = None
        for j in range(q):
            if pow(a_1,j,p) == b_1:
                c = j
                break
        if c is None:
            print("Error on", p_b)
            raise Exception("No coefficient found!")
        coefficients.append(c)
        # print("Coefficient:",c)
        # Calculate new b_prime
        a_inverse = pow(a, -c*(q ** (i - 1)), p)
        b_prime = (b_prime * a_inverse) % p
        # print("B prime:", b_prime)
    print(coefficients)
    coefficient_array.append(coefficients)
print(coefficient_array)

# We only have two powers, so we'll hardcode for speed
r = dict()
for q, e in powers:
    c = coefficient_array.popleft()
    total = 0
    for i in range(e):
        total += c[i]*(q**i)
    print(total, "mod", q**e)
    r[(q,e)] = (total, q**e)

d, m = r[powers[0]]
f, n = r[powers[1]]
def crt(a, m, b, n):
    s = pow(m, -1, n)
    t = pow(n, -1, m)
    return (b*m*s + a*n*t) % (m*n)
print("-----------------------")
print(d,m)
print(f,n)
x = (crt(d,m,f,n))
print("---------------------------")
print(pow(a,x,p))
print(b)

r = 553891431805464492215752136984312631355965750286422209988929785591226801297281126703450642772067374488366860252478677
t = 440537370812592640365953595972326957267575952315289419922394022233095769605974972907623517788097251856648133697754275

x_inverse = pow(x,-1,p)
plaintext_num = (t * (pow(r,-x,p))) % p
print(plaintext_num)
plaintext_num = [8, 9, 12, 12, 3, 9, 16, 8, 5, 18, 4, 1, 20, 1, 15, 14, 5, 20, 8, 18, 5, 5, 14, 9, 14, 5, 20, 8, 18, 5, 5, 5, 9, 7, 8, 20, 14, 9, 14, 5, 20, 23, 15, 19, 5, 22, 5, 14, 19, 5, 22, 5, 14]
print("".join(chr(i+64) for i in plaintext_num))

# HILLCIPHERDATAONETHREENINETHREEEIGHTNINETWOSEVENSEVEN