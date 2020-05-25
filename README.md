## README ##

This repo contains code for performing AES in python. It supports AES128, 192 and 256. I wrote this code to improve my understanding of the AES algorithm and I hope it will be helpful to you in the same way but please do not attempt to use this code for real world encryption.


## IMPORTANT NOTE !!! ##

I am just some guy in a room, I have no training in cryptography and this code has not been checked by anyone with real training in cryptography. Please do not use this code for any real encryption purposes. I hope you will find this document informative and that the code may be helpful to you in understanding the AES algorithm but please do not attempt to use this code for real world encryption.

## Algorithm description ##

The first step is to create a list of subkeys which will be used in the encryption. 

### Subkey generation ###

The generation of the subkeys works very slightly differently depending on the keylength used. 

#### Generation of subkeys in AES-128 ####

The first 4, 32 bit words are simply the key. Next the rcon value is set to 1 and we calculate the result of the g function. This takes the last 32 bit word and applies the following logic to it

g(W<sub>i</sub>) = SubWord(RotWord(W<sub>i</sub>)) &bigoplus; RC<sub>i/N</sub>

where RotWord is a 8 bit circular shift and SubWord applies a substitution box to each byte in the word. The value of RC<sub>i/N</sub> is given by the table below. Note these values are the same for all versions of AES so it will not be restated. Also note that the values for RC<sub>j</sub> are expressed in base 16.

| i              | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 |
|----------------|----|----|----|----|----|----|----|----|----|----|
| RC<sub>j</sub> | 01 | 02 | 04 | 08 | 10 | 20 | 40 | 80 | 1B | 36 |

This then gives a result where if the word number, i, satisfies i%N = 0 and i >=N then the new word W<sub>i</sub> is given by the following expression.

W<sub>i = W<sub>i-N</sub> &bigoplus; g(W<sub>i-1</sub>)

When i is not divisable by N then the new word is found using the logic shown below.

W<sub>i</sub> = W<sub>i-N</sub> &bigoplus; W<sub>i-1</sub>

This process is repeated until 44, 32 bit words have been generated, allowing for 10 AddRoundKey steps and the introductary AddKey step.


#### Generation of subkeys in AES-192 ####

The process for generating the subkeys for AES-192 is very similar except that we generate 52, 32 bit words which can be collected into 13, 128 bit subkeys to be used in the encryption process. This is done using the same logic as the AES-128 case however since N is larger the application of the g function will occur for every 6 words rather than every 4.


#### Generation of subkeys in AES-256 ####

The process is again similar however there is an extra function to consider, the h function. This will be used when i%N =4 and is described below

h(W<sub>i</sub>) = SubWord(W<sub>i</sub>)

meaning that when i%N = 4 the new word will be generated according to the logic shown below.

W<sub>i</sub> = W<sub>i-N</sub> &bigoplus; h(W<sub>i-1</sub>)

Otherwise the logic will remain the same with N=8 and will generate 60, 32 bit words which may be collected into 15, 128 bit subkeys.

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

(Note I convert from message to list to matrix and back again many times in my shockingly poor implementation, you should not do this but I'm too lazy to go back and fix it. I wrote this code 4 years ago and am only now doing the README.)

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
* https://www.samiam.org/key-schedule.html
* https://en.wikipedia.org/wiki/AES_key_schedule
* https://en.wikipedia.org/wiki/Rijndael_S-box
* https://en.wikipedia.org/wiki/Rijndael_MixColumns

# I'm not sure I'm generating the keys correctly !!!!!#