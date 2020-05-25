## README ##

This repo contains code for performing AES in python. It supports AES128, 192 and 256. I wrote this code to improve my understanding of the AES algorithm and I hope it will be helpful to you in the same way but please do not attempt to use this code for real world encryption.


## IMPORTANT NOTE !!! ##

I am just some guy in a room, I have no training in cryptography and this code has not been checked by anyone with real training in cryptography. Please do not use this code for any real encryption purposes. I hope you will find this document informative and that the code may be helpful to you in understanding the AES algorithm but please do not attempt to use this code for real world encryption.

## Algorithm description ##

The first step is to create a list of subkeys which will be used in the encryption. 

### Subkey generation ###

# SECTION UNFINISHED #

| i              | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 |
|----------------|----|----|----|----|----|----|----|----|----|----|
| rc<sub>i</sub> | 01 | 02 | 04 | 08 | 10 | 20 | 40 | 80 | 1B | 36 |


### Encryption procedure ###

The first step of encryption is to covert the 128 bit block into a 4X4 matrix of 8 bit words. This is done by dividing the 128 bit input block into 16, 8 bit words as shown below

M = m<sub>0</sub>, m<sub>1</sub>, ..., m<sub>15</sub>

 which are then mapped onto the 4X4 matrix as shown in the diagram below

<p>
<image src = './images/mapping_block_to_matrix.png' width="200px;"></image>
</p>


This 4X4 matrix is XORed with the the first of the subkeys and the result is sent to the rounds encryption system.

The number of rounds is set by the key length with the number rounds for each key length shown in the table below.

| Key length | Rounds |
|------------|--------|
| 128        | 10     |
| 192        | 12     |
| 256        | 14     |

Each of these rounds consists of 4 steps, except for the final round which foregoes the final step. The for steps are:

* The subBytes step
* The ShiftRows step
* The MixColumns step
* the AddRoundKey step

This procedure is shown in a very basic block diagram below

<p align="center">
<image src = './images/AES_block_diagram.png' width="500px;"></image>
</p>


We will now discus each of these steps in turn.

#### subBytes step ####

This step can be further subdivied into two sub steps. In the first step the multiplicative inverse of each element of the 4X4 matrix is found. Next the affine transformation is applied to each byte. These steps can be performed as a single substitution box applied to each byte since each byte is only 8 bits long however in a memory constrained environment the calculation could be performed for each byte in the matrix with a trade off of computation time. This also helps avoid ambiguity around the origin of the substitution boxes to avoid accusations of shenanigans.

#### shiftRows step ####

In this step the rows are shifted according to the row number they are in, so each element of row 0 is moved over zero columsn and each element of row 1 is shifted over by one element. This can be seen much more intuitivly in the diagram below

<p>
<image src = './images/shiftRows_example.png' width="350px;"></image>
</p>

#### mixColumns step ####

In this step the 4X4 block matrix is multiplied by a fixed matrix M within GF(2<sup>8</sup>). The arithmetic required for this is covered in the sub-sub-section on multiplication in GF(2<sup>8</sup>).

This step is not performed in the final round of encryption.

##### Multiplication in GF(2<sup>8</sup>) #####

The field GF(2<sup>8</sup>) is a finite field containing 2<sup>8</sup> elements, also known as the Galois field. This field is the ring of integers 2<sup>8</sup> long. Within this ring you can perform the operations of addition, subtraction and multiplication but the input and the results must always be contained within the field.

Addition in this field is performed using a XOR operation, doubling is done using a bitwise shift to the left and halving is done using a bitwise shift to the right. Knowing this we can use Russian peasant multiplication in order to find a way to perform multiplication within GF(2<sup>8</sup>)

Russian peasant multiplication is an algorithm for performing multiplication whereupon you can multiply two numbers A and B. In this algorithm we will first initialise p as zero before starting the first round of the multiplication process.

 With each round we first check if B is odd, if it is we add A to p (using XOR since we are working in GF(2<sup>8</sup>)). Next we double A, using a rightwise bitshift, and check if it is outside GF(2<sup>8</sup>). If A is outside GF(2<sup>8</sup>) we will bring the value of A back inside the field by XORing A with the primitive polynomial, valued at 283 for GF(2<sup>8</sup>). Next we will half B using a bitshift to the left, if this results in B being equal to zero we end the algorithm and return p as the result. Otherwise we go back to the start of the loop and perform another round.


#### addRoundKey ###

In this step the subkeys we generated are used. We take the round subkey, split into a 4X4 matrix in the same way as we did for the input block and XOR each of the bytes of the subkey with each of the bytes of the message. 


### Decryption procedure ###

In order to decrypt the cyphertext and recover the original blocks the procedure for encryption is simply run in reverse.

### Sources ###


* https://sites.math.washington.edu/~morrow/336_12/papers/juan.pdf
* https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
* https://en.wikipedia.org/wiki/AES_key_schedule
* https://en.wikipedia.org/wiki/Rijndael_S-box
* https://en.wikipedia.org/wiki/Rijndael_MixColumns

# I need to add exceptions for keys that are too long !!!!!#