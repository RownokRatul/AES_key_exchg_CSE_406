from Sbox import *
from timeit import default_timer

times = []

def print_time_summary() :
    print("\nExecution Time Details: (seconds)")
    print("Key Scheduling:", times[0])
    print("Encryption:", times[1])
    print("Decryption:", times[2])


def printText_HEX(str) :
    print("------------------------")
    print("In ASCII: ", str)
    print("In HEX: ", BitVector(textstring=str).get_bitvector_in_hex())
    print("------------------------")


def print_word(w) : 
    print(hex(w[0]), hex(w[1]), hex(w[2]), hex(w[3]))


def print_matrix(m) :
    for row in range(len(m)) :
        print_word(m[row])


def chunks(s, sz) :
    return [s[i:i+sz] for i in range(0, len(s), sz)]


def pad_string(str, padding_char) : 
    # print(len(str))
    if len(str) % 16 == 0 :
        return str
    padded = str + (16 - (len(str) % 16))*padding_char
    return padded


def hex_to_grid_16(str) : 
    word_div = []
    for i in range(len(str)//8) : 
        quad_bytes = str[i*8 : i*8 + 8]
        word = []
        for j in range(4):
            word.append(int(quad_bytes[j*2 : j*2+2], 16))
        word_div.append(word)
    return word_div


def grid_16_to_hex(m) :
    s = ""
    m = transpose_matrix(m)
    for i in range(len(m)):
        for j in range(len(m)):
            s += str(hex(m[i][j])[2:].zfill(2))
    return s

def rotateWord(data, offset) : 
    return data[offset:]+data[:offset]


def sbox_substitute_word(word) : 
    return [Sbox[i] for i in word]


def xor_word(w1, w2) :
    return [byte1 ^ byte2 for byte1, byte2 in zip(w1, w2)]


def add_round_key(m1, m2) :
    res = []
    for row in range(len(m1)):
        res.append(xor_word(m1[row], m2[row]))
    return res


def transpose_matrix(w) :
    return [[w[j][i] for j in range(len(w))] for i in range(len(w[0]))]


def key_schedule_aes(key, rounds) :
    # 32 bit words
    word_size = 4
    rcon = [[1, 0, 0, 0]]
    for i in range(1, rounds-1):
        rcon.append([rcon[-1][0]*2, 0, 0, 0])
        if rcon[-1][0] > 0x80:
            rcon[-1][0] ^= 0x11b

    init_key = hex_to_grid_16(key)
    
    for i in range(4*rounds) :
        temp = [] 
        if i < word_size :
            continue
        if (i >= word_size) and (i % word_size == 0) :
            temp = xor_word(xor_word(sbox_substitute_word(rotateWord(init_key[-1], 1)), init_key[i-word_size]), rcon[(i//word_size) - 1])
            # print_word(temp)
        elif (i >= word_size) and word_size > 6 and (i % word_size == 4) :
            temp = xor_word(init_key[i-word_size], sbox_substitute_word(init_key[-1]))
        else :
            temp = xor_word(init_key[i-word_size], init_key[-1])

        init_key.append(temp)
    return init_key


def sbox_substitute_matrix(m) :
    return [sbox_substitute_word(row) for row in m]


def matrix_circular_shift(m) :
    temp = []
    for i in range(len(m)):
        temp.append(rotateWord(m[i], i))
    return temp


def mixColumns(mixer, state) :
    AES_modulus = BitVector(bitstring='100011011')
    # print(mixer)
    out = []
    for i in range(len(mixer)):
        row = []
        for j in range(len(mixer)):
            entry = 0
            for k in range(len(mixer)):
                entry ^= int((mixer[i][k].gf_multiply_modular(BitVector(intVal=state[k][j], size=8), AES_modulus, 8)).get_bitvector_in_hex(), 16)
            row.append(entry)
        out.append(row)
    return out


def matrix_encrypt(state, sched_keys, rounds):
    round_key = transpose_matrix(sched_keys[0:4])
    intermediate_matrix = add_round_key(state, round_key)
    for current_round in range(rounds-1):
        t = sbox_substitute_matrix(intermediate_matrix)
        t = matrix_circular_shift(t)
        # print_matrix(t)
        if (current_round != rounds-2) :
            t = mixColumns(Mixer, t)
        
        t = add_round_key(t, transpose_matrix(sched_keys[(current_round+1)*4 : (current_round+1)*4 + 4]))
        intermediate_matrix = t

    # print_matrix(intermediate_matrix)
        
    return intermediate_matrix


def encrypt_aes128(plain, key) :
    cipher = "" 
    padded = pad_string(plain, ' ')
    plainChunks = chunks(padded, 16)
    # print(plainChunks)
    modified_key = chunks(pad_string(key, '0'), 16)[0]

    start = default_timer()
    sched_keys = key_schedule_aes(modified_key.encode("utf-8").hex(), 11)
    end = default_timer()
    times.append(end-start)

    start = default_timer()
    for each in range(len(plainChunks)) : 
        rowMajor = hex_to_grid_16(plainChunks[each].encode("ASCII").hex())
        stateMatrix = transpose_matrix(rowMajor)
        final_ecrypted_matrix = matrix_encrypt(stateMatrix, sched_keys, 11)
        cipher += BitVector(hexstring=grid_16_to_hex(final_ecrypted_matrix)).get_bitvector_in_ascii()
    end = default_timer()
    times.append(end-start)

    # print(cipher)
    return cipher


def sender_test() :
    print("Enter: plain text")
    str = input()
    print("Enter: key")
    key = input()
    print("Plain Text:")
    printText_HEX(str)
    print("Key:")
    printText_HEX(key)
    cipher = encrypt_aes128(str, key)
    # send
    receiver_test(cipher, key)


def inverse_sbox_substitute_word(w): 
    return [InvSbox[i] for i in w]


def inverse_sbox_substitute_matrix(m) :
    return [inverse_sbox_substitute_word(row) for row in m]


def inverse_matrix_circular_shift(m) :
    temp = []
    for row in range(len(m)):
        temp.append(rotateWord(m[row], len(m)-row))
    return temp


def inverse_mixColumns(inv_mixer, state):
    return mixColumns(inv_mixer, state)


def matrix_decrypt(state, sched_keys, rounds) :
    round_key = transpose_matrix(sched_keys[len(sched_keys)-4 : len(sched_keys)])
    decrypting_matrix = add_round_key(state, round_key)
    for current_round in range(rounds-1) : 
        t = inverse_matrix_circular_shift(decrypting_matrix)
        t = inverse_sbox_substitute_matrix(t)
        t = add_round_key(t, transpose_matrix(sched_keys[len(sched_keys)-4*(current_round+2) : len(sched_keys)-4*(current_round+2)+4]))
        if (current_round != rounds-2):
            t = inverse_mixColumns(InvMixer, t)
        decrypting_matrix = t
        # break
        
    # print("Finally: ")
    # print_matrix(decrypting_matrix)
    return decrypting_matrix

def decrypt_aes128(cipher, key) :
    plain = ""
    padded = pad_string(cipher, ' ')
    cipherChunks = chunks(padded, 16)
    print(cipherChunks)
    modified_key = chunks(pad_string(key, '0'), 16)[0]
    sched_keys = key_schedule_aes(modified_key.encode("utf-8").hex(), 11)

    start = default_timer()
    for each in range(len(cipherChunks)) :
        rowMajor = hex_to_grid_16(BitVector(textstring=cipherChunks[each]).get_bitvector_in_hex()) 
        stateMatrix = transpose_matrix(rowMajor)
        final_decrypted_matrix = matrix_decrypt(stateMatrix, sched_keys, 11)
        decrypted_hex = grid_16_to_hex(final_decrypted_matrix)
        plain += BitVector(hexstring=decrypted_hex).get_bitvector_in_ascii()
    end = default_timer()
    times.append(end-start)

    return plain


def receiver_test(cipher, key) :
    print("Cipher Text:")
    printText_HEX(cipher)
    print("Decipher Text:")
    plainText = decrypt_aes128(cipher, key)
    printText_HEX(plainText)
    print_time_summary()


sender_test()