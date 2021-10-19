from cypher.vigenere import VigenereKey, VigenereCipher
from pprint import pprint

k = VigenereKey()
k.validate()
k.print()

pt = 'Hide the gold in the stump'

c = VigenereCipher(plaintext=pt, key=k)
c.encrypt()
print(c.ciphertext)
c.decrypt()
print(c.plaintext)


