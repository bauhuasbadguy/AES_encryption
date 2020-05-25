#AES python implementation
import math
#This code is really badly written. It was written as an educational
#tool so if you complain about the redundancies then go fuck yourself
#Also if you like code golf your going to hate this. I've got three
#sub-key functions in here when one would do

#Sources:-
#https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
#http://www.crypto-textbook.com/

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~ These are the functions that do all the even slightly
novel mathematical calculations ~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
#These are the functions that do all the even slightly novel mathematical
#calculations

def GF256multiply(A, B):

    #multiply two numbers in the GF(256) field defined by field
    #This works using the peasents multiplication
    p = 0
    #V is the primitve polynomial
    V = 283
    #count through n
    for counter in range(8):
        if (B & 1) == 1:
            #add A to the product if B is odd like you
            #do in the peasents algorithm
            #does'nt hit when B has hit zero
            #to increase speed tell the code to stop
            #when B = 0
            p ^= A

            
        #shift A left
        A = A << 1

        #if A is outside the field use V to put it
        #back in
        if A >= 256:

            A = A ^ V
        #shift B one to the left
        B = B >> 1


    return p

#matrix multiplication in the GF(256) field
def GF256matrixmultiply(A, B):

    C = []

    for i in range(len(A)):

        C.append([])
        
        for l in range(len(B[0])):
            
            a = 0
            
            for j in range(len(A[i])):
                
                a = a ^ (GF256multiply(A[i][j], B[j][l]))

                
            C[i].append(a)
            
    return C
    
#regular matrix multiplication
def matrixmultiply(A, B):
    
    C = []

    for i in range(len(A)):

        C.append([])
        
        for l in range(len(B[0])):
            
            a = 0
            
            for j in range(len(A[i])):
                
                a = a + (A[i][j] * B[j][l])

                
            C[i].append(a)
            
    return C


#find the transpose of a 2D marix
#I could'nt be buggered adding exceptions so
#make sure your matricies are valid
def transpose_matrix(A):
    
    T = []
    for i, element in enumerate(A[0]):

        T.append([])
        for l, line in enumerate(A):
            T[i].append(line[i])

            
    return T


#convert a list of values into the vector/matrix format
def transpose_vector(A):

    T = []
    for i, M in enumerate(A):
        T.append([int(M,2)])

    return T
#convert a hex number into a binary one
def hex2bin(hex_num):
   binary = ['0000','0001','0010','0011',
         '0100','0101','0110','0111',
         '1000','1001','1010','1011',
         '1100','1101','1110','1111']
   
   aa = ''
   for digit in hex_num:
      aa += binary[int(digit,16)]
   return aa

#Convert a number to a binary string of lenth pad_val
def pad_number(number, pad_val):

    #if the input number is less that 32 bits
    #the code returns a 32 bit binary string
    #if the number is more than 32 bits it
    #returns a list of 32 bit intergers
    number = bin(number)[2:]
    startlen = len(number)


    if startlen < pad_val:

        padinglen = pad_val - startlen

        padstring = '0' * padinglen

        number = padstring + number

    elif startlen > pad_val:

        units = int(startlen/pad_val)
        #set up the padding for the left over
        #non-64 bit integer
        extrabit = pad_val - (startlen % pad_val)
        
        pading = '0' * extrabit

        binnumber = pading + number

        number = []
        for i in range(units + 1):
            number.append(binnumber[0:pad_val])
            binnumber = binnumber[pad_val:]


    return number

#convert a number to text using ascii. The number is converted to
#binary and split into bytes. Each byte is 1 character
def num2text(number):

    binnumberlist = pad_number(number, 8)
    text = ''

    for i, binnumber in enumerate(binnumberlist):

        number = int(binnumber, 2)
        letter = chr(number)
        text = text + letter
    
    return text

#convert text to a number by first splitting turning each character
#into a 1 byte number, then a binary string, then combining the strings
#into one long string which is converted into a single large decimal number
def text2num(text):

    result = ''

    for lett in text:

        number = ord(lett)


        result = result + pad_number(number, 8)

    return int(result, 2)

#Converts a string into a list of strings of length
#defined by block_size
def string2blocks(string, block_size):

    #these sections are to show the crazy bug
    #print 'Input:-'
    #print string
    #pad the string if it won't split into nice convinent blocks
    if len(string) % block_size != 0:

        extension = ' ' * (block_size - (len(string) % block_size))
        string = string + extension

    #scroll through and build the blocks saving them when they're
    #long enough
    block = ''
    blocks = []
    for i, lett in enumerate(string):

        block = block + lett

        
        if (len(block) == block_size):

            blocks.append(block)
            block = ''

            
    #these sections are to show you the wierd bug
    #print 'Output:-'
    #print blocks
    #return the list of strings
    return blocks

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~  These are the substutution box functions ~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

def AES_S_box(i):

    #The AES s_box is found by first finding the
    #multiplicative inverse of i in the GF(256) field
    #and then the result of this is turned into a vector and
    #multiplied by a constant bit matrix and the vector result
    #from that is added to the vector (1,1,0,0,0,1,1,0) and the
    #result from that is taken to mod 2. We could calculate all
    #this for every incedence of the AES S-box but it's much more
    #efficient to use a set of pre-calculated values

    #convert the input to a number than can be used as an index
    I = int(i, 2)

    #the S box is in hex because everyone loves hex for some reason and I've
    #copied these boxes off the internet
    S_vector = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]

    return pad_number(S_vector[I], 8)

def AES_inv_S_box(i):

    I = int(i,2)
    #this is the inverse of the S-box. Same principal but now were working in
    #reverse
    Inv_S_vector = [0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D]

    return pad_number(Inv_S_vector[I], 8) 

def RC(i):
    #RC is found using {x^(i-1)} % v where v is the irreducible vector:-
    #100011011
    RC_sbox = [1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154,
    47, 94, 188, 99, 198, 151, 53, 106, 212, 179, 125, 250, 239, 197, 145,
    57, 114, 228, 211, 189]

    return RC_sbox[i]


'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~ These are the functions that generate the keys ~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

#the g function
def g_function(w, round_number):

    V = []
    #do the shuffling step
    V.append(w[8:16])
    V.append(w[16:24])
    V.append(w[24:32])
    V.append(w[0:8])

    #pass all the values through an S_box
    for i, v in enumerate(V):
        V[i] = int(AES_S_box(v), 2)
        

    #XOR V[0] with RC[round number]
    V[0] ^= RC(round_number)


    #recombine the result into a single result string
    result = ''
    for i in range(4):

        result = result + pad_number(V[i], 8)

    #since the only point of g is to return something to
    #be XORed rather than combined the function returns a
    #integer rather than a binary string
    return int(result, 2)

#the H function
def h_function(w):


    V = []
    #split the 32 bit word into 4 bytes
    V.append(w[0:8])
    V.append(w[8:16])
    V.append(w[16:24])
    V.append(w[24:32])


    #pass all the values through an S_box
    for i, v in enumerate(V):
        V[i] = int(AES_S_box(v), 2)
        

    #recombine the result into a single result string
    result = ''
    for i in range(4):

        result = result + pad_number(V[i], 8)

    #since the only point of g is to return something to
    #be XORed rather than combined the function returns a
    #integer rather than a binary string
    return int(result, 2)

#generate the sub-keys when working with a 128 bit key
def gen_128_bit_keys(key):

    if len(key) > 16:

        print("********************************************************")
        print("** Your password is too long. This isn't going to work **")
        print("********************************************************")
    
    #convert the password into a number
    k = text2num(key)

    #convert the password into binary
    k = pad_number(k, 128)


    #set the number of sub keys per round
    wsize = int(128 / 32)

       
    #Create the vector W that will contain the
    #32 bit key words
    W = []


    #first round keys
    for i in range(wsize):
        W.append(k[(i*32):((i*32)+32)])



    for i in range(10):
        
        #little w is the result from the last round in
        #integers for XORing
        w = []
        for l in range(4):

            w.append(int(W[((i*4) + l)], 2))



        g_result = g_function(W[-1], i)

        #do the XORing on the temporay w vector
        w[0] ^= g_result
        w[1] ^= w[0]
        w[2] ^= w[1]
        w[3] ^= w[2]
        
        #save the calculated values for W
        for l in range(len(w)):

            W.append(pad_number(w[l], 32))


    #convert the W keys into decimal intigers for XORing
    for i, w in enumerate(W):

        W[i] = int(w, 2)


    return W

#generate the sub-keys when working with a 192 bit key
def gen_192_bit_keys(key):


    if len(key) > 24:

        print("********************************************************")
        print("** Your passwords is too long. This isn't going to work **")
        print("********************************************************")

    #convert the password into a number
    k = text2num(key)

    #convert the password into binary
    k = pad_number(k, 192)


    #set the number of sub keys per round
    wsize = int(192 / 32)

       
    #Create the vector W that will contain the
    #32 bit key words
    W = []


    #first round keys
    for i in range(wsize):
        W.append(k[(i*32):((i*32)+32)])


    #run through rounds 1:r-1 because the final round is different
    for i in range(7):
        
        #little w is the result from the last round in
        #integers for XORing
        w = []
        for l in range(6):

            w.append(int(W[((i*4) + l)], 2))



        g_result = g_function(W[-1], i)

        #do the XORing on the temporay w vector
        w[0] ^= g_result
        w[1] ^= w[0]
        w[2] ^= w[1]
        w[3] ^= w[2]
        w[4] ^= w[3]
        w[5] ^= w[4]

        #save the calculated values for W
        for l in range(len(w)):

            W.append(pad_number(w[l], 32))

    #now the final round

    w = []
    for l in range(4):

        w.append(int(W[((i*4) + l)], 2))

    g_result = g_function(W[-1], i)

    #do the XORing on the temporay w vector
    w[0] ^= g_result
    w[1] ^= w[0]
    w[2] ^= w[1]
    w[3] ^= w[2]

    #save the calculated values for W
    for l in range(len(w)):

        W.append(pad_number(w[l], 32))
            
    #convert the W keys into decimal intigers for XORing
    for i, w in enumerate(W):

        W[i] = int(w, 2)

    return W

#generate the sub-keys when working with a 256 bit key
def gen_256_bit_keys(key):

    if len(key) > 32:

        print("********************************************************")
        print("** Your passwords is too long. This isn't going to work **")
        print("********************************************************")

    #convert the password into a number
    k = text2num(key)

    #convert the password into binary
    k = pad_number(k, 256)


    #set the number of sub keys per round
    wsize = int(256 / 32)

       
    #Create the vector W that will contain the
    #32 bit key words
    W = []


    #first round keys
    for i in range(wsize):
        W.append(k[(i*32):((i*32)+32)])


    #run through rounds 1:r-1 because the final round is different
    for i in range(6):
        
        #little w is the result from the last round in
        #integers for XORing
        w = []
        for l in range(8):

            w.append(int(W[((i*4) + l)], 2))

        g_result = g_function(W[-1], i)
        h_result = h_function(W[-5])

        #do the XORing on the temporay w vector
        w[0] ^= g_result
        w[1] ^= w[0]
        w[2] ^= w[1]
        w[3] ^= w[2]
        w[4] ^= h_result
        w[5] ^= w[4]
        w[6] ^= w[5]
        w[7] ^= w[6]

        #save the calculated values for W
        for l in range(len(w)):

            W.append(pad_number(w[l], 32))

    #now the final round

    w = []
    for l in range(4):

        w.append(int(W[((i*4) + l)], 2))

    g_result = g_function(W[-1], i)

    #do the XORing on the temporay w vector
    w[0] ^= g_result
    w[1] ^= w[0]
    w[2] ^= w[1]
    w[3] ^= w[2]


    #save the calculated values for W
    for l in range(len(w)):

        W.append(pad_number(w[l], 32))
 
    #convert the W keys into decimal intigers for XORing
    for i, w in enumerate(W):

        W[i] = int(w, 2)

    return W

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~ These are the functions used for the steps of the algorithm ~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

#first XOR the split up message with the sub keys
def first_key_addition(message, W):

    #convert the message into binary

    m = text2num(message)

    #convert the password into binary
    m = pad_number(m, 128)


    #split the message up
    M = []
    for i in range(4):

        M.append(int(m[(i*32):((i*32) + 32)],2))

        
    #first XOR key round, here we're XORing with just the
    #key on its own

    for i in range(len(M)):

        #XOR with the key section
        M[i] ^= W[i]
        #turn the result back into binary
        M[i] = pad_number(M[i], 32)


    return M

#then move through a s-box
def byte_substitution(M):
    #I think this might be 90o to what it should be 
    
    #I think this is:-
    #b0, b1, b2, b3
    #b4, b5, b6, b7,
    #b8, b9, b10, b11
    #b12, b13, b14, b15
    
    #when it is meant to be 
    #b0, b4, b8, b12
    #b1, b5, b9, b13
    #b2, b6, b10, b14
    #b3, b7, b11, b15
    
    #This should be noted but I'm not sure how
    #important it is to the overall process so I'll
    #leave it as it is for now

    for i in range(len(M)):

        t = []

        for l in range(4):

            t.append(M[i][(l*8):((l*8) + 8)])

            t[l] = AES_S_box(t[l])


        #save the bytes in a list
        M[i] = t

    return M

#then do the shift rows
def shift_rows(M):


    #turn the M values into a matrix
    T = transpose_matrix(M)


    #shuffle the bytes
    M = [[T[0][0], T[0][1], T[0][2], T[0][3]],
         [T[1][1], T[1][2], T[1][3],T[1][0]],
         [T[2][2], T[2][3], T[2][0], T[2][1]],
         [T[3][3], T[3][0], T[3][1],T[3][2]]]


    #convert everything into intigers for the next step

    return M

#finally the mix column step. This is basically a matrix
#multiply in GF(256)
def mix_col(M):

    #define the mixing matrix to be used
    Mix_matrix = [[2, 3, 1, 1],
                  [1, 2, 3, 1],
                  [1, 1, 2, 3],
                  [3, 1, 1, 2]]

    #convert everything into integers for the next step
    for i, row in enumerate(M):

        for l, val in enumerate(row):

            M[i][l] = int(val, 2)

    

    #use a matrix multiplication in GF(256) to do the step
    C = GF256matrixmultiply(Mix_matrix, M)

    #convert to binary after the mixing to recombine the
    #words
    for i, row in enumerate(C):

        for l, val in enumerate(row):
            C[i][l] = pad_number(val,8)
            

    #recombine the matrix back into a 4 32 bit numbers
    M = []
    for i, col in enumerate(C[0]):

        m = ''
        
        for l, row in enumerate(C):

            m = m + C[l][i]

        M.append(int(m, 2))


    return M

#add the keys to the mixed data
def Key_addition(M, W, r):

    #do the XOR
    for i, v in enumerate(M):

        M[i] ^= W[((r+1)*4)+i]

    #turn it back into binary to prepare it for the next round
    for i,v in enumerate(M):
        
        M[i] = pad_number(v,32)

    return M



'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~ Now the inverse of the encryption functions ~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

#do the inverse of the first key addition in the forwards
#routine
def last_inv_key_addition(M, W):

    c = []
    for i in range(4):

        c.append(int(M[i],2))

    C = ''
    for i in range(4):

        c[i] ^= W[i]

        c[i] = pad_number(c[i], 32)

        C = C + c[i]

    C = int(C,2)

    C = num2text(C)

    return C



#inverse of the byte substitution step
def Inv_byte_substitution(M):

    c = []
    for i in range(len(M)):

        for l in range(len(M[i])):

            t = M[i][l]

            c.append(AES_inv_S_box(t))

    #This is where we convert to a matrix

    C = []
    for i in range(4):
        m = ''
        for l in range(4):

            m = m + c[(4*i)+l]

        C.append(m)
    
    return C



#inverse of the column mixing step
def Inv_mix_col(M):

    #define the mixing matrix to be used
    Inv_Mix_matrix = [[0x0E, 0x0B, 0x0D, 0x09],
              [0x09, 0x0E, 0x0B, 0x0D],
              [0x0D, 0x09, 0x0E, 0x0B],
              [0x0B, 0x0D, 0x09, 0x0E]]


    #convert to binary
    for i in range(len(M)):
        M[i] = pad_number(M[i], 32)

    #convert the 4 32 bit words into a matrix

    m = []

    for i in range(4):
        row = []
        for l in range(4):
        
            row.append(M[i][(l*8):((l*8)+8)])

        m.append(row)



    #transpose the matrix
    M = transpose_matrix(m)



    #convert everything into integers for the next step
    for i, row in enumerate(M):

        for l, val in enumerate(row):

            M[i][l] = int(val, 2)



    #use a matrix multiplication in GF(256) to do the step
    C = GF256matrixmultiply(Inv_Mix_matrix, M)

    #convert to binary after the mixing to recombine the
    #words
    for i, row in enumerate(C):

        for l, val in enumerate(row):
            C[i][l] = pad_number(val,8)
            

    return C

#inverse of the shift rows step
def Inv_shift_rows(T):

    #turn the M values into a matrix
    #T = M

    #shuffle the bytes
    M = [[T[0][0], T[0][1], T[0][2], T[0][3]],
         [T[1][3], T[1][0], T[1][1], T[1][2]],
         [T[2][2], T[2][3], T[2][0], T[2][1]],
         [T[3][1], T[3][2], T[3][3], T[3][0]]]

    #return it to the format where the words are represented by
    #rows not columns. I know this is horrible coding and makes
    #it hard to understand but fixing it would be a big job so
    #fuck you. I'm on a deadline here
    M = transpose_matrix(M)

    #convert everything into intigers for the next step

    return M

#invertion of the key addition step
def Inv_key_addition(M, W, r):

    C = []
    for i in range(len(M)):
        C.append(int(M[i],2))

    #invert the XOR
    for i, v in enumerate(M):

        C[i] ^= W[((r+1)*4)+i]

    return C

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~ Combine all those steps into encryption and decryption steps ~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
#Encrypt a single block using AES
def AES_encrypt_block(message, W):
    
    M = first_key_addition(message, W)
    
    print('AFTER FIRST KEY ADDITION')
    print(M)
    print('----')

    if len(W) == 44:
        rounds = 10
    elif len(W) == 52:
        rounds = 12
    elif len(W) == 60:
        rounds = 14


    for r in range(rounds):

        #now enter the round functions
        
        print('BEOFRE BYTE SUBSTITUTION')
        print(M)
        print('---')

        #byte substitution step, this also converts to a matrix
        M = byte_substitution(M)
        
        print('AFTER BYTE SUBSTITUTION')
        print(M)
        print('++++')


        #Shift rows step
        M = shift_rows(M)


        #mix columns step
        M = mix_col(M)
        

        #now XOR with the key
        M = Key_addition(M,W, r)


    #recombine the binary strings to make the cypher-text
    C = ''
    for i in range(len(M)):
        C = C + M[i]

    bin_C = C
    
    C = int(C, 2)


    C = num2text(C)

    #print '##########'
    #print bin_C
    #print '##########'

    return [bin_C, C]


#this takes in a binary string and converts it into a decrypted binary string
#and decrytped text
def AES_decrypt_block(cyphertext, W):
    #c = pad_number(text2num(cyphertext), 128)
    c = cyphertext
    p = []

    for i in range(4):

        p.append(c[(i*32):((i*32)+32)])



    if len(W) == 44:
        rounds = 10
    elif len(W) == 52:
        rounds = 12
    elif len(W) == 60:
        rounds = 14


    for R in range(rounds):
        #reverse the rounds index because we're going
        #backwards
        r = rounds - R - 1

        #now enter the round functions

        #inverse XOR
        p = Inv_key_addition(p, W, r)

        #inverse mix columns
        p = Inv_mix_col(p)

        #inverse shift rows
        p = Inv_shift_rows(p)

        #inverse byte substitution

        p = Inv_byte_substitution(p)


    #remove the first key and convert to plain text

    p = last_inv_key_addition(p, W)

    #convert into a binary string for the next step
    bin_p = pad_number(text2num(p), 128)

    
    return [bin_p, p]

#takes in a message string and outputs a hex cypher number as well as
#a cypher string for debugging.
def AES_encrypt(plain_text, password, key_length = 128):


    #check the password is the right length
    if len(password) > key_length/8:

        if (len(password) > 16) and (len(password) <= 24):
            print('Your password is too long. Reverting to AES-192')
            key_length = 192
        elif (len(password) > 24) and (len(password) <= 32):
            print('Your password is too long. Reverting to AES-256')
            key_length = 256
        elif (len(password) > 32):
            raise Exception('Your password is too long, consider shortening it')

    if key_length not in [128, 192, 256]:
        raise Exception('You have to use a key length of 128,192 or 256.')



    #generate the sub-keys
    if key_length == 128:

        W = gen_128_bit_keys(password)

    elif key_length == 192:

        W = gen_192_bit_keys(password)

    elif key_length == 256:

        W = gen_256_bit_keys(password)


    P = string2blocks(plain_text,16)

    #build up a binary string representing the cyphertext
    C = ''
    text = []
    for i, p in enumerate(P):

        p1 = p
        
        C = C + AES_encrypt_block(p1, W)[0]
        text.append(AES_encrypt_block(p1, W)[1])

    bin_C = C
    hex_C = hex(int(C,2))

    #create the cypher text, this is just to look at since it will
    #contain characters that will interfer with the string function
    Cypher_text = ''

    for i, c in enumerate(text):

        Cypher_text = Cypher_text + c


    return [bin_C, hex_C, Cypher_text]

#takes in a binary cyphertext and outputs a hex plaintext as well as the
#actual text
def AES_decrypt(Cypher_text, password, key_length = 128):

    #check the password is the right length
    if len(password) > key_length/8:

        if (len(password) > 16) and (len(password) <= 24):
            print('Your password is too long. Reverting to AES-192')
            key_length = 192
        elif (len(password) > 24) and (len(password) <= 32):
            print('Your password is too long. Reverting to AES-256')
            key_length = 256
        elif (len(password) > 32):
            raise Exception('Your password is too long, consider shortening it')

    if key_length not in [128, 192, 256]:
        raise Exception('You have to use a key length of 128,192 or 256.')



    #Generate the sub keys epending on the key length
    if key_length == 128:

        W = gen_128_bit_keys(password)

    elif key_length == 192:

        W = gen_192_bit_keys(password)

    elif key_length == 256:

        W = gen_256_bit_keys(password)

    #split the cypher text into blocks
    C = []
    for i in range(int(len(Cypher_text)/128)):

        C.append(Cypher_text[(i*128):((i*128)+128)])


    #decrypt the blocks
    P = []
    Plain_text = ''
    for i, c in enumerate(C):

        c1 = c
        P.append(AES_decrypt_block(c1, W)[0])
        Plain_text = Plain_text + AES_decrypt_block(c1, W)[1]



    return [P, Plain_text]
        

######################
## end of functions ##
######################

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~ Here are some example key generations ~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

#experemental 128 bit key
key = 'Shh,tis a secret'
W = gen_128_bit_keys(key)


#experemental 192 bit key
key = "Shh, it's still a secret"
W = gen_192_bit_keys(key)


#experemental 256 bit key
key = "Shh,this one's super secret,stum"
W = gen_256_bit_keys(key)



print('========================================')


message = 'Secret message:1, this is secret'
block_size = 16


password = 'spongegsdfsdafds'

#the encryption function
[bin_C, hex_C, Cypher_text] = AES_encrypt(message, password, 256)

#the decryption function
[P, Plain_text] = AES_decrypt(bin_C, password, 256)


print(Plain_text)



