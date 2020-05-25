## README ##

This repo contains code for performing AES in python. It supports AES128, 192 and 256


## IMPORTANT NOTE !!! ##

I am just some guy in a room, I have no training in cryptography and this code has not been checked by anyone with real training in cryptography. Please do not use this code for any real encryption purposes. I hope you will find this document informative and that the code may be helpful to you in understanding the AES algorithm but please do not attempt to use this code for real world encryption.


## Algorithm description ##

The first step is to create a list of subkeys which will be used in the encryption. 

### Subkey generation ###

|----------------||----|----|----|----|----|----|----|----|----|----|
| i              || 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 |
|----------------||----|----|----|----|----|----|----|----|----|----|
| rc<sub>i</sub> || 01 | 02 | 04 | 08 | 10 | 20 | 40 | 80 | 1B | 36 |


### Encryption procedure ###

Encryption is done in rounds with the number of rounds being set by the key length with the number rounds for each key length is shown in the table below

| Key length | Rounds |
|------------|--------|
| 128        | 10     |
| 192        | 12     |
| 256        | 14     |



### Decryption procedure ###


### Sources ###


* https://sites.math.washington.edu/~morrow/336_12/papers/juan.pdf
* https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
* https://en.wikipedia.org/wiki/AES_key_schedule