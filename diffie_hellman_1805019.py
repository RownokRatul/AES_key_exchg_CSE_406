import random
from timeit import default_timer
from tabulate import tabulate

from prime_functionalities_1805019 import *


elapsed_time = []


def Diffie_Hellman_exchange(key_len) :
    # public key bases
    time_p_start = default_timer()
    p = generateSafePrime(key_len)
    time_p_end = default_timer()
    g = primitiveRootSafePrime(p, 2, p-2)
    time_g_end = default_timer()
    # print("p, g:", p, g)
    # Alice
    red = random.randrange(0, key_len//2)
    time_a_start = default_timer()
    a = generatePrime(key_len - red)
    time_a_end = default_timer()
    A = modularExponentiation(g, a, p)
    time_A_end = default_timer()
    # print("Alice:", a, A)
    # Bob
    red = random.randrange(0, key_len//2)
    time_b_start = default_timer()
    b = generatePrime(key_len - red)
    time_b_end = default_timer()
    B = modularExponentiation(g, b, p)
    time_B_end = default_timer()
    # print("Bob:", b, B)

    # let the key has been exchanged

    # Alice's retrieval
    timer_ka_start = default_timer()
    ka = modularExponentiation(B, a, p)
    timer_ka_end = default_timer()
    # print("Alice gets:", ka)
    # Bob's retrieval
    timer_kb_start = default_timer()
    kb = modularExponentiation(A, b, p)
    timer_kb_end = default_timer()
    # print("Bob gets:", kb)

    if ka == kb :
        print("Successfully key exchanged: ", ka)
    
    elapsed_time.append([key_len, (time_p_end-time_p_start)*1000, (time_g_end-time_p_end)*1000, (time_a_end-time_a_start)*1000, (time_A_end-time_a_end)*1000, (time_b_end-time_b_start)*1000, (time_B_end-time_b_end)*1000, (timer_ka_end-timer_ka_start)*1000])


# test Diffie Hellman
def printTimeSummary() :
    print(tabulate(elapsed_time, headers=["Key-Length", "p", "g", "a", "A", "b", "B", "Shared Key"], floatfmt=".4f", tablefmt="simple_grid"))


def test() :
    for i in [128, 192, 256] :
        Diffie_Hellman_exchange(i)
    printTimeSummary()

# test()
