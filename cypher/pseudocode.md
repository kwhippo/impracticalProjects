# Cipher Pseudocode Guide

## Checklist
- [ ] Module Code
- [ ] Verify Pylint
- [ ] Verify Pydocstyle
- [ ] Verify Coverage
- [ ] cl UI
- [ ] Tk UI

## Function Definitions
### Crypt
Function that defines underlying encryption algorithm by prepping source text, and using a cryptographic protocol 
and a predetermined alphabet.

### Prep Source
Function that prepares and validates source text for encryption algorithm, usually by converting source to UPPER.
May also break text into a list or table.

## Class Definitions
### Key
#### Initialize
| Attribute | Type | Description |
| --- | --- | --- |
| keyword | str | single word |
| alpha_key | str | alphabet-length key |
| key_table | list | list of lists defining alphabet table |
| route | str | structured string of numerals indicating transposition route |
| route_step | str | CHOICE: word or character |
| key_list | list | list of keys |
| numeric_key | int | single number |
| a_key | str | single letter |
| ab_key | str | pair of letters |
| rails | int | number of rails specific to rail fence cipher |

#### Validate Key
Method to validate key attributes.

#### Generate Key
Method to calculate key attributes from an input key attribute or create random key.

### Cipher
#### Initialize
| Attribute | Type | Description |
| --------- | ---- | ----------- |
| plaintext | str | Decrypted message |
| ciphertext | str | Encrypted message |
| alphabet | str | Known alphabet, default is 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' |
| key | obj | Key object with cipher specific encryption keys |

#### Encrypt
Method to encrypt plaintext to ciphertext using key.

#### Decrypt
Method to decrypt ciphertext from plaintext using key.
