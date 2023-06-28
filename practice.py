from random import randrange, getrandbits
def is_prime(n, k=100):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    # print(s, r)
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        print(a, x)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                # print(j)
                # print(x)
                x = pow(x, 2, n)
                print("inside-> ", x)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True

print(is_prime(13))

# def generate_prime_candidate(length):
#     """ Generate an odd integer randomly
#         Args:
#             length -- int -- the length of the number to generate, in bits
#         return a integer
#     """
#     # generate random bits
#     p = getrandbits(length)
#     # apply a mask to set MSB and LSB to 1
#     p |= (1 << length - 1) | 1
#     return p
# def generate_prime_number(length=1024):
#     """ Generate a prime
#         Args:
#             length -- int -- length of the prime to generate, in          bits
#         return a prime
#     """
#     p = 4
#     # keep generating while the primality test fail
#     while not is_prime(p, 128):
#         p = generate_prime_candidate(length)
#     return p
