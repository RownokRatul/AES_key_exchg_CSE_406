import random

def modularExponentiation(b, p, m) :
    # print(b, p, m)
    if p == 0 :
        return 1
    elif p & 1 :
        temp = modularExponentiation(b, (p-1)//2, m)
        return (temp*temp*b) % m
    else :
        temp = modularExponentiation(b, p//2, m)
        return (temp*temp) % m


def Miller_Rabin(p, max_iter=100) : 
    if p == 2 :
        return True
    s = 0
    r = p - 1
    while (r & 1) == 0 :
        s += 1
        r >>= 1
    for i in range(max_iter) :
        a = random.randrange(2, p-1)
        rem = modularExponentiation(a, r, p)
        if rem != 1 and rem != p-1 : 
            for j in range(1, s) :
                rem = modularExponentiation(rem, 2, p)
                if rem == 1 :
                    return False
            if rem != p-1 :
                return False     
    return True
    

def safePrimeCandidate(n):
    # generate a random odd integer of n bits
    p = random.getrandbits(n)
    p = ((1 << n-1) | 1) | p
    # print(bin(p))
    return p


# main
def test() :
    # arr = list(map(int, input().strip().split()))
    # f = modularExponentiation(3, 10, 4)
    p = (safePrimeCandidate(127) << 1) + 1
    while Miller_Rabin(p) == False : 
        p = (safePrimeCandidate(127) << 1) + 1
    print(p)

test()
